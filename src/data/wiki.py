import argparse
import gzip
import json
from pathlib import Path

from tqdm import tqdm

DATA_DIR = Path("data")
DEFAULT_INPUT_PATH = DATA_DIR / "wikipedia_prefixes_for_qa.txt.gz"
DEFAULT_OUTPUT_PATH = DATA_DIR / "wikipedia_prefixes_for_qa.json"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT_PATH)

    args = parser.parse_args()

    assert args.input.exists(), f"{args.input} not exists"

    data = []

    with gzip.open(args.input, "rt") as f:
        lines = iter(tqdm(f.readlines()))
        try:
            while (first_line := next(lines)).startswith("TITLE: "):
                title = next(lines).strip()
                content_lines = []
                while l := next(lines).strip():
                    content_lines.append(l)
                content = " ".join(content_lines)
                data.append({"title": title, "content": content})
        except StopIteration:
            pass

    with args.output.open("wt") as f:
        json.dump(data, f, indent=True)
