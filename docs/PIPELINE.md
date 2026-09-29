# Recommended QA pipeline

The framework separates translation correctness from game-specific context.

1. **Extract source records**
   - Keep FormIDs, parent dialogue/topic IDs, quest/scene IDs, and surrounding dialogue.
   - Never translate internal identifiers, script names, paths, or editor IDs.

2. **Resolve approved terminology**
   - Build a project glossary outside the engine.
   - Mark terms that must be locked inside larger strings.
   - Keep exact whole-source replacements separate from contextual phrase locks.

3. **Protect immutable content**
   - Replace approved proper nouns with `__PN###__`.
   - Replace markup, newlines, page breaks, and printf placeholders with `__FMT###__`.
   - Restore all protected material locally after model output.

4. **Attach dialogue context**
   - Resolve speaker when the game data supports it.
   - Add likely addressee/context type.
   - Attach a character style profile only when identity is sufficiently certain.
   - Treat ambiguous speaker sets as shared-register lines rather than inventing a unique voice.

5. **Translate**
   - Require natural Korean rather than English word-order imitation.
   - Preserve jokes, sarcasm, emotional shifts, and wordplay function.
   - Use historical translations only as terminology or speech-level evidence unless a project explicitly chooses reuse.

6. **Automated QA**
   - Token count/order validation.
   - Markup/newline/placeholder round-trip validation.
   - Locked terminology validation.
   - Korean particle resolution.
   - Semantic-compression and suspicious-duplicate checks.
   - Dialogue tone classification.

7. **Character voice review**
   - Group by speaker + likely addressee/context.
   - Flag unexplained switching between 합니다체, 해요체, and 반말.
   - Review major recurring characters as a complete corpus.

8. **Wordplay review**
   - Keep a separate candidate list for puns, idioms, irony, insults, titles used as jokes, and meaning-bearing names.
   - A technically correct locked-term translation is not automatically a good wordplay translation.

9. **Human/Sol review**
   - Compare against the English source.
   - Use machine output as a draft, not final authority.
   - Record intentional exceptions so later reruns do not undo them.

## Reuse across games

The core package should remain game-neutral. Add a new adapter when record relationships differ:

- Oblivion: INFO + CTDA/GetIsID + DIAL type.
- Fallout 4 / Fallout London / Sim Settlements 2: INFO/DIAL plus Quest Alias, Scene, Voice Type, Actor, faction/rank, and relationship resolution.

Project-specific names, terminology, aliases, and character profiles belong in project data, not in the shared engine.
