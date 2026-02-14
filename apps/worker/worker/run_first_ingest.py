import argparse
import json

from worker.pipelines.ingest import run_ingest


def main():
    parser = argparse.ArgumentParser(description="Run initial tourism ingestion")
    parser.add_argument("--no-persist", action="store_true", help="Skip writing extracted records to database")
    args = parser.parse_args()
    result = run_ingest(persist=not args.no_persist)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
