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

## Requirements

- **Python 3** (check with `python --version`; `python3` on Linux/macOS)
- **Claude Code** (terminal, desktop app or IDE extension)
- **Gemini inside Antigravity IDE**
- Both working in the same project folder

## Setup (step by step)

1. **Download.** On GitHub use the green **Code → Download ZIP**, or:
   ```
   git clone https://github.com/digi500/foreveryoung.git
   ```
2. **Copy the `kopru2` folder to a permanent place**, e.g. `C:\kopru`. Don't move it afterwards: setup writes the scripts' full path into your project. If you move it, run setup again.
3. **Install into your project** (in a terminal):
   ```
   python C:\kopru\kur.py C:\project_folder
   ```
   You'll see `Köprü kuruldu` ("bridge installed") and a list of what was done. Safe to re-run.
4. **Reopen Claude Code in that project folder.** The hook only takes effect in a new session.
5. **Start a new chat in Antigravity** and tell Gemini:
   > Read `GEMINI.md` and `bilgi.md` in the bridge folder.

## How do I know it works?

1. Ask Gemini something and let it answer.
2. Send Claude any message. Claude will see Gemini's reply under the header **"[Gemini'nin son kontrolden bu yana yazdığı yeni cevaplar]"** ("Gemini's new replies since the last check").
3. Try the reverse: let Claude write something, then message Gemini. Gemini runs the command on every message and reads Claude's new reply.

The first run does not replay old conversation; only replies written after setup are passed on.

## Daily use

1. Tell Claude what you want. Claude writes the task into `.ortak/gorevler.md`.
2. Tell Gemini: "do the task in `.ortak/gorevler.md`, write your report to `.ortak/rapor.md`".
3. Tell Claude "check it". Claude verifies the report against real files and outputs and writes corrections to `.ortak/kontrol.md`.
4. Commit, push and release decisions stay with you.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Claude doesn't show Gemini's replies | Reopen Claude Code in the project folder. Check `.claude/settings.json` contains the `son_mesajlar.py` line. |
| Gemini doesn't read Claude | Start a new chat in Antigravity and say "read GEMINI.md". |
| `python` not found | Install Python 3. Linux/macOS use `python3`. |
| I moved the bridge folder | Run `kur.py` again from the new place. Remove the old hook line from `.claude/settings.json` and the old rule from `GEMINI.md`. |

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
