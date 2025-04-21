import difflib

def check_plagiarism_advanced(text):
    # Simulează surse reale
    results = []
    if "inteligență artificială" in text.lower():
        results.append({
            "sursa": "Wikipedia",
            "scor": 65.2,
            "link": "https://ro.wikipedia.org/wiki/Inteligența_artificială"
        })
        results.append({
            "sursa": "arXiv",
            "scor": 48.7,
            "link": "https://arxiv.org/abs/2304.09999"
        })
    return results