#!/usr/bin/env python3
"""
Basic Usage Example for Destiny AI Content Processing Framework
Demonstrates core functionality of the framework
"""
import sys
import os

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.gemini_service import GeminiService
from src.content_processor import ContentProcessor

def main():
    """Demonstrate basic usage of Destiny framework"""
    
    print("🚀 Destiny AI Content Processing Framework - Basic Usage Example")
    print("=" * 60)
    
    try:
        # Initialize the processor (reads GEMINI_API_KEY from environment)
        processor = ContentProcessor()
        print("✅ ContentProcessor initialized successfully")
        
        # Example 1: Process HTML content
        print("\n📄 Example 1: HTML Content Processing")
        print("-" * 40)
        
        sample_html = """
        <html>
        <head><title>Sample Article</title></head>
        <body>
            <nav>
                <ul>
                    <li><a href="/home">Home</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>
            <main>
                <h1>Climate Change Impact on Agriculture</h1>
                <p>Climate change is significantly affecting agricultural practices worldwide. 
                Farmers are experiencing unpredictable weather patterns, increased droughts, 
                and extreme temperature fluctuations that impact crop yields.</p>
                <p>Recent studies show that adaptation strategies are crucial for maintaining 
                food security in the coming decades.</p>
            </main>
            <footer>
                <p>&copy; 2024 Sample News Site</p>
            </footer>
        </body>
        </html>
        """
        
        processed_content = processor.process_html_content(sample_html, target_language="English")
        
        if processed_content:
            print("✅ HTML processing successful!")
            print(f"Processed content: {processed_content[:200]}...")
        else:
            print("❌ No valid content found in HTML")
        
        # Example 2: Clean messy translation
        print("\n🧹 Example 2: Translation Cleaning")
        print("-" * 40)
        
        messy_translation = """
        The provided HTML content contains information about climate change. 
        **Navigation menu items removed for clarity.**
        
        Here is the extracted content:
        
        Climate Change Impact on Agriculture
        
        Climate change is significantly affecting agricultural practices worldwide...
        
        [Note: Footer and navigation elements have been removed]
        """
        
        cleaned_text = processor.clean_translation(messy_translation)
        
        if cleaned_text:
            print("✅ Translation cleaning successful!")
            print(f"Cleaned text: {cleaned_text[:200]}...")
        else:
            print("❌ No valid content found in translation")
        
        # Example 3: Extract structured content
        print("\n📊 Example 3: Content Structure Extraction")
        print("-" * 40)
        
        raw_text = """
        Published: 2024-01-15
        
        Breaking News: New Climate Policy Announced
        
        The government announced a comprehensive climate policy today that will affect 
        multiple sectors including agriculture, transportation, and energy production.
        
        Key points include carbon emission targets, renewable energy incentives, and 
        support for green technology development.
        """
        
        structured_content = processor.extract_article_content(raw_text)
        
        if structured_content:
            print("✅ Content extraction successful!")
            print(f"Structured content: {structured_content}")
        else:
            print("❌ Could not extract structured content")
        
        # Example 4: Duplicate detection
        print("\n🔍 Example 4: Duplicate Content Detection")
        print("-" * 40)
        
        content1 = "Climate change is affecting agriculture worldwide with unpredictable weather patterns."
        content2 = "Agricultural practices are being impacted globally by climate change and weather unpredictability."
        content3 = "The new smartphone features advanced camera technology and improved battery life."
        
        # Compare similar content
        is_duplicate_1_2 = processor.detect_content_similarity(content1, content2, "Climate Article 1", "Climate Article 2")
        print(f"Content 1 vs Content 2 (similar topics): {'Duplicate' if is_duplicate_1_2 else 'Different'}")
        
        # Compare different content
        is_duplicate_1_3 = processor.detect_content_similarity(content1, content3, "Climate Article", "Tech Article")
        print(f"Content 1 vs Content 3 (different topics): {'Duplicate' if is_duplicate_1_3 else 'Different'}")
        
        print("\n🎉 All examples completed successfully!")
        print("\nNext steps:")
        print("- Check out examples/batch_processing.py for batch processing")
        print("- Check out examples/duplicate_detection.py for advanced duplicate detection")
        print("- Read the README.md for more detailed usage instructions")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure you have set GEMINI_API_KEY in your .env file")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check your internet connection")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)