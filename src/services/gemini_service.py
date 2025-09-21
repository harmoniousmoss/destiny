"""
Gemini AI service for text cleaning and processing
A clean, reusable service for AI-powered content processing tasks
"""
import os
import json
import logging
import google.generativeai as genai
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: Optional[str] = None, model_name: str = 'gemini-1.5-flash'):
        """
        Initialize Gemini API client
        
        Args:
            api_key: Google Gemini API key. If None, will read from GEMINI_API_KEY env var
            model_name: Gemini model to use (default: gemini-1.5-flash)
        """
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please provide api_key parameter or set GEMINI_API_KEY environment variable")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def clean_translation(self, text: str) -> Optional[str]:
        """
        Clean translation text by removing unwanted content
        like HTML parsing errors and metadata
        
        Args:
            text: Raw translated text to clean
            
        Returns:
            Cleaned text or None if no valid content found
        """
        try:
            prompt = """
            Please clean the following translated text by:
            1. Remove all mentions of "The provided HTML content..."
            2. Remove any technical messages about missing content or HTML parsing
            3. Remove navigation elements, menu items, and metadata descriptions
            4. Keep ONLY the actual article content
            5. If there are multiple attempts at translation, keep only the most complete one
            6. Return the cleaned text in proper English
            
            If the text contains no actual article content, return "No valid content found."
            
            Text to clean:
            """
            
            response = self.model.generate_content(prompt + "\n\n" + text)
            
            if response and response.text:
                cleaned = response.text.strip()
                # Check if the response indicates no content
                if "no valid content" in cleaned.lower() or "no article content" in cleaned.lower():
                    return None
                return cleaned
            
            return None
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise Exception(f"Failed to clean text: {str(e)}")
    
    def extract_article_content(self, text: str) -> Optional[dict]:
        """
        Extract and structure article content from messy translation
        
        Args:
            text: Raw text to extract article content from
            
        Returns:
            Dictionary with structured content or None if extraction fails
        """
        try:
            prompt = """
            Extract the main article content from this text and return it in JSON format with these fields:
            - title: The article title
            - date: Publication date (if found)
            - content: The main article body (cleaned and properly formatted)
            - summary: A brief 2-3 sentence summary
            
            Remove all HTML parsing errors, navigation elements, and metadata.
            If no valid article content exists, return {"error": "No valid content found"}
            
            Text to process:
            """
            
            response = self.model.generate_content(prompt + "\n\n" + text)
            
            if response and response.text:
                try:
                    # Try to parse as JSON
                    result = json.loads(response.text)
                    return result
                except json.JSONDecodeError:
                    # If not valid JSON, return as plain text
                    return {"content": response.text}
            
            return None
            
        except Exception as e:
            logger.error(f"Gemini extraction error: {str(e)}")
            raise Exception(f"Failed to extract content: {str(e)}")
    
    def detect_content_similarity(self, content1: str, content2: str, title1: str = "", title2: str = "") -> Optional[bool]:
        """
        Use Gemini AI to check if two pieces of content are substantially the same
        
        Args:
            content1: First content to compare
            content2: Second content to compare
            title1: Optional title for first content
            title2: Optional title for second content
            
        Returns:
            True if content is duplicated/same, False if different, None if error
        """
        try:
            prompt = f"""Compare these two articles and determine if they are substantially the same content (duplicates) or different articles.

Consider them duplicates if they:
- Report the same news event or story
- Have the same main facts and information
- Are about the same topic with similar details
- Are just different versions/translations of the same article

Consider them different if they:
- Report different events or stories
- Have different main facts or focus
- Are about different topics
- Just happen to mention similar keywords but cover different content

Return ONLY "DUPLICATE" if they are the same content, or "DIFFERENT" if they are different articles.

Article 1 Title: {title1}
Article 1 Content:
{content1[:2000]}

Article 2 Title: {title2}
Article 2 Content:
{content2[:2000]}

Response:"""
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                result = response.text.strip().upper()
                if "DUPLICATE" in result:
                    return True
                elif "DIFFERENT" in result:
                    return False
                else:
                    logger.warning(f"Unexpected Gemini response: {result}")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return None
    
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
            prompt = f"""
            Extract and translate the main article content from this HTML.
            
            Instructions:
            1. Extract only the main article text, ignore navigation, ads, footers, headers
            2. Translate the content to {target_language} if it's in another language
            3. Clean up any HTML artifacts or formatting issues
            4. Return only the clean, translated article text
            5. If no meaningful content is found, return "No article content found"
            
            HTML Content:
            """
            
            response = self.model.generate_content(prompt + "\n\n" + html_content[:8000])  # Limit to prevent token overflow
            
            if response and response.text:
                result = response.text.strip()
                if "no article content" in result.lower() or "no meaningful content" in result.lower():
                    return None
                return result
            
            return None
            
        except Exception as e:
            logger.error(f"HTML processing error: {str(e)}")
            raise Exception(f"Failed to process HTML content: {str(e)}")