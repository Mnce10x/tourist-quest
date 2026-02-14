import hashlib
import re
import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

from worker.storage.object_store import LocalObjectStore

ALLOWED_SCHEMES = {"http", "https"}


def safe_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        return False
    host = parsed.hostname or ""
    return not re.match(r"^(localhost|127\.|0\.0\.0\.0)", host)


def _robots_allowed(client: httpx.Client, url: str, respect_robots: bool = True) -> bool:
    if not respect_robots:
        return True
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        text = client.get(robots_url, timeout=10).text
        rp.parse(text.splitlines())
        return rp.can_fetch("TourismIntelBot", url)
    except Exception:
        return True


def discover_sitemaps(client: httpx.Client, base_url: str) -> list[str]:
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    sitemap_urls = []
    try:
        robots_txt = client.get(robots_url, timeout=10).text
        for line in robots_txt.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_urls.append(line.split(":", 1)[1].strip())
    except Exception:
        pass
    if not sitemap_urls:
        sitemap_urls.append(f"{parsed.scheme}://{parsed.netloc}/sitemap.xml")
    return sitemap_urls


def extract_links_from_sitemap(xml_content: str) -> list[str]:
    soup = BeautifulSoup(xml_content, "xml")
    return [loc.text.strip() for loc in soup.find_all("loc") if loc.text.strip()]


def discover_and_fetch(seed_urls: list[str], crawl_delay: float = 0.5, respect_robots: bool = True) -> list[dict]:
    store = LocalObjectStore()
    docs = []
    seen = set()
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        targets = list(seed_urls)
        for seed in seed_urls:
            if safe_url(seed):
                for sitemap in discover_sitemaps(client, seed):
                    if not safe_url(sitemap):
                        continue
                    try:
                        xml = client.get(sitemap).text
                        targets.extend(extract_links_from_sitemap(xml)[:60])
                    except Exception:
                        continue

        for target in targets:
            if target in seen or not safe_url(target):
                continue
            seen.add(target)
            if not _robots_allowed(client, target, respect_robots):
                continue
            try:
                response = client.get(target)
            except Exception:
                continue
            if response.status_code >= 400:
                continue
            content_type = response.headers.get("content-type", "")
            h = hashlib.sha256(response.content).hexdigest()
            if ".pdf" in target.lower() or "pdf" in content_type.lower():
                key = f"pdf/{h}.pdf"
                store.put(key, response.content)
                docs.append({"url": target, "object_key": key, "file_hash": h, "content_type": "application/pdf"})
            else:
                key = f"html/{h}.html"
                store.put(key, response.content)
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(" ", strip=True)
                docs.append({"url": target, "object_key": key, "file_hash": h, "content_type": "text/html", "text": text[:12000]})
                for a in soup.select("a[href]")[:50]:
                    href = urljoin(target, a["href"])
                    if safe_url(href) and href not in seen:
                        targets.append(href)
            time.sleep(crawl_delay)
    return docs
