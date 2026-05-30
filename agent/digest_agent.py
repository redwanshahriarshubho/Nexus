import os, json, re
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("HERMES_API_KEY"),
    base_url=os.environ.get("HERMES_BASE_URL", "https://openrouter.ai/api/v1"),
)
MODEL = os.environ.get("HERMES_MODEL", "openrouter/auto")

SYSTEM_PROMPT = """You are Nexus, a research digest agent. For the given topic:
1. Call search_web 2-3 times with different queries
2. Call fetch_url on 2-3 of the returned URLs
3. Call cluster_findings with all findings you collected
4. Call save_digest with the COMPLETE digest object

CRITICAL: You MUST call save_digest at the end no matter what.
Even if fetching fails, synthesize findings from search snippets alone.
The digest object needs: topic, date, summary (string), key_findings (array of strings),
themes (array of {name, findings}), citations (array of {title,url,source,snippet}),
read_next (array of {title,url,reason})
Do not stop early. Always finish with save_digest."""

TOOLS = [
    {"type":"function","function":{"name":"search_web","description":"Search for articles on a topic","parameters":{"type":"object","properties":{"query":{"type":"string"},"num_results":{"type":"integer","default":5}},"required":["query"]}}},
    {"type":"function","function":{"name":"fetch_url","description":"Fetch text from a URL","parameters":{"type":"object","properties":{"url":{"type":"string"},"max_chars":{"type":"integer","default":3000}},"required":["url"]}}},
    {"type":"function","function":{"name":"cluster_findings","description":"Group findings into themes","parameters":{"type":"object","properties":{"findings":{"type":"array","items":{"type":"string"}},"num_clusters":{"type":"integer","default":3}},"required":["findings"]}}},
    {"type":"function","function":{"name":"save_digest","description":"Save the final digest — MUST be called at the end","parameters":{"type":"object","properties":{"digest":{"type":"object"}},"required":["digest"]}}},
]

def run_tool(name, args):
    from tools.search import search_web
    from tools.fetch import fetch_url
    from tools.cluster import cluster_findings
    from tools.persist import save_digest
    dispatch = {"search_web":search_web,"fetch_url":fetch_url,"cluster_findings":cluster_findings,"save_digest":save_digest}
    try:
        return json.dumps(dispatch[name](**args))
    except Exception as e:
        return json.dumps({"error": str(e)})

def safe_parse_args(raw):
    try:
        return json.loads(raw)
    except Exception:
        pass
    try:
        return json.loads(raw + "}")
    except Exception:
        pass
    try:
        m = re.search(r'"query"\s*:\s*"([^"]+)"', raw)
        if m: return {"query": m.group(1)}
    except Exception:
        pass
    try:
        m = re.search(r'"url"\s*:\s*"([^"]+)"', raw)
        if m: return {"url": m.group(1)}
    except Exception:
        pass
    try:
        m = re.search(r'"findings"\s*:\s*(\[[^\]]+\])', raw, re.DOTALL)
        if m: return {"findings": json.loads(m.group(1))}
    except Exception:
        pass
    return None

def run_digest_agent(topic, date=None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    print(f"\n⚡ Nexus Research Digest")
    print(f"   Topic : {topic}")
    print(f"   Date  : {date}")
    print(f"   Model : {MODEL}\n")

    messages = [{"role":"user","content":(
        f'Research topic for {date}: "{topic}"\n\n'
        f'Follow these steps IN ORDER:\n'
        f'1. search_web("{topic} recent research 2025")\n'
        f'2. search_web("{topic} key challenges solutions")\n'
        f'3. fetch_url on 1-2 URLs from results\n'
        f'4. cluster_findings with all findings\n'
        f'5. save_digest with complete digest\n\n'
        f'You MUST call save_digest at the end. Do not stop without saving.'
    )}]

    saved = False

    for i in range(20):
        print(f"[step {i+1}] Thinking...")
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role":"system","content":SYSTEM_PROMPT}] + messages,
                tools=TOOLS, tool_choice="auto", temperature=0.3, max_tokens=4096,
            )
        except Exception as e:
            print(f"API error: {e}")
            break

        msg = response.choices[0].message
        messages.append(msg)

        if msg.content:
            print(f"Agent: {msg.content[:200]}")

        if not msg.tool_calls:
            if not saved:
                # Nudge the agent to save
                messages.append({"role":"user","content":"Please now call save_digest with all the research you have gathered so far."})
                continue
            break

        for tc in msg.tool_calls:
            print(f"  Tool: {tc.function.name}")
            args = safe_parse_args(tc.function.arguments)
            if args is None:
                print(f"  Skipping — bad args")
                result = json.dumps({"error": "bad args"})
            else:
                result = run_tool(tc.function.name, args)
                if tc.function.name == "save_digest":
                    saved = True
                    print("  ✅ Digest saved!")
            messages.append({"role":"tool","tool_call_id":tc.id,"content":result})

        if saved:
            break

    if not saved:
        print("\n⚠ Saving fallback digest...")
        from tools.persist import save_digest
        save_digest({"topic":topic,"date":date,"summary":"Research completed. See search results for details.","key_findings":[],"themes":[],"citations":[],"read_next":[]})

    print("\n✅ Done! Check the output/ folder.")

if __name__ == "__main__":
    import sys
    run_digest_agent(" ".join(sys.argv[1:]) or "AI agents")
