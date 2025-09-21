# Destiny - AI Content Processing Framework

Destiny is open-source Python framework for AI-powered content processing, translation, and duplicate detection. Built around Google Gemini AI, it provides clean, reusable components for extracting, cleaning, and analyzing text content from various sources.

## ✨ Features

- **AI-Powered Content Processing**: Extract and clean content from HTML, translate between languages
- **Smart Duplicate Detection**: Use AI to identify semantically similar content beyond simple text matching
- **Batch Processing**: Efficiently process large datasets with customizable callbacks
- **Clean Architecture**: Modular design with clear separation of concerns
- **Production Ready**: Comprehensive error handling, logging, and rate limiting

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd destiny

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Google Gemini API key
```

### Basic Usage

```python
from src.services.gemini_service import GeminiService
from src.content_processor import ContentProcessor

# Initialize the processor
processor = ContentProcessor(gemini_api_key="your_api_key_here")

# Process HTML content
html_content = "<html><body><h1>Article Title</h1><p>Content...</p></body></html>"
processed = processor.process_html_content(html_content, target_language="English")

# Clean translated text
messy_translation = "The provided HTML content contains... actual content here..."
cleaned = processor.clean_translation(messy_translation)

# Detect duplicate content
is_duplicate = processor.detect_content_similarity(content1, content2, title1, title2)
```

## 📁 Project Structure

```
destiny/
├── src/
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py      # Core Gemini AI integration
│   ├── utils/
│   │   └── __init__.py
│   ├── content_processor.py       # High-level content processing
│   └── __init__.py
├── examples/
│   ├── basic_usage.py            # Basic usage examples
│   ├── batch_processing.py       # Batch processing example
│   └── duplicate_detection.py    # Duplicate detection example
├── .env.example                  # Environment configuration template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🛠️ Core Components

### GeminiService

The core AI service that handles all interactions with Google Gemini API:

```python
from src.services.gemini_service import GeminiService

service = GeminiService(api_key="your_key")

# Clean translation text
cleaned = service.clean_translation(messy_text)

# Extract structured content
structured = service.extract_article_content(raw_text)

# Process HTML content
processed = service.process_html_content(html_content)

# Detect content similarity
is_similar = service.detect_content_similarity(content1, content2)
```

### Content Processor

High-level processor that combines multiple AI operations:

```python
from src.content_processor import ContentProcessor

processor = ContentProcessor()

# Process items in batches
items = [{'id': '1', 'content': 'html...', 'title': 'Article'}]
results = processor.process_batch(items, update_callback=your_callback)

# Find duplicates in dataset
duplicates = processor.find_duplicates(items)
```

## 📖 Examples

### Basic Content Processing

```python
from src.content_processor import ContentProcessor

# Initialize processor
processor = ContentProcessor()

# Example HTML content
html = """
<html>
<body>
    <nav>Navigation menu</nav>
    <h1>Important Article</h1>
    <p>This is the main article content that we want to extract.</p>
    <footer>Footer content</footer>
</body>
</html>
"""

# Process and extract clean content
result = processor.process_html_content(html, target_language="English")
print(result)  # Output: Clean article text without navigation/footer
```

### Batch Processing with Custom Callbacks

```python
# Define your update callback
def save_to_database(item_id: str, processed_content: str, is_error: bool) -> bool:
    if is_error:
        print(f"Error processing {item_id}: {processed_content}")
    else:
        print(f"Successfully processed {item_id}")
        # Save to your database here
    return True

# Process items
items = [
    {'id': '1', 'content': 'html content 1', 'title': 'Article 1'},
    {'id': '2', 'content': 'html content 2', 'title': 'Article 2'}
]

results = processor.process_batch(
    items=items,
    content_field='content',
    update_callback=save_to_database
)

print(f"Processed: {results['processed']}, Failed: {results['failed']}")
```

### Duplicate Detection

```python
# Example items with similar content
items = [
    {'id': '1', 'content': 'Article about climate change...', 'title': 'Climate News'},
    {'id': '2', 'content': 'Different article about weather...', 'title': 'Weather Update'},
    {'id': '3', 'content': 'Same climate change story...', 'title': 'Climate Report'}
]

# Find duplicates
duplicates = processor.find_duplicates(items)

for dup in duplicates:
    print(f"Items {dup['item1']['id']} and {dup['item2']['id']} are duplicates")
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Required: Google Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Custom model (default: gemini-1.5-flash)
GEMINI_MODEL=gemini-1.5-flash

# Optional: Logging configuration
LOG_LEVEL=INFO
```

### API Key Setup

1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/)
2. Add it to your `.env` file or pass it directly to the service
3. Ensure your API key has appropriate quotas for your usage

## 🔧 Advanced Usage

### Custom Processing Functions

```python
def custom_processor(content: str) -> str:
    # Your custom processing logic
    return processed_content

# Use custom processor in batch processing
results = processor.process_batch(
    items=items,
    process_func=custom_processor,
    update_callback=your_callback
)
```

### Error Handling

```python
try:
    result = processor.process_html_content(html_content)
    if result:
        print("Processing successful")
    else:
        print("No valid content found")
except Exception as e:
    print(f"Processing failed: {e}")
```

## 🧪 Testing

Run the examples to test your setup:

```bash
# Test basic functionality
python examples/basic_usage.py

# Test batch processing
python examples/batch_processing.py

# Test duplicate detection
python examples/duplicate_detection.py
```

## 📊 Performance Considerations

- **Rate Limiting**: Built-in delays prevent API rate limit issues
- **Token Management**: Content is automatically truncated to stay within API limits
- **Batch Processing**: Process items in manageable batches to avoid timeouts
- **Error Recovery**: Comprehensive error handling with detailed logging

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- [Flask Content Processing API Template](https://github.com/example/flask-content-api)

## 💡 Use Cases

- **Content Migration**: Clean and translate content during migrations
- **Data Deduplication**: Remove duplicate articles from large datasets
- **Content Analysis**: Extract structured data from unstructured content
- **Multi-language Processing**: Translate and process content across languages
- **Quality Assurance**: Clean AI-generated or scraped content
