# YouTube Transcript Extractor

Extract and analyze transcripts from YouTube videos for reference, summarization, and content creation.

## Usage

### Fetch Transcript from URL

```bash
python3 {baseDir}/scripts/get_transcript.py <youtube_url>
```

Examples:
```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=z5bgiFuBY_g"
```

### Output
- Saves transcript to `transcripts/VIDEO_ID.txt`
- Returns full text for analysis

## Use Cases

1. **Reference for Content Scripts**
   - Extract NotebookLM video transcripts
   - Use as tone/style reference for AdugboInsure scripts
   - Understand target language level and structure

2. **Content Analysis**
   - Summarize video content
   - Extract key points and messaging
   - Identify effective phrases or structures

3. **Quality Assurance**
   - Compare generated scripts to reference videos
   - Ensure tone and messaging consistency

## Dependencies

- `yt-dlp` — YouTube video and subtitle extraction
- Python 3.10+

## Notes

- Works with auto-generated subtitles if manual captions unavailable
- Requires public YouTube access
- Saved transcripts stored in `transcripts/` directory

## Examples

### Get Transcript from Your AdugboInsure Videos
```bash
python3 {baseDir}/scripts/get_transcript.py "https://youtu.be/WJiqZKBv7ls"
```

### Analyze NotebookLM Video
```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=z5bgiFuBY_g"
```
