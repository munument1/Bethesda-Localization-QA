from __future__ import annotations

import collections
import csv
import re
from pathlib import Path

FORMAL_PATTERNS = (
    r"습니다[.!?…]*$",
    r"습니까[?!…]*$",
    r"십시오[.!?…]*$",
    r"입니다[.!?…]*$",
    r"입니까[?!…]*$",
)
POLITE_PATTERNS = (r"요[.!?…]*$", r"세요[.!?…]*$", r"죠[.!?…]*$")
PLAIN_PATTERNS = (r"(?:다|냐|니|라|자|군|네|어|아)[.!?…]*$",)

STYLE_RULE = (
    "Preserve the speaker's social register and attitude, not English word order. "
    "Use surrounding dialogue, titles, commands, hostility, intimacy, rank, and explicit "
    "honorific cues. Do not arbitrarily switch between 반말, 해요체, and 합니다체 within "
    "the same conversational voice. If speaker/relationship is uncertain, prefer neutral "
    "natural 존댓말 rather than inventing intimacy or hierarchy. Hostile or explicitly casual "
    "dialogue may use 반말 when supported by context. Preserve sarcasm, jokes, emotional shifts, "
    "and character voice."
)

TONE_HINT_TEXT = {
    "FORMAL_HAPSYO": (
        "Prior evidence for this exact source line consistently used 합니다/하십시오체. "
        "Use this only as a speech-level hint, not wording to copy."
    ),
    "POLITE_HAEYO": (
        "Prior evidence for this exact source line consistently used 해요체. "
        "Use this only as a speech-level hint, not wording to copy."
    ),
    "PLAIN": (
        "Prior evidence for this exact source line consistently used plain/반말 style. "
        "Use this only as a speech-level hint, not wording to copy."
    ),
}


def classify_korean_tone(text: str) -> str:
    s = (text or "").strip()
    if not s:
        return "UNKNOWN"
    s = re.sub(r'["”’\']+$', "", s).strip()
    for pattern in FORMAL_PATTERNS:
        if re.search(pattern, s):
            return "FORMAL_HAPSYO"
    for pattern in POLITE_PATTERNS:
        if re.search(pattern, s):
            return "POLITE_HAEYO"
    for pattern in PLAIN_PATTERNS:
        if re.search(pattern, s):
            return "PLAIN"
    return "UNKNOWN"


def build_legacy_style_index(paths, *, record_type="INFO", min_confidence=0.8):
    counts = collections.defaultdict(collections.Counter)
    for path in paths:
        p = Path(path)
        if not p.exists():
            continue
        with p.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if record_type and (row.get("record_type") or "") != record_type:
                    continue
                source = (row.get("old_english") or row.get("source_english") or "").strip()
                korean = (row.get("new_korean") or row.get("korean") or "").strip()
                if not source or not korean:
                    continue
                tone = classify_korean_tone(korean)
                if tone != "UNKNOWN":
                    counts[source][tone] += 1

    result = {}
    for source, counter in counts.items():
        total = sum(counter.values())
        tone, n = counter.most_common(1)[0]
        confidence = n / total
        if confidence >= min_confidence:
            result[source] = {
                "tone": tone,
                "confidence": round(confidence, 3),
                "count": total,
            }
    return result


def load_speaker_map(path):
    out = {}
    p = Path(path)
    if not p.exists():
        return out
    with p.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            out[(row.get("source_file", ""), row.get("info_formid", ""))] = row
    return out


def load_style_profiles(path, aliases=None):
    out = {}
    p = Path(path)
    if not p.exists():
        return out
    with p.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            name = (row.get("speaker_name") or "").strip()
            if name:
                out[name.casefold()] = row

    for alias, canonical in (aliases or {}).items():
        canonical_row = out.get(canonical.casefold())
        if canonical_row:
            out[alias.casefold()] = canonical_row
    return out


def speaker_metadata(item, speaker_map, profiles):
    rec = speaker_map.get((item.get("source_file", ""), item.get("formid", "")))
    if not rec:
        return None, None

    names = [x for x in (rec.get("speaker_names") or "").split("|") if x]
    meta = {
        "confidence": rec.get("speaker_confidence", ""),
        "speaker_formids": rec.get("speaker_formids", ""),
        "speaker_names": names,
        "evidence": rec.get("evidence", ""),
    }
    profile = profiles.get(names[0].casefold()) if len(names) == 1 else None
    return meta, profile


def load_dialog_context_map(path):
    out = {}
    p = Path(path)
    if not p.exists():
        return out
    with p.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            out[(row.get("source_file", ""), row.get("dial_formid", ""))] = row
    return out


def dialogue_context_metadata(item, dialog_map):
    rec = dialog_map.get(
        (item.get("source_file", ""), item.get("parent_dialog_formid", ""))
    )
    if not rec:
        return None
    return {
        "topic_editor_id": rec.get("editor_id", ""),
        "topic_name": rec.get("full", ""),
        "dialogue_type": rec.get("dialogue_type_name", ""),
        "addressee_hint": rec.get("addressee_hint", ""),
    }
