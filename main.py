# Sehla Razzak (24K-0575)

from input import get_user_input
from ARY_Scraper import verify_ary_news
from News_API import check_newsapi
from Machine_learning import get_ml_prediction

def calculate_final_confidence(ary_result, ml_result, api_result):
    """
    Combine all three verification methods
    Weights: ML (50%), ARY (30%), NewsAPI (20%)
    """
    
    confidence = 0
    weights_used = []
    
    # 1. Logistic Regression ML (50% weight - Most important)
    if ml_result['prediction'] == 'REAL':
        ml_score = ml_result['confidence'] * 0.50
        weights_used.append(f"ML(REAL):{ml_result['confidence']:.1f}%")
    else:
        ml_score = (100 - ml_result['confidence']) * 0.50
        weights_used.append(f"ML(FAKE):{100-ml_result['confidence']:.1f}%")
    confidence += ml_score
    
    # 2. ARY News Search (30% weight)
    if ary_result['found']:
        ary_score = ary_result['similarity'] * 0.30
        weights_used.append(f"ARY:{ary_result['similarity']:.1f}%")
    else:
        weights_used.append(f"ARY:0%")
    confidence += ary_score if ary_result['found'] else 0
    
    # 3. NewsAPI (20% weight)
    if api_result['found']:
        api_score = min(api_result['total_sources'] * 4, 20)
        weights_used.append(f"API:{api_score:.1f}%")
    else:
        weights_used.append(f"API:0%")
    confidence += api_score if api_result['found'] else 0
    
    return round(confidence, 2), weights_used

def display_final_results(category_name, headline, ary_result, ml_result, api_result):
    """Display complete results with verdict"""
    
    print("\n" + "="*60)
    print("📊 FINAL FAKE NEWS DETECTION REPORT")
    print("="*60)
    
    print(f"\n📌 CATEGORY: {category_name.title()}")
    print(f"📰 HEADLINE: {headline}")
    
    # Calculate final confidence
    final_confidence, weights = calculate_final_confidence(ary_result, ml_result, api_result)
    
    # Display individual results
    print("\n" + "-"*40)
    print("🔍 INDIVIDUAL VERIFICATION RESULTS:")
    print("-"*40)
    
    # ML Result
    print(f"\n🤖 MACHINE LEARNING (Logistic Regression) - 50% weight:")
    print(f"   Prediction: {ml_result['prediction']}")
    print(f"   Confidence: {ml_result['confidence']:.1f}%")
    
    # ARY Result
    print(f"\n📰 ARY NEWS SEARCH (BFS) - 30% weight:")
    if ary_result['found']:
        print(f"   Status: ✅ MATCH FOUND")
        print(f"   Similarity: {ary_result['similarity']:.1f}%")
        if ary_result['match']:
            print(f"   Match: {ary_result['match']['text'][:60]}...")
    else:
        print(f"   Status: ❌ NO MATCH FOUND")
    
    # NewsAPI Result
    print(f"\n🌐 NEWSAPI (50,000+ sources) - 20% weight:")
    if api_result['found']:
        print(f"   Status: ✅ FOUND in {api_result['total_sources']} other sources")
        if api_result.get('sources'):
            print(f"   Sources: {', '.join(api_result['sources'][:3])}")
    else:
        print(f"   Status: ❌ NOT FOUND in other sources")
    
    # Final Verdict
    print("\n" + "="*40)
    print("🎯 FINAL VERDICT")
    print("="*40)
    
    print(f"\n📊 Confidence Score: {final_confidence:.1f}%")
    print(f"📊 Weights: {' + '.join(weights)}")
    
    if final_confidence >= 70:
        print("\n✅✅ FINAL VERDICT: REAL NEWS ✅✅")
        print("   This headline is VERIFIED and AUTHENTIC!")
        print("   ✓ Found on ARY News")
        print("   ✓ ML Model confirms REAL")
        if api_result['found']:
            print("   ✓ Other news sources agree")
    elif final_confidence >= 45:
        print("\n⚠️⚠️ FINAL VERDICT: SUSPICIOUS ⚠️⚠️")
        print("   This headline needs further verification!")
        print("   💡 Tip: Cross-check with official sources")
    else:
        print("\n❌❌ FINAL VERDICT: FAKE NEWS ❌❌")
        print("   This appears to be FAKE or MISINFORMATION!")
        print("   ⚠️ Do not share without verification")
    
    print("\n" + "="*60)

def main():
    """Main function - Complete AI Project"""
    
    print("\n" + "🚀"*30)
    print("   AI-POWERED FAKE NEWS DETECTOR")
    print("   Using: BFS Search + Logistic Regression ML + NewsAPI")
    print("🚀"*30)
    
    # Step 1: Get user input (input.py)
    category_name, category_url, headline = get_user_input()
    
    if not category_name:
        print("❌ Invalid input. Exiting...")
        return
    
    # Step 2: ARY News Search (ARY_Scraper.py)
    ary_result = verify_ary_news(category_name, headline)
    
    # Step 3: Machine Learning Prediction (Machine_learning.py)
    ml_result = get_ml_prediction(headline)
    
    # Step 4: NewsAPI Verification (News_API.py)
    api_result = check_newsapi(headline)
    
    # Step 5: Display Final Results
    display_final_results(category_name, headline, ary_result, ml_result, api_result)
    
    print("\n👋 Thank you for using AI Fake News Detector!")

if __name__ == "__main__":
    main()