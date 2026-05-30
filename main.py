#!/usr/bin/env python3
import argparse, json, os, sys
from datetime import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Nexus Research Digest Agent")
    parser.add_argument("topic", nargs="?")
    parser.add_argument("--topic", "-t", dest="topic_flag")
    parser.add_argument("--date", "-d", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        _list_digests(); return
    if args.demo:
        _run_demo(); return

    topic = args.topic or args.topic_flag
    if not topic:
        parser.print_help(); sys.exit(1)

    if not os.environ.get("HERMES_API_KEY"):
        print("HERMES_API_KEY not set. Run: python main.py --demo to test first.")
        sys.exit(1)

    from agent.digest_agent import run_digest_agent
    run_digest_agent(topic, args.date)
    print("\nDone! Check the output/ folder.")

def _run_demo():
    from tools.persist import save_digest
    print("Running Nexus demo...\n")
    demo = {
        "topic": "AI Agents and Multi-Step Reasoning",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": "Recent research on AI agents shows rapid progress in multi-step reasoning, tool use, and autonomous planning. Open-source models are closing the gap with proprietary systems on complex reasoning tasks.",
        "key_findings": [
            "Chain-of-thought prompting improves task success rates by 40-60%",
            "Tool-augmented agents outperform text-only agents on retrieval tasks",
            "Self-reflection loops significantly reduce agent failure cascades",
            "Open-source models now match GPT-4 on several agentic benchmarks",
        ],
        "themes": [
            {"name": "Reasoning & Planning", "findings": ["Tree-of-thought enables backtracking and plan revision", "Hierarchical planning decomposes complex goals into sub-tasks"]},
            {"name": "Tool Use & Grounding", "findings": ["Web search integration improves factual accuracy", "Code execution lets agents verify mathematical claims"]},
            {"name": "Open-Source Progress", "findings": ["Hermes 3 shows strong function-calling performance", "Community benchmarks drive rapid model iteration"]},
        ],
        "citations": [
            {"title": "ReAct: Synergizing Reasoning and Acting in LLMs", "url": "https://arxiv.org/abs/2210.03629", "source": "arXiv", "snippet": "Combines chain-of-thought reasoning with action execution."},
            {"title": "Hermes Agent by Nous Research", "url": "https://github.com/NousResearch/hermes-agent", "source": "GitHub", "snippet": "Open-source agent with built-in learning loop and skill creation."},
        ],
        "read_next": [
            {"title": "AgentBench: Evaluating LLMs as Agents", "url": "https://arxiv.org/abs/2308.03688", "reason": "The definitive benchmark paper for agentic evaluation"},
            {"title": "Nous Research Blog", "url": "https://nousresearch.com", "reason": "Latest updates on Hermes models"},
        ],
    }
    result = save_digest(demo)
    print(f"\nDone! Open this file in your browser:\n  {result['html_path']}")

def _list_digests():
    files = sorted(Path("output").glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        print("No digests yet. Run: python main.py --demo")
        return
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        print(f"  {d.get('date')} — {d.get('topic')}")

if __name__ == "__main__":
    main()
