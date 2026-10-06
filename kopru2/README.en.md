# Bridge 2 — Claude ↔ Gemini Collaboration System

[ 🇹🇷 Türkçe Sürümü Oku (Read in Turkish) → ](README.md)

---

The first version ([`kopru/`](../kopru/)) let two AI assistants read each other's replies. **Bridge 2** turns that into a working setup: one command installs it into any project, roles and rules are defined, and tasks and reports live in shared files.

## What changed from version 1

| | Bridge 1 | Bridge 2 |
|---|---|---|
| Setup | Manual (copy hook and rule) | `python kur.py <project>`, one command, safe to re-run |
| Script | One copy per project | One shared copy for all projects |
| Log path | Passed via environment variable | Found automatically from the project path (Claude and Gemini/Antigravity) |
| Read state | One file next to the script | Per project, in `.ortak/durum_*.json` |
| Roles and rules | None | `bilgi.md`: manager/reviewer, worker, decision maker; no fake data, secrets never printed |
| Task flow | None | `.ortak/gorevler.md` (tasks) → `rapor.md` (report) → `kontrol.md` (review) |

## Setup

1. Copy this folder to your machine (e.g. `C:\kopru`).
2. Install into a project:
   ```
   python C:\kopru\kur.py C:\project_folder
   ```
3. Reopen the Claude Code session. In Gemini, start a new chat or say "read GEMINI.md".

`kur.py` does the following:
- Creates `<project>/.ortak/` with `gorevler.md`, `rapor.md`, `kontrol.md`.
- Adds a `UserPromptSubmit` hook to `<project>/.claude/settings.json` that brings Gemini's new replies into every user message.
- Adds a rule to `<project>/GEMINI.md` telling Gemini to read Claude's new replies on every message.
- Adds these local files to `.gitignore`.

## How it works

- `son_mesajlar.py gemini|claude [project]`: prints the other side's replies written since the last check. Prints nothing if there is nothing new (zero tokens).
- Claude logs: `~/.claude/projects/<project path>/*.jsonl`
- Gemini (Antigravity) logs: `~/.gemini/antigravity-ide/brain/*/.system_generated/logs/transcript.jsonl`. These are not split per project, so the script picks the first of the 15 newest sessions that mentions the project path.
- At most 4,500 characters per reply and 9,000 per run are passed on.

Full working rules (in Turkish): [`bilgi.md`](bilgi.md)

## Notes

- Paths are shown with Windows examples. The scripts also run on Linux and macOS.
- The Gemini log path targets Antigravity IDE. For another client, change `GEMINI_KAYITLARI` in `son_mesajlar.py`.

## License

[MIT License](LICENSE)
