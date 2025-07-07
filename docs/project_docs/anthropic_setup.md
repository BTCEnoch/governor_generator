# Anthropic Claude API Setup Guide

## Prerequisites

1. **Get an Anthropic API Key**
   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Create an account or sign in
   - Generate an API key

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Override the default model (defaults to claude-3-5-sonnet-20241022)
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
# ANTHROPIC_MODEL=claude-3-5-haiku-20241022
# ANTHROPIC_MODEL=claude-3-opus-20240229
```

### Available Models

- **claude-3-5-sonnet-20241022** (default) - Best balance of intelligence and speed
- **claude-3-5-haiku-20241022** - Fastest and most cost-effective
- **claude-3-opus-20240229** - Most intelligent, but slower and more expensive

## Usage

Run the governor generator:

```bash
python generate_governor_jsons.py
```

## Key Differences from OpenAI

1. **System Messages**: Anthropic handles system messages differently (as a separate parameter)
2. **Response Format**: Claude returns content as a list with text objects
3. **Rate Limits**: Different rate limiting structure
4. **Pricing**: Generally more cost-effective for longer conversations

## Benefits of Using Claude

- **Better at following complex instructions**
- **More nuanced understanding of context**
- **Excellent at creative writing and character development**
- **Better at maintaining consistent tone and personality**
- **More cost-effective for longer prompts**

Perfect for generating detailed governor personalities! 