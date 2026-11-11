# Changelog

## 4.2.0

- French tells now draw on [ferr079/humanizer-fr](https://github.com/ferr079/humanizer-fr) (MIT). Its license notice is in `THIRD_PARTY_NOTICES.md`.
- New section G in `references/french.md` and in SKILL.md: §27 too many connectors, §28 calques from English, §29 empty verbs and phrases. Connectors and calques moved there from §7 and §12.
- Longer "À repérer" lists for §1 to §25 in French, for example "ne se contente pas de", "Tout est dit.", "il se pourrait que", "ouvre la voie à", "Vous avez tout à fait raison".
- New nuances in French: passive voice and "on" are a tell only when systematic (§11). A vague link stays vague if the source gives no relation (§14). A missing source alone is not a tell (§17).
- New French "Quand ne pas agir" list, and new plain words (délivrer, supporter, opportunité, digital, se veut).
- `ste_check.py` flags the new French phrases, calques and empty verbs. It flags a paragraph where most sentences start with a connector (rule `connectors`). English results do not change.

## 4.1.0

- French support. SKILL.md has a new section "French text": the French phrases for Pass 1, the S-rules that change in French, and a third pass for French typography (T1 to T12).
- New `references/french.md`, written in French: the 26 tells with French phrases and examples, the S-rules for French, a list of plain words and a full example.
- New `references/french-typography.md`, written in French: spaces and punctuation, quotation marks, capitals, numbers, units, dates, abbreviations, dashes, lists, ligatures and italics. It also says which rule wins when typography and the other passes disagree.
- `ste_check.py` finds the language (`--lang auto`, `en` or `fr`). In French it flags French tells, French stock words, possible passive voice and typography errors. The limits for sentence length have 5 words of slack in French at 80%.
- `ste_check.py --fix-spaces` writes the no-break spaces of French typography into a file. It leaves code, URLs and front matter alone.
- New eval case: `humanize-french-article`.

## 4.0.0

- SKILL.md is now 217 lines instead of 573, and about 2,650 words instead of 6,250. Pass 1 and Pass 2 are compact tables with one example per group.
- The full entries for the 26 AI tells moved to `references/ai-tells.md`. The worked example moved to `references/worked-example.md`.
- AGENTS.md now sets a limit of 500 lines for SKILL.md.

## 3.2.1

- LICENSE is now a plain MIT license. The blader/humanizer MIT notice moved to `THIRD_PARTY_NOTICES.md`.

## 3.2.0

- Cut SKILL.md down to what the model needs. The story of Karpathy's post, the note about the graphic and the sources moved out. They are in the README.
- Fixed a sentence in the README that had an AI tell.

## 3.1.0

- Renamed from `humanizer-ste80` to `ste80-humanizer` ("STE80 Humanizer"). Install with `npx skills add Dodaios/ste80-humanizer`. The slash command is now `/ste80-humanizer`.

## 3.0.0

- Rewrote SKILL.md from top to bottom for readability.
- New section "How to read this skill": two passes, §1 to §26 for AI tells, S1 to S15 for structure, the same fields in every entry.
- New section "The method": Karpathy's full tip, the ladder from writing to diagrams, HTML and video, why STE works on LLMs, a table of what 100% and 80% mean, and a note on errors in the graphic that came with his post.
- Pass 1 now covers all 26 patterns of blader/humanizer in the same order (adds hyphenated pairs, vague association, repeated heading, borrowed authority with prestige lists, and others), each with Watch for, Problem, and new Before/After examples. The MIT notice of blader/humanizer is in LICENSE.
- Pass 2 has 15 S-rules, each with 80% and Strict levels and examples.
- New worked example that shows the text after Pass 1 and after Pass 2.
- Return formats now include file mode, embedded mode and review mode.

## 2.0.0

- Renamed from `ste80` to `humanizer-ste80`. The skill is now a general humanizer that uses STE80 as its method.
- New Part 1: 23 AI tells in five groups (staging, rhythm, inflation, formatting, chat residue), inspired by Wikipedia's "Signs of AI writing" and blader/humanizer.
- Part 2: the 23 STE80 structure rules, now in compact form. The full rules with before and after examples moved to `references/ste80-rules.md`.
- New modes: Humanize (default), Light, Strict STE.
- New sections: Voice (match a writing sample), "Human quirks" to keep, contradiction flag in the fidelity rules.
- `ste_check.py` now also flags AI tells: not-X-but-Y, chatbot openers and closers, run-ups, fake depth, stacked hedges, vague authority, "-ing" riders, inflated significance and curly quotes.
- New eval case: `humanize-linkedin-post`.

## 1.0.0

- First release.
- 80% mode (default) and strict mode.
- 23 rules in six groups (sentences, verbs, words, structure, punctuation, what 80% relaxes), with before and after examples.
- Fidelity rules: keep every fact, keep uncertainty at its strength, add nothing.
- `references/word-swaps.md`: plain alternatives in ten groups, including typical LLM vocabulary.
- `references/strict-mode.md`: paraphrased ASD-STE100 Issue 9 rule sections and a final checklist.
- `scripts/ste_check.py`: dependency-free heuristic linter.
