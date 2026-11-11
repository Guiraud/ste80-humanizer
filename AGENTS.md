# Guide for agents

This repo is one agent skill, `ste80-humanizer`. `SKILL.md` at the root is the skill. Pass 1 lists the 26 AI tells in a table (§1 to §26, same order as blader/humanizer). Pass 2 lists the STE80 structure rules (S1 to S15). The section "French text" adds the French phrases and the French typography rules (T1 to T12). Follow these rules when you change it.

- **Write in the style the skill teaches.** Short sentences, active voice, simple tenses, one term per thing.
- **Keep the version in sync** in four places: `SKILL.md` (`metadata.version`), the first heading in `CHANGELOG.md`, `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`.
- **Keep SKILL.md under 500 lines** (Anthropic's limit) and about 3,000 words. SKILL.md holds compact tables. Full entries, long examples and anything for human readers go in `references/` or the README.
- **Keep the entry format in `references/ai-tells.md`:** Watch for, Problem, Before, After.
- **Keep LICENSE a plain MIT license.** Keep the blader/humanizer MIT notice in `THIRD_PARTY_NOTICES.md` as long as Pass 1 follows its catalog. Keep the ferr079/humanizer-fr notice there as long as `references/french.md` uses its section G.
- **Keep SKILL.md and README.md in sync** when you add, remove or rename a tell or a rule. Keep `references/ste80-rules.md` mapped to the S-rules.
- **Write the French references in French.** `references/french.md` and `references/french-typography.md` use the same style: short sentences, active voice, no semicolons, no dashes for asides. They follow their own typography rules. After you change them, run `python scripts/ste_check.py --fix-spaces references/french.md references/french-typography.md`. Put an example of wrong typography in backticks, so the command does not correct it.
- **Keep the French section in sync** with the two French references and with the README when you add, remove or rename a T-rule or a French tell.
- **Keep `scripts/ste_check.py` in sync** with the tells and words in SKILL.md and in `references/french.md` where a regex can find them. Do not change what the checker reports for English text when you work on French.
- **Do not copy the ASD-STE100 specification or dictionary.** ASD owns the copyright. Paraphrase rules in your own words. Cite only single word pairs.
- **Do not claim compliance.** The skill and the checker give "STE style", not certified STE.
- **Before you publish**, run:

```bash
python scripts/ste_check.py --help
npx skills add . --list
claude plugin validate .
```
