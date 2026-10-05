# AI-to-AI Local Orchestration Bridge

[ 🇹🇷 Türkçe Sürümü Oku (Read in Turkish) → ](README.md)

---

This directory contains the lightweight orchestration script that enables two distinct local AI assistants (e.g., Gemini and Claude) to sequentially review and evaluate each other's outputs without costly API streaming loops or polling overhead.

---

## How It Works

1. Neither model stays in an active polling loop (zero wasted idle compute or API tokens).
2. When an AI generates a response, it writes into its local session transcript.
3. When the user prompts the peer model, a lightweight Python script (`son_mesajlar.py`) triggers:
   - Reads only new assistant responses generated since the last checkpoint.
   - Outputs nothing if no new response exists (zero token consumption).
   - Injects the latest peer response into context only when fresh content is available.

---

## Configuration & Environment Variables

The script locates transcript logs using customizable glob path patterns. These can be defined via environment variables or CLI arguments:

* `CLAUDE_LOG_PATTERN`: Path pattern for Claude's project session transcripts.  
  *Example:* `~/.claude/projects/<project-name>/*.jsonl`
* `GEMINI_LOG_PATTERN`: Path pattern for Gemini's session logs.  
  *Example:* `~/<assistant-dir>/logs/transcript.jsonl`

If environment variables are omitted, you can pass the pattern directly as a CLI argument:
```bash
python son_mesajlar.py claude "~/.claude/projects/example-project/*.jsonl"
```

---

## Integration Examples

### 1. Claude Integration (User Prompt Hook)
In your workspace `.claude/settings.json`, add a `UserPromptSubmit` hook:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "python .ortak/son_mesajlar.py gemini"
      }
    ]
  }
}
```

### 2. Gemini Integration (Project Rule)
In your workspace `GEMINI.md` file, define the rule:

```markdown
# Claude Collaboration Rule
Before answering each user prompt, execute:
python .ortak/son_mesajlar.py claude
- If the command produces no output, proceed normally.
- If output is returned, incorporate Claude's latest thesis into your response.
```

---

## License
The bridge script and utilities are licensed under the [MIT License](LICENSE).
