# Adeel Rehman

import requests
from difflib import SequenceMatcher

API_KEY = "835e964336fa4f1cbc0caf170a19d613"

def clean_text(text):
    """Clean text for comparison"""
    return text.lower().replace(",", "").replace("!", "").replace(".", "").replace("?", "")

def fuzzy_similarity(a, b):
    return SequenceMatcher(None, clean_text(a), clean_text(b)).ratio()

def keyword_score(a, b):
    a_words = set(clean_text(a).split())
    b_words = set(clean_text(b).split())
    common = a_words & b_words
    
    if len(a_words) == 0:
        return 0
    return len(common) / len(a_words)

def get_similarity(a, b):
    """Combine fuzzy + keyword scores"""
    fuzzy = fuzzy_similarity(a, b)
    keyword = keyword_score(a, b)
    return (0.6 * keyword) + (0.4 * fuzzy)

def fetch_newsapi_headlines(user_headline):
    """Fetch headlines from NewsAPI"""
    
    keywords = " ".join(user_headline.split()[:4])
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keywords,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10,
        "apiKey": API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") != "ok":
            return []
        
        articles = data.get("articles", [])
        return [a["title"] for a in articles if a.get("title")]
    except:
        return []

def check_newsapi(headline):
    """Main function for NewsAPI verification"""
    
    print("\n🌐 Checking NewsAPI (50,000+ sources)...")
    
    api_headlines = fetch_newsapi_headlines(headline)
    
    if not api_headlines:
        return {
            'found': False,
            'total_sources': 0,
            'sources': []
        }
    
    # Find matches with threshold 40%
    matches = []
    for title in api_headlines:
        score = get_similarity(headline, title)
        if score >= 0.4:
            matches.append(title)
    
    # Extract source names
    sources = []
    for title in matches[:5]:
        if '-' in title:
            source = title.split('-')[-1].strip()
            if source not in sources:
                sources.append(source[:30])
    
    result = {
        'found': len(matches) >= 3,
        'total_sources': len(matches),
        'sources': sources
    }
    
    if result['found']:
        print(f"   ✅ Found in {len(matches)} other sources!")
    else:
        print(f"   ⚠️ Found in only {len(matches)} sources")
    
    return result

if __name__ == "__main__":
    test_result = check_newsapi("Pakistan won the match")
    print(test_result)