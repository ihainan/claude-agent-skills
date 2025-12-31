---
name: downloading-youtube-playlist
description: Download videos from YouTube playlists with support for range selection, quality settings, and subtitle embedding. Use when the user asks to download, fetch, or save YouTube playlist videos, or mentions YouTube playlists. Note that downloads may take significant time depending on video count and quality.
---

# Downloading YouTube Playlist

Download videos from YouTube playlists using yt-dlp with full control over video range, quality, and subtitle options.

## Important notes

**Long-running operation**: Downloading videos can take considerable time:
- Single video (1080p): 2-5 minutes
- Small playlist (5-10 videos): 10-30 minutes
- Large playlist (20+ videos): 30+ minutes to several hours

**Verbose logging warning**: yt-dlp produces EXTENSIVE real-time progress output with frequent updates for each video:
- Download percentage updates (every few seconds)
- Speed and ETA information
- Multiple lines per second during active download
- Total output can be thousands of lines for large playlists

**CRITICAL: Recommended execution approach**:

1. **Use run_in_background for downloads** (STRONGLY RECOMMENDED):
   ```bash
   # Run download in background and redirect verbose output
   python scripts/download.py --url "..." --output "./videos" > download.log 2>&1
   ```
   Then periodically check the log file or output directory to monitor progress.

2. **Use quiet mode** (RECOMMENDED):
   ```bash
   # Add --quiet flag to suppress detailed progress output
   python scripts/download.py --url "..." --quiet
   ```
   This still shows video titles and errors, but suppresses per-second progress updates.

3. **Check completion by listing output directory**:
   ```bash
   # After starting download, periodically check what's been downloaded
   ls -lh ./output_directory/
   ```

**DO NOT** watch the full real-time output unless:
- Debugging a specific download issue
- Downloading only 1-2 videos
- User explicitly requests to see detailed progress

**Progress monitoring best practice**:
- Start the download in background or quiet mode
- Inform user the download has started
- Periodically check output directory to report progress
- Check for completion by examining the final video count

**Automatic skip of downloaded content**: yt-dlp intelligently handles existing files:
- **Already-downloaded videos are automatically skipped** - no re-download or bandwidth waste
- **Partially downloaded files are resumed** from where they stopped
- **Safe to re-run the same command** - interrupted downloads will continue seamlessly
- **No duplicate downloads** - each video is downloaded only once even if command is run multiple times

This means you can safely re-run a download command after interruptions without worrying about downloading videos again.

**Dependencies required**: This skill requires `yt-dlp` and `ffmpeg` to be installed. See [README.md](README.md) for installation instructions.

## Quick start

### Download entire playlist

Download all videos from a playlist to the current directory:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Download specific range

Download videos 1-10 from a playlist:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
  --start 1 \
  --end 10
```

### Download to custom directory

Download videos to a specific folder:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
  --output "./my_videos"
```

### Resume interrupted downloads

If a download is interrupted (network issue, user cancellation, etc.), simply re-run the exact same command:

```bash
# Run this command again - already downloaded videos will be skipped
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
  --output "./my_videos"
```

yt-dlp automatically:
- Skips fully downloaded videos (no re-download)
- Resumes partially downloaded videos from where they stopped
- Continues with remaining videos in the playlist

## Configuration

### Video quality

Specify video quality with `--quality`:

```bash
# Best quality (default)
python scripts/download.py --url "..." --quality "best"

# Limit to 1080p
python scripts/download.py --url "..." --quality "bestvideo[height<=1080]+bestaudio/best"

# Limit to 720p
python scripts/download.py --url "..." --quality "bestvideo[height<=720]+bestaudio/best"

# Worst quality (fastest download)
python scripts/download.py --url "..." --quality "worst"
```

### Subtitle options

The script automatically:
- Downloads available subtitles (Chinese Simplified, Chinese Traditional, English)
- Downloads auto-generated subtitles if manual ones are not available
- Embeds subtitles into the video file

All videos are saved in MP4 format with naming pattern: `{playlist_index} - {title}.mp4`

## Command reference

### download.py

Main playlist download script.

**Required arguments:**
- `--url` or `-u`: YouTube playlist URL

**Optional arguments:**
- `--start` or `-s`: Starting video index (default: 1)
- `--end` or `-e`: Ending video index (default: 38)
- `--output` or `-o`: Output directory (default: current directory)
- `--quality` or `-q`: Video quality setting (default: "best")
- `--quiet`: Quiet mode - suppresses verbose progress output (RECOMMENDED for LLM usage)

**Examples:**

Basic download with quiet mode (RECOMMENDED):
```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --quiet
```

Download specific range with quality limit:
```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --start 5 \
  --end 15 \
  --quality "bestvideo[height<=720]+bestaudio/best" \
  --output "./downloads" \
  --quiet
```

## Use cases

### Educational content archival
- Download course playlists for offline study
- Archive tutorial series
- Save lectures for reference

### Content backup
- Backup your own YouTube playlists
- Preserve playlists that might be deleted
- Create local copies of important content

### Batch processing
- Download specific episodes from a series
- Get recent uploads from a playlist
- Archive multiple playlists systematically

## Error handling

The script handles common errors:
- **Missing dependencies**: Shows installation instructions if yt-dlp or ffmpeg are not found
- **Invalid URL**: Reports if playlist URL is malformed
- **Network errors**: yt-dlp automatically retries failed downloads
- **Invalid range**: Validates that start index <= end index
- **Permission errors**: Reports if output directory is not writable

Check script output for detailed error messages and progress information.

## Performance tips

1. **Parallel downloads**: For multiple playlists, run separate commands in parallel
2. **Quality vs speed**: Lower quality settings download significantly faster
3. **Disk space**: Ensure sufficient disk space (1080p videos: ~100-500 MB each)
4. **Network**: Stable high-speed connection recommended for large playlists

## Limitations

- Requires active internet connection
- Download speed depends on YouTube servers and your network
- Some videos may be geo-restricted or unavailable
- Very large playlists (100+ videos) may take several hours

## Advanced usage

For more examples and advanced use cases, see [EXAMPLES.md](EXAMPLES.md).

For dependency installation and troubleshooting, see [README.md](README.md).
