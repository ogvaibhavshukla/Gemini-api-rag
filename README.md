# YouTube Channel RAG Tool

A powerful tool that lets you chat with YouTube channel videos using AI! This tool scrapes video transcripts from any YouTube channel and creates a searchable knowledge base using Google's Gemini API with file search capabilities.

## Features

- 🎬 Scrape videos from any YouTube channel (newest to oldest)
- 📝 Extract video titles, descriptions, and transcripts/subtitles
- 🤖 Upload transcripts to Gemini API for semantic search
- 💬 Interactive chat interface to ask questions about video content
- 🔍 Powered by Gemini's file search for accurate RAG responses

## Prerequisites

Before you begin, you'll need:

1. **Python 3.8+** installed on your system
2. **Gemini API Key** - Get it from [Google AI Studio](https://aistudio.google.com/app/apikey)
3. **Apify API Token** - Get it from [Apify Console](https://console.apify.com/account/integrations)

## Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   APIFY_API_TOKEN=your_apify_api_token_here
   ```

## Usage

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Enter the YouTube channel URL**

   You'll be prompted to enter a YouTube channel URL. Examples:
   - `https://www.youtube.com/@channelname`
   - `https://www.youtube.com/c/channelname`
   - `https://www.youtube.com/channel/UCxxxxx`

3. **Specify how many videos to process**

   Enter the number of videos you want to scrape (from newest to oldest).
   - Recommended: 5-20 videos for faster processing
   - Note: Only videos with available transcripts/subtitles will be processed

4. **Wait for processing**

   The tool will:
   - Scrape the specified videos from the channel
   - Extract transcripts and metadata
   - Upload them to Gemini file search
   - Prepare the chat interface

5. **Chat with the videos!**

   Once processing is complete, you can ask questions like:
   - "What are the main topics covered in these videos?"
   - "Summarize the video about [topic]"
   - "What did the creator say about [subject]?"
   - "Compare the approaches discussed in different videos"

## Chat Commands

While in the chat interface, you can use:

- `help` - Show available commands
- `info` - Display file search store information
- `exit`, `quit`, or `q` - Exit the chat

## How It Works

1. **Scraping**: Uses Apify's YouTube scraper to fetch video metadata and transcripts
2. **Processing**: Formats each video's transcript with metadata into a structured document
3. **Indexing**: Uploads documents to Gemini's file search store with optimized chunking
4. **Querying**: Uses Gemini 2.0 Flash with file search to answer questions based on the transcripts

## Project Structure

```
.
├── main.py              # Main application entry point
├── youtube_scraper.py   # YouTube scraping logic using Apify
├── gemini_manager.py    # Gemini API file search integration
├── chat_interface.py    # Interactive chat interface
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your API keys (gitignored)
└── README.md           # This file
```

## Limitations

- Only works with videos that have transcripts/subtitles available
- Apify free tier has usage limits - check [Apify pricing](https://apify.com/pricing)
- Gemini API has file storage limits based on tier (1GB free tier)
- Processing large numbers of videos may take time

## Troubleshooting

### "No transcripts available"
- Not all videos have transcripts. Try a different channel or fewer videos
- Some channels disable automatic captions
- Videos without captions are skipped automatically (the Actor does not charge for them)

### "Actor run failed"
- Check your Apify API token is valid
- Ensure you have sufficient Apify credits
- Verify the channel URL is correct

### "API key error"
- Verify your Gemini API key is correct in `.env`
- Check your API quota at [Google AI Studio](https://aistudio.google.com/)

## References

- [Gemini File Search Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- [Apify Documentation](https://docs.apify.com/)
- [YouTube Transcript Scraper Actor](https://apify.com/shephouse/youtube-transcript-scraper-bulk)

## License

MIT License - feel free to use and modify as needed!

## Support

If you encounter any issues or have questions, please check:
1. Your API keys are correctly set in `.env`
2. You have sufficient credits/quota for both APIs
3. The YouTube channel URL is valid and accessible
4. Videos have transcripts available
