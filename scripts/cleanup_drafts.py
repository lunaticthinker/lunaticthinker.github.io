#!/usr/bin/env python3
"""Cleanup WordPress-exported markdown drafts for Hugo.

Features:
    - Recursively scans (using Path.rglob) all Markdown files under a chosen directory (defaults to `drafts/`).
    - Fixes common HTML entities / smart quotes to UTF-8 (via html.unescape).
    - Strips known WordPress / theme front matter keys.
    - Removes Visual Composer and similar shortcodes.
    - Optionally strips obvious layout-only HTML wrappers (only `eltd-` / `wp-` class div/span wrappers).

CLI Options:
    --dir <path>        Base directory (relative to repo root) to process. Default: drafts
    --dry-run           Show which files would change without modifying them.
    --verbose           Extra logging.
    --no-recursive      Limit to top-level *.md files (no descent). (Default is recursive.)

Usage:
        python scripts/cleanup_drafts.py              # clean drafts recursively
        python scripts/cleanup_drafts.py --dry-run    # see what would change
        python scripts/cleanup_drafts.py --dir drafts/posts

Review changes with `git diff` afterwards.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple
import html

RE_DRAFT_MD = re.compile(r".*\.md$", re.IGNORECASE)

# Keys in front matter to drop entirely
FRONTMATTER_DROP_KEYS = {
    "eltd_disable_footer_meta",
    "eltd_hide_background_image_meta",
    "eltd_show_title_area_meta",
    "eltd_page_padding_meta",
    "aktt_notify_twitter",
    "author",  # FixIt theme uses global params.author from config.toml
}

# Simple shortcode pattern: [vc_xxx ...] or [/vc_xxx]
SHORTCODE_RE = re.compile(r"\\[(?:/)?vc_[^\\]]*\\]")

# WordPress more tag
MORE_TAG_RE = re.compile(r"<!--more-->", re.IGNORECASE)

# Very broad div/span wrappers with eltd- / wp- style classes
LAYOUT_WRAPPER_RE = re.compile(
    r"<(?:div|span)([^>]*class=\"(?:eltd-|wp-)[^>]*>).*?</(?:div|span)>",
    re.DOTALL | re.IGNORECASE,
)


def split_front_matter(text: str) -> Tuple[str, str]:
    """Split Hugo/TOML front matter (`---` ... `---`) from body.

    Returns (front_matter, body). If no front matter, front_matter is ''.
    """
    if not text.lstrip().startswith("---"):
        return "", text

    # Find the first line starting with ---
    lines = text.splitlines(keepends=True)
    if not lines:
        return "", text

    if not lines[0].strip().startswith("---"):
        return "", text

    fm_lines = [lines[0]]
    i = 1
    while i < len(lines):
        fm_lines.append(lines[i])
        if lines[i].strip().startswith("---"):
            i += 1
            break
        i += 1

    front_matter = "".join(fm_lines)
    body = "".join(lines[i:])
    return front_matter, body


def clean_front_matter(front_matter: str) -> str:
    if not front_matter:
        return front_matter

    cleaned_lines = []
    skip_block_key = None

    for line in front_matter.splitlines(keepends=False):
        # Detect top-level keys like `key:` or `key =`
        m = re.match(r"^([A-Za-z0-9_]+)\\s*[:=]", line)
        if m:
            key = m.group(1)
            if key in FRONTMATTER_DROP_KEYS:
                skip_block_key = key
                continue
            else:
                skip_block_key = None

        # Skip indented lines belonging to a dropped key block
        if skip_block_key is not None and (line.startswith("  ") or line.startswith("\t") or not line.strip()):
            continue

        cleaned_lines.append(line)

    result = "\n".join(cleaned_lines)
    if result and not result.endswith("\n"):
        result += "\n"
    return result


def decode_entities(text: str) -> str:
    # Use html.unescape for most entities, then handle a few special cases if needed.
    text = html.unescape(text)
    return text


def strip_shortcodes(text: str) -> str:
    return SHORTCODE_RE.sub("", text)


def strip_more_tags(text: str) -> str:
    return MORE_TAG_RE.sub("", text)


def strip_layout_wrappers(text: str) -> str:
    # Conservative: remove only obvious eltd-/wp- wrappers; leave other HTML intact.
    return LAYOUT_WRAPPER_RE.sub("", text)


def clean_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(original)

    new_front = clean_front_matter(front_matter)

    new_body = body
    new_body = strip_shortcodes(new_body)
    new_body = strip_more_tags(new_body)
    new_body = strip_layout_wrappers(new_body)
    new_body = decode_entities(new_body)

    cleaned = f"{new_front}{new_body}"

    if cleaned == original:
        return False

    path.write_text(cleaned, encoding="utf-8")
    return True


def gather_files(base: Path, recursive: bool, verbose: bool = False) -> list[Path]:
    if recursive:
        raw_iter = list(base.rglob("*.md"))
    else:
        raw_iter = list(base.glob("*.md"))
    files = [p for p in raw_iter if RE_DRAFT_MD.match(p.name)]
    if verbose:
        print(f"[DEBUG] gather_files: base={base} recursive={recursive} raw_count={len(raw_iter)} filtered_count={len(files)}")
        for sample in raw_iter[:5]:
            print(f"[DEBUG] sample path: {sample}")
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean WordPress-exported markdown for Hugo.")
    parser.add_argument("--dir", default="drafts", help="Directory (relative to repo root) to scan recursively.")
    parser.add_argument("--dry-run", action="store_true", help="Report files that would change without writing.")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging.")
    parser.add_argument("--no-recursive", action="store_true", help="Do not recurse; only process top-level .md files.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    target_dir = (repo_root / args.dir).resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Directory not found: {target_dir}", file=sys.stderr)
        return 1

    files = gather_files(target_dir, recursive=not args.no_recursive, verbose=args.verbose)
    if args.verbose:
        print(f"Scanning {'recursively' if not args.no_recursive else 'non-recursively'} in: {target_dir}")
        print(f"Found {len(files)} markdown files.")

    changed = 0
    total = 0

    for md_path in files:
        total += 1
        original = md_path.read_text(encoding="utf-8")
        front_matter, body = split_front_matter(original)
        new_front = clean_front_matter(front_matter)
        new_body = body
        new_body = strip_shortcodes(new_body)
        new_body = strip_more_tags(new_body)
        new_body = strip_layout_wrappers(new_body)
        new_body = decode_entities(new_body)
        cleaned = f"{new_front}{new_body}"
        if cleaned != original:
            changed += 1
            rel = md_path.relative_to(repo_root)
            if args.dry_run:
                print(f"[DRY] Would clean: {rel}")
            else:
                md_path.write_text(cleaned, encoding="utf-8")
                print(f"Cleaned: {rel}")

    print(f"Processed {total} markdown files; changed {changed}{' (dry-run)' if args.dry_run else ''}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
