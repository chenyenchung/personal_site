#!/usr/bin/env python3
"""Fetch publication metadata from Crossref for the local Hugo data file."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SOURCE = Path("data/publications.yaml")
OUTPUT = Path("data/publications_generated.json")
CROSSREF_WORKS_URL = "https://api.crossref.org/works/"


def parse_scalar(value: str):
    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_source(path: Path) -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    active_list_key: str | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        stripped = line.strip()
        if stripped.startswith("- "):
            content = stripped[2:].strip()
            if ":" in content:
                if line.startswith("- "):
                    current = {}
                    records.append(current)
                    active_list_key = None
                    key, value = content.split(":", 1)
                    current[key.strip()] = parse_scalar(value)
                else:
                    raise ValueError(f"Nested maps are not supported at line {line_number}")
            else:
                if current is None or active_list_key is None:
                    raise ValueError(f"List item without an active key at line {line_number}")
                current.setdefault(active_list_key, []).append(parse_scalar(content))
            continue

        if current is None:
            raise ValueError(f"Expected a record before line {line_number}")

        if ":" not in stripped:
            raise ValueError(f"Expected key/value at line {line_number}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            current[key] = parse_scalar(value)
            active_list_key = None
        else:
            current[key] = []
            active_list_key = key

    return records


def normalize_doi(doi: str) -> str:
    doi = doi.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            return doi[len(prefix) :]
    return doi


def doi_url(doi: str) -> str:
    return "https://doi.org/" + normalize_doi(doi)


def crossref_date(message: dict) -> tuple[str, int | None]:
    for key in ("published-print", "published-online", "published", "issued"):
        date_parts = message.get(key, {}).get("date-parts", [])
        if not date_parts or not date_parts[0]:
            continue
        parts = date_parts[0]
        year = int(parts[0])
        month = int(parts[1]) if len(parts) > 1 else 1
        day = int(parts[2]) if len(parts) > 2 else 1
        return f"{year:04d}-{month:02d}-{day:02d}", year
    return "", None


def normalize_author(author: dict) -> str:
    if author.get("given") and author.get("family"):
        return f"{author['given']} {author['family']}".strip()
    if author.get("name"):
        return str(author["name"]).strip()
    if author.get("family"):
        return str(author["family"]).strip()
    return ""


def get_first(message: dict, key: str) -> str:
    value = message.get(key)
    if isinstance(value, list):
        return str(value[0]).strip() if value else ""
    return str(value).strip() if value else ""


def normalize_text(value: str) -> str:
    value = html.unescape(str(value))
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def fetch_crossref(doi: str, mailto: str, timeout: int) -> dict:
    encoded_doi = urllib.parse.quote(normalize_doi(doi), safe="")
    query = urllib.parse.urlencode({"mailto": mailto}) if mailto else ""
    url = CROSSREF_WORKS_URL + encoded_doi + (f"?{query}" if query else "")
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": f"yenchungchen.com publication sync ({mailto})",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["message"]


def build_record(source: dict, message: dict) -> dict:
    date, year = crossref_date(message)
    crossref_authors = [normalize_author(author) for author in message.get("author", [])]
    crossref_authors = [author for author in crossref_authors if author]
    authors = source.get("authors") or crossref_authors
    journal_short = source.get("journal_short") or normalize_text(
        get_first(message, "short-container-title")
    )
    journal = source.get("journal") or normalize_text(
        get_first(message, "container-title")
    ) or journal_short
    doi = normalize_doi(str(source["doi"]))

    return {
        "slug": source["slug"],
        "doi": doi,
        "doi_url": doi_url(doi),
        "title": source.get("title") or normalize_text(get_first(message, "title")),
        "authors": authors,
        "journal": journal,
        "journal_short": journal_short,
        "date": date,
        "year": year,
        "projects": source.get("projects", []),
        "featured": bool(source.get("featured", False)),
        "image": source.get("image", ""),
        "full_text": source.get("full_text", ""),
        "bts": source.get("bts", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--mailto",
        default=os.environ.get("CROSSREF_MAILTO", "ycc520@nyu.edu"),
        help="Email address for Crossref polite pool requests.",
    )
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--sleep", type=float, default=0.1)
    args = parser.parse_args()

    sources = parse_source(args.source)
    generated = []
    failures = []

    for source in sources:
        slug = source.get("slug", "<missing slug>")
        try:
            message = fetch_crossref(str(source["doi"]), args.mailto, args.timeout)
            record = build_record(source, message)
            if not record["title"] or not record["authors"]:
                failures.append(f"{slug}: Crossref record is missing title or authors")
            generated.append(record)
            print(f"synced {slug}", file=sys.stderr)
        except (KeyError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            failures.append(f"{slug}: {exc}")
        time.sleep(args.sleep)

    if failures:
        print("Publication sync failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    args.output.write_text(
        json.dumps(generated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
