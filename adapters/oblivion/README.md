# Oblivion adapter

This adapter contains TES4-specific record interpretation only.

It deliberately does **not** contain project terminology or character profiles.

Current rules:

- `INFO/CTDA GetIsID` can identify a single explicit NPC speaker or a set of NPCs sharing a line.
- `DIAL/DATA` is classified into Topic, Conversation, Combat, Persuasion, Detection, Service, and Misc.
- Dialogue type produces an **addressee hint**, not an absolute addressee claim.

The binary parser itself is intentionally left outside the generic package. Feed parsed CTDA payloads and NPC lookups into the adapter. This lets projects use xEdit exports, a custom parser, or another extraction layer without changing the QA core.
