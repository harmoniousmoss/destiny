#!/usr/bin/env python3
"""
Batch Processing Example for Destiny AI Content Processing Framework
Demonstrates how to process multiple items efficiently with custom callbacks
"""
import sys
import os
import time

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.content_processor import ContentProcessor

def main():
    """Demonstrate batch processing capabilities"""
    
    print("🚀 Destiny AI Content Processing Framework - Batch Processing Example")
    print("=" * 70)
    
    try:
        # Initialize the processor
        processor = ContentProcessor()
        print("✅ ContentProcessor initialized successfully")
        
        # Example data set
        sample_items = [
            {
                'id': 'article_001',
                'content': '''
                <html><body>
                <h1>Renewable Energy Breakthrough</h1>
                <p>Scientists have developed a new solar panel technology that increases 
                efficiency by 40%. This breakthrough could revolutionize clean energy adoption.</p>
                <p>The new technology uses quantum dot enhancement to capture more sunlight.</p>
                </body></html>
                ''',
                'title': 'Solar Panel Breakthrough',
                'source': 'Tech News'
            },
            {
                'id': 'article_002',
                'content': '''
                <html><body>
                <nav>Menu items here</nav>
                <h1>Ocean Conservation Success</h1>
                <p>A new marine protected area has shown remarkable recovery of fish populations. 
                Marine biologists report a 300% increase in biodiversity within two years.</p>
                <footer>Copyright notice</footer>
                </body></html>
                ''',
                'title': 'Marine Conservation',
                'source': 'Environment Today'
            },
            {
                'id': 'article_003',
                'content': '''
                <html><body>
                <h1>AI in Healthcare</h1>
                <p>Artificial intelligence is transforming diagnostic medicine with new 
                machine learning algorithms that can detect diseases earlier than traditional methods.</p>
                <p>Early trials show 95% accuracy in cancer detection.</p>
                </body></html>
                ''',
                'title': 'AI Healthcare Revolution',
                'source': 'Medical Journal'
            },
            {
                'id': 'article_004',
                'content': '',  # Empty content to test error handling
                'title': 'Empty Article',
                'source': 'Test Source'
            },
            {
                'id': 'article_005',
                'content': '''
                <html><body>
                <nav>Navigation</nav>
                <div>Advertisement</div>
                <p>This is minimal content that might not be worth processing.</p>
                <footer>Footer</footer>
                </body></html>
                ''',
                'title': 'Minimal Content',
                'source': 'Test Source'
            }
        ]
        
        print(f"\n📊 Processing {len(sample_items)} items in batch...")
        print("-" * 50)
        
        # Storage for processed results
        processed_results = {}
        error_log = []
        
        def update_callback(item_id: str, processed_content: str, is_error: bool) -> bool:
            """
            Custom callback function to handle processed content
            In a real application, this would typically save to a database
            """
            try:
                if is_error:
                    print(f"❌ Error processing {item_id}: {processed_content[:100]}...")
                    error_log.append({
                        'id': item_id,
                        'error': processed_content,
                        'timestamp': time.time()
                    })
                else:
                    print(f"✅ Successfully processed {item_id}: {processed_content[:100]}...")
                    processed_results[item_id] = {
                        'content': processed_content,
                        'timestamp': time.time(),
                        'length': len(processed_content)
                    }
                
                # Simulate database save delay
                time.sleep(0.1)
                return True
                
            except Exception as e:
                print(f"❌ Callback error for {item_id}: {str(e)}")
                return False
        
        # Custom processing function (optional)
        def custom_html_processor(content: str) -> str:
            """
            Custom processing function that adds metadata
            You can define your own processing logic here
            """
            # Use the standard processor but add some metadata
            result = processor.process_html_content(content)
            if result:
                return f"[PROCESSED] {result}"
            return None
        
        # Process the batch
        start_time = time.time()
        
        results = processor.process_batch(
            items=sample_items,
            content_field='content',
            id_field='id',
            process_func=custom_html_processor,  # Use custom processor
            update_callback=update_callback
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Display results
        print("\n📈 Batch Processing Results")
        print("=" * 30)
        print(f"Total items: {results['total']}")
        print(f"Successfully processed: {results['processed']}")
        print(f"Failed: {results['failed']}")
        print(f"Skipped (no content): {results['skipped']}")
        print(f"Processing time: {processing_time:.2f} seconds")
        print(f"Average time per item: {processing_time/results['total']:.2f} seconds")
        
        # Show successful results
        if processed_results:
            print(f"\n✅ Successfully Processed Items ({len(processed_results)}):")
            print("-" * 40)
            for item_id, data in processed_results.items():
                print(f"• {item_id}: {data['length']} characters")
                print(f"  Preview: {data['content'][:150]}...")
                print()
        
        # Show errors
        if error_log:
            print(f"\n❌ Error Log ({len(error_log)}):")
            print("-" * 20)
            for error in error_log:
                print(f"• {error['id']}: {error['error'][:100]}...")
        
        # Performance metrics
        success_rate = (results['processed'] / results['total']) * 100 if results['total'] > 0 else 0
        print(f"\n📊 Performance Metrics:")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Throughput: {results['total']/processing_time:.1f} items/second")
        
        print("\n🎉 Batch processing example completed!")
        print("\nKey takeaways:")
        print("- Use custom callbacks to handle processed content")
        print("- Error handling ensures robust processing")
        print("- Custom processing functions provide flexibility")
        print("- Built-in metrics help monitor performance")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your GEMINI_API_KEY environment variable")
        print("2. Ensure you have internet connectivity")
        print("3. Verify all dependencies are installed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)