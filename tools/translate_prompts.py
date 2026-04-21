#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
DATE_STR = dt.date.today().isoformat()
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
MYMEMORY_URL = "https://api.mymemory.translated.net/get"
SEGMENT_TOKEN_TEMPLATE = "[[[SEG_{:04d}]]]"
PLACEHOLDER_TEMPLATE = "[[[KEEP_{:04d}]]]"
TEXT_EXTS = {".md", ".mkd", ".txt", ""}
SKIP_DIRS = {"中文", ".git", "tools", "__pycache__"}


def should_translate(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name.startswith("."):
        return False
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.parent == REPO_ROOT:
        return False
    return path.suffix in TEXT_EXTS


def iter_source_files() -> Iterable[Path]:
    for path in sorted(REPO_ROOT.rglob("*")):
        if should_translate(path):
            yield path


def filter_files(files: list[Path], prefixes: list[str]) -> list[Path]:
    if not prefixes:
        return files
    normalized = [prefix.strip("/").strip() for prefix in prefixes if prefix.strip()]
    output: list[Path] = []
    for path in files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        if any(rel == prefix or rel.startswith(prefix + "/") for prefix in normalized):
            output.append(path)
    return output


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def is_rule_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and all(ch in "-|: " for ch in stripped)


def should_keep_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if is_rule_line(line):
        return True
    if re.fullmatch(r"#{1,6}", stripped):
        return True
    if re.fullmatch(r"[`~]{3,}.*", stripped):
        return True
    if re.fullmatch(r"</?[\w:-]+[^>]*>", stripped):
        return True
    if re.fullmatch(r"https?://\S+", stripped):
        return True
    if re.fullmatch(r"[\w./:-]+", stripped) and "/" in stripped:
        return True
    return False


def protect_inline_tokens(text: str) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}

    def replace_pattern(pattern: str, content: str) -> str:
        nonlocal placeholders

        def repl(match: re.Match[str]) -> str:
            key = PLACEHOLDER_TEMPLATE.format(len(placeholders))
            placeholders[key] = match.group(0)
            return key

        return re.sub(pattern, repl, content)

    text = replace_pattern(r"`[^`\n]+`", text)
    text = replace_pattern(r"\[[^\]]+\]\([^)]+\)", text)
    text = replace_pattern(r"https?://\S+", text)
    text = replace_pattern(r"<[^>\n]+>", text)
    return text, placeholders


def restore_inline_tokens(text: str, placeholders: dict[str, str]) -> str:
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def translate_batch(
    segments: list[str],
    source_lang: str = "en",
    target_lang: str = "zh-CN",
    engine: str = "auto",
) -> list[str]:
    if not segments:
        return []
    joined_parts: list[str] = []
    for idx, seg in enumerate(segments):
        if idx:
            joined_parts.append("\n" + SEGMENT_TOKEN_TEMPLATE.format(idx) + "\n")
        joined_parts.append(seg)
    query = "".join(joined_parts)
    data = urllib.parse.urlencode(
        {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": query,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        TRANSLATE_URL,
        data=data,
        headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"},
    )
    translated = None
    if engine in {"auto", "google"}:
        for attempt, delay in enumerate((0, 2, 5), start=1):
            if delay:
                time.sleep(delay)
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                translated = "".join(part[0] for part in payload[0])
                break
            except HTTPError as exc:
                if exc.code != 429 or attempt == 3:
                    translated = None
                    break

    if translated is None:
        return [translate_with_mymemory(seg, source_lang, target_lang) for seg in segments]

    if len(segments) == 1:
        return [translated]

    tokenized = translated
    split_tokens = ["\n" + SEGMENT_TOKEN_TEMPLATE.format(i) + "\n" for i in range(1, len(segments))]
    output: list[str] = []
    cursor = tokenized
    for token in split_tokens:
        head, sep, tail = cursor.partition(token)
        if not sep:
            raise RuntimeError(f"Translation separator was lost: {token}")
        output.append(head)
        cursor = tail
    output.append(cursor)
    return output


def translate_with_mymemory(text: str, source_lang: str, target_lang: str) -> str:
    if len(text) > 800:
        return "".join(translate_with_mymemory(piece, source_lang, target_lang) for piece in split_text_for_fallback(text, 700))

    params = urllib.parse.urlencode({"q": text, "langpair": f"{source_lang}|{target_lang}"})
    request = urllib.request.Request(
        f"{MYMEMORY_URL}?{params}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    for attempt, delay in enumerate((0, 2, 5), start=1):
        if delay:
            time.sleep(delay)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload["responseData"]["translatedText"]
        except HTTPError as exc:
            if exc.code != 429 or attempt == 3:
                raise
    raise RuntimeError("MyMemory translation failed after retries")


def split_text_for_fallback(text: str, max_len: int) -> list[str]:
    pieces = re.split(r"(\n\s*\n)", text)
    output: list[str] = []
    chunk = ""
    for piece in pieces:
        if not piece:
            continue
        if chunk and len(chunk) + len(piece) > max_len:
            output.append(chunk)
            chunk = ""
        if len(piece) > max_len:
            lines = piece.splitlines(keepends=True)
            for line in lines:
                if chunk and len(chunk) + len(line) > max_len:
                    output.append(chunk)
                    chunk = ""
                if len(line) > max_len:
                    output.extend(line[i : i + max_len] for i in range(0, len(line), max_len))
                else:
                    chunk += line
        else:
            chunk += piece
    if chunk:
        output.append(chunk)
    return output


def batched_translate_blocks(blocks: list[str], engine: str = "auto") -> list[str]:
    translated: list[str] = []
    batch_original: list[str] = []
    batch_meta: list[dict[str, object]] = []
    char_limit = 12000

    def flush() -> None:
        nonlocal batch_original, batch_meta
        if not batch_original:
            return
        batch_result = translate_batch(batch_original, engine=engine)
        for meta, text in zip(batch_meta, batch_result):
            restored = restore_inline_tokens(text, meta["placeholders"])  # type: ignore[arg-type]
            translated.append(restored)
        batch_original = []
        batch_meta = []
        time.sleep(0.05)

    for block in blocks:
        if not block.strip():
            flush()
            translated.append(block)
            continue

        lines = block.splitlines()
        if lines and all(should_keep_line(line) for line in lines):
            flush()
            translated.append(block)
            continue

        protected, placeholders = protect_inline_tokens(block)
        if not re.search(r"[A-Za-z]{2,}", protected):
            flush()
            translated.append(block)
            continue

        current_chars = sum(len(item) for item in batch_original)
        if batch_original and current_chars + len(protected) > char_limit:
            flush()

        batch_original.append(protected)
        batch_meta.append({"placeholders": placeholders})

    flush()
    return translated


def split_non_code_blocks(text: str) -> list[str]:
    parts = re.split(r"(\n\s*\n)", text)
    blocks: list[str] = []
    pending = ""
    for part in parts:
        if not part:
            continue
        if re.fullmatch(r"\n\s*\n", part):
            if pending:
                blocks.append(pending)
                pending = ""
            blocks.append(part)
        else:
            pending += part
    if pending:
        blocks.append(pending)
    return split_long_blocks(blocks)


def split_long_blocks(blocks: list[str], max_len: int = 5000) -> list[str]:
    output: list[str] = []
    for block in blocks:
        if len(block) <= max_len or not block.strip():
            output.append(block)
            continue

        lines = block.splitlines(keepends=True)
        chunk = ""
        for line in lines:
            if len(line) > max_len:
                if chunk:
                    output.append(chunk)
                    chunk = ""
                output.extend(split_very_long_line(line, max_len))
                continue
            if chunk and len(chunk) + len(line) > max_len:
                output.append(chunk)
                chunk = ""
            chunk += line
        if chunk:
            output.append(chunk)
    return output


def split_very_long_line(line: str, max_len: int) -> list[str]:
    pieces = re.split(r"(?<=[.;:!?])\s+", line)
    if len(pieces) == 1:
        return [line[i : i + max_len] for i in range(0, len(line), max_len)]

    output: list[str] = []
    chunk = ""
    for piece in pieces:
        if chunk and len(chunk) + len(piece) + 1 > max_len:
            output.append(chunk.rstrip() + "\n")
            chunk = ""
        chunk += piece + " "
    if chunk:
        output.append(chunk.rstrip())
    return output


def translate_content(content: str, engine: str = "auto") -> str:
    lines = content.splitlines()
    output: list[str] = []
    buffer: list[str] = []
    in_fence = False

    def flush_buffer() -> None:
        nonlocal buffer
        if not buffer:
            return
        text = "\n".join(buffer)
        output.extend(batched_translate_blocks(split_non_code_blocks(text), engine=engine))
        buffer = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush_buffer()
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue
        buffer.append(line)

    flush_buffer()
    return "".join(output).rstrip() + "\n"


def build_output(source_path: Path, translated_body: str) -> str:
    title = source_path.stem if source_path.suffix else source_path.name
    source_rel = source_path.relative_to(REPO_ROOT)
    return (
        f"# {title}（中文翻译）\n\n"
        f"> 原文：`../{source_path.name}`\n"
        f"> 来源路径：`{source_rel.as_posix()}`\n"
        f"> 翻译方式：脚本批量翻译\n"
        f"> 翻译日期：{DATE_STR}\n\n"
        f"---\n\n"
        f"{translated_body}"
    )


def translate_file(source_path: Path, engine: str = "auto") -> Path:
    source_text = read_text(source_path)
    translated_body = translate_content(source_text, engine=engine)
    output_path = source_path.parent / "中文" / source_path.name
    write_text(output_path, build_output(source_path, translated_body))
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate prompt files into Chinese subfolders.")
    parser.add_argument("--limit", type=int, default=0, help="Only translate the first N files.")
    parser.add_argument("--paths", nargs="*", default=[], help="Only translate files under these repo-relative paths.")
    parser.add_argument("--engine", choices=["auto", "google", "mymemory"], default="auto")
    args = parser.parse_args()

    files = list(iter_source_files())
    files = filter_files(files, args.paths)
    if args.limit > 0:
        files = files[: args.limit]

    if not files:
        print("No source files found.")
        return 0

    translated_paths: list[Path] = []
    for idx, source_path in enumerate(files, start=1):
        try:
            output_path = translate_file(source_path, engine=args.engine)
            translated_paths.append(output_path)
            print(f"[{idx}/{len(files)}] {source_path.relative_to(REPO_ROOT)} -> {output_path.relative_to(REPO_ROOT)}")
        except Exception as exc:  # pragma: no cover
            print(f"Failed to translate {source_path}: {exc}", file=sys.stderr)
            return 1

    print(f"Translated {len(translated_paths)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
