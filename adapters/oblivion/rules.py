from __future__ import annotations

import struct

GET_IS_ID_FUNCTION = 72

DIALOGUE_TYPE_NAMES = {
    0: "TOPIC",
    1: "CONVERSATION",
    2: "COMBAT",
    3: "PERSUASION",
    4: "DETECTION",
    5: "SERVICE",
    6: "MISC",
}

SPECIAL_CONVERSATION_EDIDS = {
    "INFOGENERAL",
    "HELLO",
    "GOODBYE",
    "IdleChatter",
}


def extract_getisid_formids(ctda_payloads):
    """Return FormIDs referenced by TES4 GetIsID conditions.

    The adapter expects raw CTDA payload bytes from a record parser.
    In TES4 CTDA, the condition function is at offset 8 and parameter 1
    is at offset 12 for the GetIsID cases used by INFO speaker restrictions.
    """
    result = []
    for raw in ctda_payloads:
        if len(raw) < 16:
            continue
        function = struct.unpack_from("<I", raw, 8)[0]
        if function != GET_IS_ID_FUNCTION:
            continue
        formid = struct.unpack_from("<I", raw, 12)[0]
        if formid not in result:
            result.append(formid)
    return result


def classify_speaker_candidates(formids, npc_lookup):
    """Resolve candidate FormIDs against a caller-supplied NPC lookup.

    npc_lookup maps integer FormID -> {"editor_id": ..., "name": ...}.
    """
    candidates = []
    for formid in formids:
        npc = npc_lookup.get(formid) or {}
        if not npc:
            continue
        candidates.append(
            {
                "formid": f"{formid:08X}",
                "editor_id": npc.get("editor_id", ""),
                "name": npc.get("name", ""),
            }
        )

    if len(candidates) == 1:
        confidence = "EXACT_SINGLE"
    elif len(candidates) > 1:
        confidence = "EXACT_SET"
    else:
        confidence = "UNRESOLVED_ID"

    return {
        "speaker_confidence": confidence,
        "speaker_count": len(candidates),
        "speaker_formids": "|".join(x["formid"] for x in candidates),
        "speaker_names": "|".join(
            x["name"] or x["editor_id"] for x in candidates
        ),
        "speaker_editor_ids": "|".join(x["editor_id"] for x in candidates),
        "evidence": "CTDA:GetIsID",
    }


def classify_dialogue_context(dialogue_type, editor_id=""):
    name = DIALOGUE_TYPE_NAMES.get(dialogue_type, "UNKNOWN")

    if dialogue_type == 0:
        addressee_hint = "PLAYER_LIKELY"
    elif dialogue_type == 1 and editor_id in SPECIAL_CONVERSATION_EDIDS:
        addressee_hint = "SPECIAL_CONVERSATION_OR_BARK"
    elif dialogue_type == 1:
        addressee_hint = "NPC_CONVERSATION_OR_SCRIPTED"
    elif dialogue_type in (3, 5):
        addressee_hint = "PLAYER_LIKELY"
    elif dialogue_type in (2, 4, 6):
        addressee_hint = "SITUATIONAL_TARGET"
    else:
        addressee_hint = "UNKNOWN"

    return {
        "dialogue_type": dialogue_type,
        "dialogue_type_name": name,
        "addressee_hint": addressee_hint,
    }
