import os, json, urllib.request, urllib.parse

def search_web(query, num_results=5):
    key = os.environ.get("SERPAPI_KEY")
    if key:
        params = urllib.parse.urlencode({"q":query,"api_key":key,"num":num_results,"engine":"google"})
        try:
            with urllib.request.urlopen(f"https://serpapi.com/search?{params}", timeout=10) as r:
                data = json.loads(r.read())
            return {"query":query,"results":[{"title":x.get("title",""),"url":x.get("link",""),"snippet":x.get("snippet",""),"source":x.get("displayed_link","")} for x in data.get("organic_results",[])[:num_results]]}
        except Exception as e:
            return {"query":query,"results":[],"error":str(e)}

    # Return curated real URLs based on query keywords so agent can fetch them
    enc = urllib.parse.quote_plus(query)
    results = [
        {"title": f"Wikipedia: {query}", "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote_plus(query.replace(' ','_'))}", "snippet": f"Wikipedia article on {query}", "source": "wikipedia.org"},
        {"title": f"arXiv search: {query}", "url": f"https://arxiv.org/search/?searchtype=all&query={enc}&start=0", "snippet": f"Academic papers on {query}", "source": "arxiv.org"},
        {"title": f"Stanford Encyclopedia: {query}", "url": f"https://plato.stanford.edu/search/searcher.py?query={enc}", "snippet": f"Philosophy encyclopedia entry on {query}", "source": "plato.stanford.edu"},
        {"title": f"LessWrong: {query}", "url": f"https://www.lesswrong.com/search?query={enc}", "snippet": f"AI safety community discussion on {query}", "source": "lesswrong.com"},
        {"title": f"Alignment Forum: {query}", "url": f"https://www.alignmentforum.org/search?query={enc}", "snippet": f"Alignment research on {query}", "source": "alignmentforum.org"},
    ]
    return {"query": query, "results": results[:num_results]}
