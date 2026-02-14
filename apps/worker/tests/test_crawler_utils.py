from worker.pipelines.crawler import extract_links_from_sitemap, safe_url


def test_safe_url_blocks_localhost():
    assert not safe_url('http://localhost/test')
    assert safe_url('https://www.tourism.gov.za')


def test_extract_links_from_sitemap():
    xml = '<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url></urlset>'
    links = extract_links_from_sitemap(xml)
    assert links == ['https://x/a', 'https://x/b']
