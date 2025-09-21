#!/usr/bin/env python3
"""
Duplicate Detection Example for Destiny AI Content Processing Framework
Demonstrates AI-powered semantic duplicate detection capabilities
"""
import sys
import os
import time

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.content_processor import ContentProcessor

def main():
    """Demonstrate duplicate detection capabilities"""
    
    print("🚀 Destiny AI Content Processing Framework - Duplicate Detection Example")
    print("=" * 75)
    
    try:
        # Initialize the processor
        processor = ContentProcessor()
        print("✅ ContentProcessor initialized successfully")
        
        # Example dataset with intentional duplicates and similar content
        sample_articles = [
            {
                'id': 'news_001',
                'title': 'Climate Change Affects Agriculture',
                'content': '''Climate change is significantly impacting agricultural practices worldwide. 
                Farmers are experiencing unpredictable weather patterns, increased droughts, and extreme 
                temperature fluctuations that affect crop yields. Adaptation strategies are becoming 
                crucial for maintaining food security.''',
                'source': 'Environmental News',
                'date': '2024-01-15'
            },
            {
                'id': 'news_002',
                'title': 'Agricultural Impact of Climate Change',
                'content': '''The global agricultural sector is facing significant challenges due to climate change. 
                Unpredictable weather, drought conditions, and temperature extremes are causing major disruptions 
                to farming operations worldwide. Food security experts emphasize the need for adaptive strategies.''',
                'source': 'Farm Today',
                'date': '2024-01-16'
            },
            {
                'id': 'tech_001',
                'title': 'New Smartphone Released',
                'content': '''Apple has announced its latest iPhone with revolutionary camera technology. 
                The new device features improved battery life, faster processing speeds, and enhanced 
                security features. Pre-orders begin next week with worldwide availability in March.''',
                'source': 'Tech Review',
                'date': '2024-01-20'
            },
            {
                'id': 'news_003',
                'title': 'Renewable Energy Breakthrough',
                'content': '''Scientists have developed a new type of solar panel that achieves 40% higher 
                efficiency than traditional models. The breakthrough uses quantum dot technology to capture 
                more sunlight and convert it to electricity more effectively.''',
                'source': 'Science Daily',
                'date': '2024-01-18'
            },
            {
                'id': 'tech_002',
                'title': 'Apple Unveils Latest iPhone',
                'content': '''Apple\'s newest iPhone model showcases cutting-edge camera innovations and 
                extended battery performance. The device includes upgraded processors and advanced security 
                measures. Global launch scheduled for March following pre-order period.''',
                'source': 'Mobile News',
                'date': '2024-01-21'
            },
            {
                'id': 'news_004',
                'title': 'Ocean Conservation Initiative',
                'content': '''A new marine protected area has demonstrated remarkable success in restoring 
                ocean biodiversity. Marine biologists report a 300% increase in fish populations and 
                significant coral reef recovery within just two years of protection.''',
                'source': 'Ocean Times',
                'date': '2024-01-22'
            },
            {
                'id': 'news_005',
                'title': 'Global Warming and Farming',
                'content': '''Agricultural production worldwide is being severely affected by climate change. 
                Irregular weather patterns, prolonged droughts, and temperature variations are creating 
                unprecedented challenges for farmers globally. Experts stress the importance of adaptation.''',
                'source': 'Agricultural Weekly',
                'date': '2024-01-17'
            }
        ]
        
        print(f"\n🔍 Analyzing {len(sample_articles)} articles for duplicate content...")
        print("-" * 60)
        
        # Method 1: Use the built-in duplicate detection
        print("Method 1: Automated Duplicate Detection")
        print("-" * 40)
        
        start_time = time.time()
        duplicates = processor.find_duplicates(
            items=sample_articles,
            content_field='content',
            title_field='title',
            id_field='id'
        )
        detection_time = time.time() - start_time
        
        print(f"⏱️  Detection completed in {detection_time:.2f} seconds")
        print(f"🔍 Found {len(duplicates)} duplicate pairs")
        
        if duplicates:
            print("\n📋 Duplicate Pairs Found:")
            for i, dup in enumerate(duplicates, 1):
                item1 = dup['item1']
                item2 = dup['item2']
                print(f"\n{i}. Duplicate Pair:")
                print(f"   Article A: {item1['id']} - \"{item1['title']}\"")
                print(f"   Article B: {item2['id']} - \"{item2['title']}\"")
                print(f"   Sources: {item1['source']} vs {item2['source']}")
                print(f"   Dates: {item1['date']} vs {item2['date']}")
        
        # Method 2: Manual comparison of specific pairs
        print(f"\n\nMethod 2: Manual Pairwise Comparison")
        print("-" * 40)
        
        # Compare climate change articles (should be duplicates)
        climate_articles = [article for article in sample_articles if 'climate' in article['title'].lower() or 'warming' in article['title'].lower()]
        
        if len(climate_articles) >= 2:
            article1 = climate_articles[0]
            article2 = climate_articles[1]
            
            print(f"Comparing: \"{article1['title']}\" vs \"{article2['title']}\"")
            
            is_duplicate = processor.detect_content_similarity(
                article1['content'],
                article2['content'],
                article1['title'],
                article2['title']
            )
            
            result = "🔄 DUPLICATE" if is_duplicate else "✅ DIFFERENT"
            print(f"Result: {result}")
            
            if is_duplicate:
                print("💡 These articles cover the same story with similar facts")
            else:
                print("💡 These articles are about different topics or events")
        
        # Compare tech articles (should be duplicates)
        tech_articles = [article for article in sample_articles if article['id'].startswith('tech_')]
        
        if len(tech_articles) >= 2:
            article1 = tech_articles[0]
            article2 = tech_articles[1]
            
            print(f"\nComparing: \"{article1['title']}\" vs \"{article2['title']}\"")
            
            is_duplicate = processor.detect_content_similarity(
                article1['content'],
                article2['content'],
                article1['title'],
                article2['title']
            )
            
            result = "🔄 DUPLICATE" if is_duplicate else "✅ DIFFERENT"
            print(f"Result: {result}")
        
        # Compare articles from different topics (should be different)
        if len(sample_articles) >= 3:
            climate_article = next((a for a in sample_articles if 'climate' in a['title'].lower()), None)
            tech_article = next((a for a in sample_articles if a['id'].startswith('tech_')), None)
            
            if climate_article and tech_article:
                print(f"\nComparing different topics: \"{climate_article['title']}\" vs \"{tech_article['title']}\"")
                
                is_duplicate = processor.detect_content_similarity(
                    climate_article['content'],
                    tech_article['content'],
                    climate_article['title'],
                    tech_article['title']
                )
                
                result = "🔄 DUPLICATE" if is_duplicate else "✅ DIFFERENT"
                print(f"Result: {result}")
        
        # Deduplication strategy example
        print(f"\n📊 Deduplication Strategy Example")
        print("-" * 40)
        
        if duplicates:
            print("Recommended deduplication actions:")
            
            for i, dup in enumerate(duplicates, 1):
                item1 = dup['item1']
                item2 = dup['item2']
                
                # Simple strategy: keep the earlier article
                date1 = item1['date']
                date2 = item2['date']
                
                if date1 <= date2:
                    keep = item1
                    remove = item2
                else:
                    keep = item2
                    remove = item1
                
                print(f"\n{i}. Duplicate pair {item1['id']} & {item2['id']}:")
                print(f"   ✅ Keep: {keep['id']} (published {keep['date']})")
                print(f"   ❌ Remove: {remove['id']} (published {remove['date']})")
                print(f"   Reason: Earlier publication date")
        
        # Performance summary
        total_comparisons = len(sample_articles) * (len(sample_articles) - 1) // 2
        avg_time_per_comparison = detection_time / total_comparisons if total_comparisons > 0 else 0
        
        print(f"\n📈 Performance Summary")
        print("=" * 25)
        print(f"Articles analyzed: {len(sample_articles)}")
        print(f"Total comparisons: {total_comparisons}")
        print(f"Duplicates found: {len(duplicates)}")
        print(f"Total processing time: {detection_time:.2f} seconds")
        print(f"Average time per comparison: {avg_time_per_comparison:.2f} seconds")
        print(f"Deduplication rate: {len(duplicates)/len(sample_articles)*100:.1f}%")
        
        print("\n🎉 Duplicate detection example completed!")
        print("\nKey insights:")
        print("- AI can detect semantic similarity beyond exact text matching")
        print("- Different sources can report the same story (duplicates)")
        print("- Similar topics with different facts are correctly identified as different")
        print("- Automated deduplication can significantly reduce dataset size")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify your GEMINI_API_KEY environment variable")
        print("2. Check internet connection for API calls")
        print("3. Ensure sufficient API quota for multiple requests")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)