# Bethesda Localization QA

Reusable QA utilities for Korean localization of Bethesda games and large Bethesda-engine mods.

The project started from the Oblivion Korean v2 translation pipeline, but the core rules are designed to be reusable for Fallout 4, Fallout London, Sim Settlements 2, and other projects.

## Goals

- Lock proper nouns and approved terminology before machine translation.
- Restore Korean particles locally instead of asking an LLM to guess 을/를, 이/가, 은/는, 과/와, 으로/로.
- Preserve markup, line breaks, page breaks, and printf-style placeholders.
- Detect semantic drift, missing locked terms, malformed tokens, and suspiciously compressed translations.
- Track dialogue register by speaker and likely addressee.
- Review character voice, sarcasm, wordplay, and relationship-dependent speech levels separately from literal correctness.
- Keep game-specific record parsing in adapters so the QA engine stays reusable.

## Layout

```
src/bethesda_localization_qa/
  locked_terms.py        # proper-name locking, Korean particle resolution, format-token protection
  dialogue_style.py      # speech-level classification and speaker/style metadata helpers

adapters/
  oblivion/              # TES4 INFO/DIAL speaker and dialogue-context extraction

docs/
  PIPELINE.md            # recommended translation + QA pipeline

tests/
  test_locked_terms.py
```

## Design rule

Game data and project terminology must stay outside the generic engine.

For example:

- `Vitharn -> 비탄` is project data.
- "lock approved proper nouns before translation" is a reusable engine rule.

This separation is what allows the same QA code to be reused later for Fallout London or Sim Settlements 2 without leaking Oblivion terminology into another project.

## Status

Early v0.1 extraction from the Oblivion Korean v2 workflow. APIs and CSV schemas may still change while the first adapter is generalized.
