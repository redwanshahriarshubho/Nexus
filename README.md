
<div align="center">

# ⚡ Nexus

### Autonomous Research Digest Agent

*Give it a topic. Get a cited research digest.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Hermes](https://img.shields.io/badge/Powered_by-Hermes_Agent-7C3AED?style=for-the-badge)](https://hermes-agent.nousresearch.com)
[![OpenRouter](https://img.shields.io/badge/API-OpenRouter-FF6B35?style=for-the-badge)](https://openrouter.ai)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![DEV Challenge](https://img.shields.io/badge/DEV-Hermes_Agent_Challenge-000000?style=for-the-badge&logo=devdotto)](https://dev.to/challenges/hermes-agent-2026-05-15)

</div>

---

## What is Nexus?

Nexus is an **autonomous research digest agent** built for the [Hermes Agent Challenge](https://dev.to/challenges/hermes-agent-2026-05-15) by Nous Research × DEV Community.

You give it one topic. Nexus plans a search strategy, reads real sources, clusters findings into themes, and generates a **beautiful HTML digest** with citations and a "what to read next" queue — completely autonomously. No hand-holding. No prompting for each step.

---

## Demo

```bash
$ python main.py "AI safety and alignment"

⚡ Nexus Research Digest
   Topic : AI safety and alignment
   Date  : 2026-05-30
   Model : openrouter/auto

[step 1] Thinking...
  Tool: search_web
  Tool: search_web
[step 2] Thinking...
  Tool: fetch_url
  Tool: fetch_url
[step 3] Thinking...
  Tool: cluster_findings
[step 4] Thinking...
  Tool: save_digest
  ✅ Digest saved!

✅ Done! Check the output/ folder.
```

---

## How It Works

```
You type a topic
       │
       ▼
┌─────────────────────────────────┐
│        Hermes Agent Loop        │
│                                 │
│  1. PLAN   → search strategy    │
│  2. SEARCH → search_web ×2-3    │
│  3. READ   → fetch_url ×2-3     │
│  4. CLUSTER→ cluster_findings   │
│  5. SAVE   → save_digest        │
└─────────────────────────────────┘
       │
       ▼
  output/
  ├── digest.html  ← open in browser
  └── digest.json  ← structured data
```

Each step is a **real tool call** — Hermes decides when to call what, in what order, with what arguments. The agent plans before it acts and always finishes by saving the digest.

---

## Quick Start

```bash
# Clone
git clone https://github.com/redwanshahriarshubho/Nexus.git
cd Nexus

# Install
pip install -r requirements.txt

# Try the demo — no API key needed
python main.py --demo

# Run for real (get a free key at openrouter.ai)
export HERMES_API_KEY="your-key"
python main.py "quantum computing breakthroughs"
```

### Windows (PowerShell)

```powershell
$env:HERMES_API_KEY="your-key"
$env:HERMES_MODEL="openrouter/auto"
python main.py "your topic here"
```

---

## Agentic Capabilities

| Capability | How Nexus uses it |
|---|---|
| **Multi-step planning** | Decides which queries to run before searching |
| **Tool use** | Calls `search_web`, `fetch_url`, `cluster_findings`, `save_digest` |
| **Autonomous completion** | Runs up to 20 steps, self-corrects, always saves |
| **Structured output** | JSON + HTML with citations, themes, read-next queue |

---

## Project Structure

```
Nexus/
├── main.py                  # CLI entrypoint
├── agent/
│   └── digest_agent.py      # Hermes agent loop
├── tools/
│   ├── search.py            # search_web tool
│   ├── fetch.py             # fetch_url tool
│   ├── cluster.py           # cluster_findings tool
│   └── persist.py           # save_digest + HTML renderer
├── output/                  # Generated digests
└── requirements.txt
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `HERMES_API_KEY` | — | OpenRouter API key **(required)** |
| `HERMES_MODEL` | `openrouter/auto` | Model to use |
| `HERMES_BASE_URL` | `https://openrouter.ai/api/v1` | API endpoint |
| `SERPAPI_KEY` | — | Optional: richer search results |

---

## Output

Every run saves two files to `output/`:

| File | Description |
|---|---|
| `YYYY-MM-DD_topic.html` | Beautiful digest — open in any browser |
| `YYYY-MM-DD_topic.json` | Structured data — pipe into other tools |

---

## Built With

- [Hermes Agent](https://hermes-agent.nousresearch.com) — Nous Research's open-source agentic system
- [OpenRouter](https://openrouter.ai) — Multi-model API gateway  
- Python — `urllib`, `json`, `re`, `html` + `openai` + `scikit-learn`

---

## License

MIT — do whatever you want with it.

---

<div align="center">

Built by **Redwan** for the [Hermes Agent Challenge](https://dev.to/challenges/hermes-agent-2026-05-15)

*⚡ Nexus — Research at the speed of thought*

</div>



