import urllib.request, urllib.error, re, html

def fetch_url(url, max_chars=4000):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Nexus/1.0","Accept":"text/html,*/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
        text = raw.decode("utf-8", errors="replace")
        cleaned = _clean(text)
        return {"url":url,"content":cleaned[:max_chars],"truncated":len(cleaned)>max_chars}
    except Exception as e:
        return {"url":url,"content":"","error":str(e)}

def _clean(t):
    t = re.sub(r"<script[^>]*>.*?</script>","",t,flags=re.DOTALL|re.IGNORECASE)
    t = re.sub(r"<style[^>]*>.*?</style>","",t,flags=re.DOTALL|re.IGNORECASE)
    t = re.sub(r"<(?:p|div|br|li|h[1-6])[^>]*>","\n",t,flags=re.IGNORECASE)
    t = re.sub(r"<[^>]+>"," ",t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+"," ",t)
    t = re.sub(r"\n{3,}","\n\n",t)
    return t.strip()
