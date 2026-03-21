from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import feedparser
import httpx
import yaml
from bs4 import BeautifulSoup


@dataclass
class Item:
    title: str
    url: str
    source: str
    published: str | None = None
    score: int = 0


def load_config(config_path: str | Path) -> dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_rss(name: str, url: str) -> list[Item]:
    feed = feedparser.parse(url)
    items: list[Item] = []
    for entry in feed.entries:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not title or not link:
            continue
        published = entry.get("published") or entry.get("updated")
        items.append(Item(title=title, url=link, source=name, published=published))
    return items


def fetch_html(name: str, spec: dict[str, Any]) -> list[Item]:
    resp = httpx.get(spec["url"], timeout=20, follow_redirects=True)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    item_selector = spec["item_selector"]
    title_selector = spec.get("title_selector")
    link_selector = spec.get("link_selector", "a")

    items: list[Item] = []
    for node in soup.select(item_selector):
        title_node = node.select_one(title_selector) if title_selector else node
        link_node = node.select_one(link_selector)
        if not title_node or not link_node:
            continue
        title = title_node.get_text(" ", strip=True)
        href = link_node.get("href")
        if not title or not href:
            continue
        link = urljoin(spec["url"], href)
        items.append(Item(title=title, url=link, source=name))
    return items


def score_item(item: Item, topic_name: str) -> int:
    score = 0
    if topic_name and topic_name.lower() in item.title.lower():
        score += 5
    if item.published:
        score += 1
    return score


def dedupe_items(items: list[Item]) -> list[Item]:
    seen: set[str] = set()
    deduped: list[Item] = []
    for item in items:
        key = hashlib.sha256(f"{item.title}|{item.url}".encode("utf-8")).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def collect_items(config_path: str | Path) -> list[Item]:
    config = load_config(config_path)
    topic_name = config.get("topic_name", "")
    collected: list[Item] = []
    for source in config.get("sources", []):
        source_type = source.get("type")
        name = source.get("name", "unknown")
        if source_type == "rss":
            collected.extend(fetch_rss(name, source["url"]))
        elif source_type == "html":
            collected.extend(fetch_html(name, source))
        else:
            raise ValueError(f"Unsupported source type: {source_type}")

    items = dedupe_items(collected)
    for item in items:
        item.score = score_item(item, topic_name)
    items.sort(key=lambda x: (-x.score, x.source, x.title))
    max_items = int(config.get("max_items_per_run", 5))
    return items[:max_items]


def save_snapshot(items: list[Item], out_dir: str | Path = "runtime") -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out / f"snapshot_{stamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(x) for x in items], f, ensure_ascii=False, indent=2)
    return path
