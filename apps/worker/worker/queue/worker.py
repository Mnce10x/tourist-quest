from redis import Redis
from rq import Worker

from worker.config.settings import settings


if __name__ == "__main__":
    redis = Redis.from_url(settings.redis_url)
    worker = Worker(["crawl", "parse", "nlp"], connection=redis)
    worker.work()
