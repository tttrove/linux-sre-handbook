#!/usr/bin/env python3
"""Convert Obsidian [[wikilinks]] to standard Markdown [text](path.md) links.

Run this script to convert all wiki-links in the linux-sre-handbook vault.
Usage: python convert_wikilinks.py

NOTE: This script has already been run manually. All wiki-links in the
vault have been converted. This script is kept for reference.
"""

import os
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.resolve()

WIKI_PATTERN = re.compile(r'\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]')


def build_filename_index(root: Path) -> dict[str, str]:
    """Map filename_stem -> relative_path_from_vault_root (without .md)."""
    index = {}
    for md_file in sorted(root.rglob("*.md")):
        if '.obsidian' in str(md_file.relative_to(root)):
            continue
        rel = md_file.relative_to(root)
        stem = md_file.stem
        rel_no_ext = str(rel.with_suffix('')).replace('\\', '/')
        index[stem] = rel_no_ext
        index[rel_no_ext] = rel_no_ext
    return index


def resolve_target(target: str, current_file: str, file_index: dict[str, str]) -> str | None:
    """Resolve a wiki-link target to a vault-relative path (without .md)."""
    clean_target = target.lstrip('/')

    if '/' in clean_target:
        return clean_target

    if clean_target in file_index:
        return file_index[clean_target]

    return None


def compute_relative_path(from_file: str, to_path: str) -> str:
    """Compute relative path from current file to target file."""
    from_parts = from_file.split('/')
    to_parts = to_path.split('/')

    if len(from_parts) > 1:
        from_dir = from_parts[:-1]
    else:
        from_dir = []

    i = 0
    while i < len(from_dir) and i < len(to_parts) and from_dir[i] == to_parts[i]:
        i += 1

    rel_parts = ['..'] * (len(from_dir) - i) + to_parts[i:]

    if not rel_parts:
        return os.path.basename(to_path) + '.md'

    return '/'.join(rel_parts) + '.md'


def convert_links_in_file(filepath: Path, file_index: dict[str, str]) -> tuple[int, int]:
    """Convert all wiki-links in a single file. Returns (modified_count, link_count)."""
    content = filepath.read_text(encoding='utf-8')
    vault_rel = str(filepath.relative_to(VAULT_ROOT)).replace('\\', '/')
    vault_rel_no_ext = vault_rel.rsplit('.', 1)[0]

    count = 0
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        new_line = line
        pos = 0
        while True:
            start = new_line.find('[[', pos)
            if start == -1:
                break

            end = new_line.find(']]', start)
            if end == -1:
                break

            after_open = new_line[start+2:start+3] if start+2 < len(new_line) else ''
            if after_open in (' ', '\t'):
                pos = end + 2
                continue

            inner = new_line[start+2:end]
            inner_stripped = inner.strip()
            if not inner_stripped:
                pos = end + 2
                continue

            pipe_pos = inner.find('|')
            if pipe_pos != -1:
                target = inner[:pipe_pos].strip()
                display = inner[pipe_pos+1:].strip()
            else:
                target = inner_stripped
                display = None

            if target.startswith('$') or target.startswith('"') or target.startswith("'"):
                pos = end + 2
                continue

            if target == '双向链接':
                pos = end + 2
                continue

            resolved = resolve_target(target, vault_rel_no_ext, file_index)
            if resolved is None:
                pos = end + 2
                continue

            rel_path = compute_relative_path(vault_rel_no_ext, resolved)
            display_text = display if display else (target.rsplit('/', 1)[-1] if '/' in target else target)

            replacement = f'[{display_text}]({rel_path})'
            new_line = new_line[:start] + replacement + new_line[end+2:]
            pos = start + len(replacement)
            count += 1

        new_lines.append(new_line)

    new_content = '\n'.join(new_lines)

    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        return 1, count

    return 0, count


def main():
    if not VAULT_ROOT.exists():
        print(f"ERROR: Vault root not found: {VAULT_ROOT}")
        sys.exit(1)

    print(f"Building filename index from {VAULT_ROOT}...")
    file_index = build_filename_index(VAULT_ROOT)
    print(f"  Indexed {len(file_index)} entries")

    total_files = 0
    total_links = 0

    for md_file in sorted(VAULT_ROOT.rglob("*.md")):
        if '.obsidian' in str(md_file.relative_to(VAULT_ROOT)):
            continue
        files_mod, links = convert_links_in_file(md_file, file_index)
        if files_mod > 0:
            rel = str(md_file.relative_to(VAULT_ROOT)).replace('\\', '/')
            print(f"  {rel}: {links} links")
            total_files += files_mod
            total_links += links

    print(f"\nDone: {total_files} files modified, {total_links} links converted.")


if __name__ == '__main__':
    main()
