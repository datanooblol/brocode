from rapidfuzz import fuzz

SKILLS = [
    {
        "name": "pdf-summarize",
        "description": "Summarizes long PDF documents into key points",
        "tag": ["pdf", "document"],
        "keywords": ["tldr", "condense", "executive summary", "shrink report"],
    },
    {
        "name": "k8s-deploy",
        "description": "Deploys a manifest to a Kubernetes cluster",
        "tag": ["cloud", "devops", "kubernetes"],
        "keywords": ["k8s", "helm apply", "rollout", "ship to prod"],
    },
    {
        "name": "file-editor",
        "description": "Reads and patches files on disk",
        "tag": ["file", "code"],
        "keywords": ["edit code", "write file", "patch"],
    },
]


def searchable_fields(skill: dict) -> list[tuple[str, str]]:
    fields = [(skill["name"], "name"), (skill["description"], "description")]
    fields += [(kw, "keyword") for kw in skill.get("keywords", [])]
    fields += [(t, "tag") for t in skill.get("tag", [])]
    return fields


def search(query: str, skills: list[dict], limit: int = 5, threshold: float = 60.0):
    results = []
    for skill in skills:
        best_score, best_field, best_value = 0.0, None, None
        for value, label in searchable_fields(skill):
            score = fuzz.partial_ratio(query.lower(), value.lower())
            if score > best_score:
                best_score, best_field, best_value = score, label, value
        if best_score >= threshold:
            results.append({
                "name": skill["name"],
                "score": round(best_score, 1),
                "matched_field": best_field,
                "matched_value": best_value,
            })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:limit]


if __name__ == "__main__":
    for query in ["shrink report", "helm apply", "edit a file", "kubernetes"]:
        print(f"\nquery: {query!r}")
        for r in search(query, SKILLS):
            print(f"  {r['name']:15} score={r['score']:<5} matched via {r['matched_field']} = {r['matched_value']!r}")
