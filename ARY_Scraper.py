# Tania (24K-0713)

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from collections import deque

def calculate_similarity(a, b):
    """Calculate similarity percentage between two headlines"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100

def scrape_page(url):
    """Extract all headlines from a single page"""
    headlines = []
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for tag in soup.find_all(['h2', 'h3']):
            text = tag.get_text(strip=True)
            
            if text and len(text) > 10:
                link = tag.find('a')
                if link and link.get('href'):
                    headlines.append({
                        'text': text,
                        'url': link['href']
                    })
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    
    return headlines

def bfs_scrape(category, max_pages=2):
    """Scrape multiple pages using BFS search"""
    
    category_urls = {
        "pakistan": "https://arynews.tv/category/pakistan/",
        "international": "https://arynews.tv/category/international/",
        "sports": "https://arynews.tv/category/sports/",
        "business": "https://arynews.tv/category/business/",
        "lifestyle": "https://arynews.tv/category/lifestyle/",
        "sci-tech": "https://arynews.tv/category/sci-tech/",
        "blogs": "https://arynews.tv/category/blogs/",
        "health": "https://arynews.tv/category/health/",
        "off-beat": "https://arynews.tv/category/off-beat/"
    }
    
    if category not in category_urls:
        return []
    
    base_url = category_urls[category]
    queue = deque([base_url])
    visited = set()
    all_headlines = []
    page_count = 0
    
    while queue and page_count < max_pages:
        current_url = queue.popleft()
        
        if current_url in visited:
            continue
        
        visited.add(current_url)
        headlines = scrape_page(current_url)
        all_headlines.extend(headlines)
        page_count += 1
        
        next_page_url = base_url + f"page/{page_count + 1}/"
        if next_page_url not in visited:
            queue.append(next_page_url)
    
    return all_headlines

def find_best_match(user_headline, headlines, threshold=60):
    """Find the best matching headline"""
    
    best_match = None
    best_score = 0
    
    for item in headlines:
        score = calculate_similarity(user_headline, item['text'])
        if score > best_score:
            best_score = score
            best_match = item
    
    if best_score >= threshold:
        return {
            'found': True,
            'similarity': round(best_score, 2),
            'match': {
                'text': best_match['text'],
                'url': best_match['url']
            }
        }
    else:
        return {
            'found': False,
            'similarity': 0,
            'match': None
        }

def verify_ary_news(category_name, user_headline):
    """Main function - Verifies headline on ARY News"""
    
    print(f"\n🔍 Searching ARY News ({category_name})...")
    
    headlines = bfs_scrape(category_name)
    
    if not headlines:
        return {'found': False, 'similarity': 0, 'match': None}
    
    result = find_best_match(user_headline, headlines)
    
    if result['found']:
        print(f"   ✅ Match found! ({result['similarity']}% similar)")
        print(f"   📝 {result['match']['text'][:60]}...")
    else:
        print(f"   ❌ No match found on ARY News")
    
    return result

if __name__ == "__main__":
    test_result = verify_ary_news("pakistan", "PM announces new policy")
    print(test_result)