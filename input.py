#Sehla Razzak (24K-0575)

def get_user_input():
    """Get category and headline from user"""
    
    print("="*60)
    print("📰 ARY NEWS FAKE NEWS DETECTOR - AI PROJECT")
    print("="*60)
    
    # Show categories
    print("\n📌 SELECT NEWS CATEGORY:")
    print("  1. 🇵🇰 Pakistan")
    print("  2. 🌍 International")
    print("  3. 🏏 Sports")
    print("  4. 💼 Business")
    print("  5. 🎭 Lifestyle")
    print("  6. 💻 Sci-Tech")
    print("  7. 📝 Blogs")
    print("  8. 🏥 Health")
    print("  9. 🎲 Off-Beat")
    
    # Category mapping
    categories = {
        1: ("pakistan", "https://arynews.tv/category/pakistan/"),
        2: ("international", "https://arynews.tv/category/international/"),
        3: ("sports", "https://arynews.tv/category/sports/"),
        4: ("business", "https://arynews.tv/category/business/"),
        5: ("lifestyle", "https://arynews.tv/category/lifestyle/"),
        6: ("sci-tech", "https://arynews.tv/category/sci-tech/"),
        7: ("blogs", "https://arynews.tv/category/blogs/"),
        8: ("health", "https://arynews.tv/category/health/"),
        9: ("off-beat", "https://arynews.tv/category/off-beat/")
    }
    
    # Get valid category choice
    while True:
        try:
            choice = int(input("\n👉 Enter your choice (1-9): "))
            if 1 <= choice <= 9:
                break
            else:
                print("Please enter number between 1-9")
        except ValueError:
            print("Please enter a valid number!")
    
    category_name, category_url = categories[choice]
    
    # Get headline
    headline = input("\n📝 Enter the headline to verify: ").strip()
    
    # Validation
    if not headline:
        print("Headline cannot be empty!")
        return None, None, None
    
    print(f"\nCategory: {category_name.title()}")
    print(f"Headline: {headline[:80]}...")
    
    return category_name, category_url, headline


# Test code
if __name__ == "__main__":
    cat_name, cat_url, headline = get_user_input()
    print(f"\nOutput: ({cat_name}, {cat_url}, {headline})")