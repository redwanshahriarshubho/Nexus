from collections import defaultdict

def cluster_findings(findings, num_clusters=3):
    if not findings:
        return {"clusters":{},"num_clusters":0}
    num_clusters = min(num_clusters, len(findings))
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        vec = TfidfVectorizer(stop_words="english", max_features=500)
        X = vec.fit_transform(findings)
        km = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        labels = km.fit_predict(X)
        names = vec.get_feature_names_out()
        cluster_labels = {i:" / ".join(names[km.cluster_centers_[i].argsort()[-3:][::-1]]).title() for i in range(num_clusters)}
        clusters = defaultdict(list)
        for i,f in enumerate(findings):
            clusters[cluster_labels[labels[i]]].append(f)
        return {"clusters":dict(clusters),"method":"tfidf-kmeans"}
    except ImportError:
        clusters = defaultdict(list)
        for i,f in enumerate(findings):
            clusters[f"Theme {(i % num_clusters)+1}"].append(f)
        return {"clusters":dict(clusters),"method":"fallback"}
