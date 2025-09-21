#!/usr/bin/env python3
"""
Content Processor - A generic content processing framework using AI
Processes content from various sources using Gemini AI for extraction and translation
"""
import os
import sys
import logging
from typing import Optional, Dict, List, Any, Callable
from .services.gemini_service import GeminiService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self, gemini_api_key: Optional[str] = None, model_name: str = 'gemini-1.5-flash'):
        """
        Initialize the content processor with Gemini AI
        
        Args:
            gemini_api_key: Google Gemini API key. If None, reads from GEMINI_API_KEY env var
            model_name: Gemini model to use (default: gemini-1.5-flash)
        """
        self.gemini_service = GeminiService(api_key=gemini_api_key, model_name=model_name)
    
    def process_html_content(self, html_content: str, target_language: str = "English") -> Optional[str]:
        """
        Process raw HTML content by extracting main article text and translating
        
        Args:
            html_content: Raw HTML content to process
            target_language: Target language for translation (default: English)
            
        Returns:
            Processed and translated content or None if processing fails
        """
        try:
            return self.gemini_service.process_html_content(html_content, target_language)
        except Exception as e:
            logger.error(f"HTML processing error: {str(e)}")
            raise Exception(f"Failed to process HTML content: {str(e)}")
    
    def clean_translation(self, text: str) -> Optional[str]:
        """
        Clean translation text by removing unwanted content and metadata
        
        Args:
            text: Raw translated text to clean
            
        Returns:
            Cleaned text or None if no valid content found
        """
        try:
            return self.gemini_service.clean_translation(text)
        except Exception as e:
            logger.error(f"Translation cleaning error: {str(e)}")
            raise Exception(f"Failed to clean translation: {str(e)}")
    
    def extract_article_content(self, text: str) -> Optional[dict]:
        """
        Extract and structure article content from messy text
        
        Args:
            text: Raw text to extract article content from
            
        Returns:
            Dictionary with structured content or None if extraction fails
        """
        try:
            return self.gemini_service.extract_article_content(text)
        except Exception as e:
            logger.error(f"Content extraction error: {str(e)}")
            raise Exception(f"Failed to extract content: {str(e)}")
    
    def detect_content_similarity(self, content1: str, content2: str, title1: str = "", title2: str = "") -> Optional[bool]:
        """
        Check if two pieces of content are substantially the same using AI
        
        Args:
            content1: First content to compare
            content2: Second content to compare
            title1: Optional title for first content
            title2: Optional title for second content
            
        Returns:
            True if content is duplicated/same, False if different, None if error
        """
        try:
            return self.gemini_service.detect_content_similarity(content1, content2, title1, title2)
        except Exception as e:
            logger.error(f"Similarity detection error: {str(e)}")
            return None
    
    def process_batch(self, 
                     items: List[Dict[str, Any]], 
                     content_field: str = 'content',
                     id_field: str = 'id',
                     process_func: Optional[Callable] = None,
                     update_callback: Optional[Callable] = None) -> Dict[str, int]:
        """
        Process a batch of content items with customizable processing and update functions
        
        Args:
            items: List of content items to process
            content_field: Field name containing content to process (default: 'content')
            id_field: Field name containing unique identifier (default: 'id')
            process_func: Custom processing function. If None, uses process_html_content
            update_callback: Function to call with (id, processed_content, is_error) for each item
            
        Returns:
            Dictionary with processing statistics
        """
        if not process_func:
            process_func = self.process_html_content
        
        logger.info(f"Starting batch processing of {len(items)} items...")
        
        processed = 0
        failed = 0
        skipped = 0
        
        for item in items:
            try:
                item_id = item.get(id_field)
                content = item.get(content_field)
                
                if not content:
                    logger.warning(f"No content found for item {item_id}")
                    skipped += 1
                    continue
                
                logger.info(f"Processing item {item_id}...")
                
                # Process content using provided function
                result = process_func(content)
                
                if result:
                    # Update using callback if provided
                    if update_callback:
                        if update_callback(item_id, result, False):
                            logger.info(f"Successfully processed item {item_id}")
                            processed += 1
                        else:
                            logger.warning(f"Failed to update item {item_id}")
                            failed += 1
                    else:
                        logger.info(f"Successfully processed item {item_id} (no update callback)")
                        processed += 1
                else:
                    # Handle "no valid content" case
                    error_msg = "No valid content found during processing"
                    if update_callback:
                        if update_callback(item_id, error_msg, True):
                            logger.warning(f"No valid content for item {item_id} - recorded as error")
                            skipped += 1
                        else:
                            logger.error(f"Failed to record error for item {item_id}")
                            failed += 1
                    else:
                        logger.warning(f"No valid content for item {item_id}")
                        skipped += 1
                    
            except Exception as e:
                # Handle processing errors
                error_msg = f"Processing failed: {str(e)}"
                item_id = item.get(id_field, 'unknown')
                
                if update_callback:
                    try:
                        if update_callback(item_id, error_msg, True):
                            logger.error(f"Processing error for item {item_id}: {str(e)} - recorded")
                            failed += 1
                        else:
                            logger.error(f"Failed to record processing error for item {item_id}: {str(e)}")
                            failed += 1
                    except Exception as cb_error:
                        logger.error(f"Callback error while recording processing error for item {item_id}: {str(cb_error)}")
                        failed += 1
                else:
                    logger.error(f"Processing error for item {item_id}: {str(e)}")
                    failed += 1
        
        results = {
            'processed': processed,
            'failed': failed,
            'skipped': skipped,
            'total': len(items)
        }
        
        logger.info(f"Batch processing completed: {results}")
        return results
    
    def find_duplicates(self, items: List[Dict[str, Any]], 
                       content_field: str = 'content',
                       title_field: str = 'title',
                       id_field: str = 'id') -> List[Dict[str, Any]]:
        """
        Find duplicate content items in a list using AI similarity detection
        
        Args:
            items: List of items to check for duplicates
            content_field: Field name containing content (default: 'content')
            title_field: Field name containing title (default: 'title')
            id_field: Field name containing unique identifier (default: 'id')
            
        Returns:
            List of duplicate pairs with similarity information
        """
        duplicates = []
        processed_pairs = set()
        
        logger.info(f"Checking {len(items)} items for duplicates...")
        
        for i, item1 in enumerate(items):
            for j, item2 in enumerate(items[i+1:], i+1):
                # Create unique pair identifier
                pair_id = tuple(sorted([item1.get(id_field), item2.get(id_field)]))
                if pair_id in processed_pairs:
                    continue
                processed_pairs.add(pair_id)
                
                try:
                    is_duplicate = self.detect_content_similarity(
                        item1.get(content_field, ''),
                        item2.get(content_field, ''),
                        item1.get(title_field, ''),
                        item2.get(title_field, '')
                    )
                    
                    if is_duplicate is True:
                        duplicates.append({
                            'item1': item1,
                            'item2': item2,
                            'similarity': 'duplicate'
                        })
                        logger.info(f"Found duplicate: {item1.get(id_field)} and {item2.get(id_field)}")
                    
                except Exception as e:
                    logger.error(f"Error comparing items {item1.get(id_field)} and {item2.get(id_field)}: {str(e)}")
                    continue
        
        logger.info(f"Found {len(duplicates)} duplicate pairs out of {len(processed_pairs)} comparisons")
        return duplicates

def main():
    """
    Example main function showing how to use the ContentProcessor
    """
    # Example usage
    processor = ContentProcessor()
    
    # Example items (you would typically load these from your data source)
    example_items = [
        {
            'id': '1',
            'content': '<html><body><h1>Sample Article</h1><p>This is sample content...</p></body></html>',
            'title': 'Sample Article'
        }
    ]
    
    # Example processing function
    def example_update_callback(item_id: str, processed_content: str, is_error: bool) -> bool:
        """Example callback to handle processed content"""
        prefix = "[ERROR] " if is_error else ""
        print(f"Item {item_id}: {prefix}{processed_content[:100]}...")
        return True  # Simulate successful update
    
    # Process the batch
    results = processor.process_batch(
        items=example_items,
        content_field='content',
        update_callback=example_update_callback
    )
    
    print(f"\nProcessing Results:")
    print(f"Total: {results['total']}")
    print(f"Processed: {results['processed']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")

if __name__ == "__main__":
    main()