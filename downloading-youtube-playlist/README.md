# Downloading YouTube Playlist Skill

An Agent Skill for downloading YouTube playlist videos with full control over quality, range, and subtitle options.

## Overview

This skill enables Claude to download videos from YouTube playlists using the powerful yt-dlp tool. It supports:

- Downloading entire playlists or specific video ranges
- Quality selection (from 4K to lowest quality)
- Automatic subtitle downloading and embedding
- Resume capability for interrupted downloads
- Progress tracking and error handling

## Prerequisites

This skill requires two command-line tools to be installed:

### 1. yt-dlp

yt-dlp is a powerful YouTube downloader with extensive format support.

**Installation methods:**

**macOS (recommended: Homebrew)**
```bash
brew install yt-dlp
```

**macOS (alternative: pip)**
```bash
pip3 install yt-dlp
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install yt-dlp
```

**Linux (alternative: pip)**
```bash
pip3 install yt-dlp
```

**Windows (recommended: pip)**
```bash
pip install yt-dlp
```

**Windows (alternative: Chocolatey)**
```bash
choco install yt-dlp
```

**Verify installation:**
```bash
yt-dlp --version
```

You should see output like: `2024.12.06` or similar version number.

### 2. ffmpeg

ffmpeg is required for merging video and audio streams and embedding subtitles.

**macOS (Homebrew)**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Linux (Fedora)**
```bash
sudo dnf install ffmpeg
```

**Windows (Chocolatey)**
```bash
choco install ffmpeg
```

**Windows (Scoop)**
```bash
scoop install ffmpeg
```

**Windows (manual download)**
1. Download from https://www.gyan.dev/ffmpeg/builds/
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add `C:\ffmpeg\bin` to your PATH environment variable

**Verify installation:**
```bash
ffmpeg -version
```

You should see ffmpeg version information and configuration details.

## Quick start

Once dependencies are installed, you can start downloading:

```bash
# Download entire playlist
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"

# Download specific range
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID" \
  --start 1 \
  --end 10 \
  --output "./my_videos"
```

## Features

### Automatic subtitle handling

The script automatically:
- Downloads available manual subtitles in Chinese (Simplified/Traditional) and English
- Falls back to auto-generated subtitles if manual ones are unavailable
- Embeds subtitles into the video file (not as separate files)

### Smart file naming

Videos are saved with a clear naming pattern:
```
{playlist_index} - {video_title}.mp4
```

Examples:
- `1 - Introduction to Python.mp4`
- `2 - Variables and Data Types.mp4`
- `10 - Advanced Functions.mp4`

### Resume capability

If a download is interrupted:
- yt-dlp automatically skips already-downloaded videos
- Partially downloaded videos are resumed from where they stopped
- Simply run the same command again to continue

### Quality options

Choose from various quality presets:

```bash
# Best available quality (default)
--quality "best"

# Limit to 1080p
--quality "bestvideo[height<=1080]+bestaudio/best"

# Limit to 720p (good balance of quality and size)
--quality "bestvideo[height<=720]+bestaudio/best"

# Limit to 480p (smaller files)
--quality "bestvideo[height<=480]+bestaudio/best"

# Worst quality (fastest download, smallest files)
--quality "worst"
```

## Usage guide

### Command-line arguments

**Required:**
- `--url` or `-u`: YouTube playlist URL

**Optional:**
- `--start` or `-s`: First video to download (default: 1)
- `--end` or `-e`: Last video to download (default: 38)
- `--output` or `-o`: Output directory (default: current directory)
- `--quality` or `-q`: Quality setting (default: "best")

### Common use cases

See [EXAMPLES.md](EXAMPLES.md) for detailed examples of:
- Downloading specific video ranges
- Quality optimization
- Organizing downloads
- Batch downloading multiple playlists
- Real-world scenarios (courses, music, podcasts)

## Troubleshooting

### "Command not found: yt-dlp"

**Problem**: yt-dlp is not installed or not in PATH.

**Solution**:
1. Install yt-dlp using one of the methods above
2. Verify with `yt-dlp --version`
3. If installed but not found, check your PATH environment variable

### "Command not found: ffmpeg"

**Problem**: ffmpeg is not installed or not in PATH.

**Solution**:
1. Install ffmpeg using one of the methods above
2. Verify with `ffmpeg -version`
3. On Windows, ensure ffmpeg is added to PATH

### Downloads are very slow

**Possible causes**:
- Slow internet connection
- YouTube server throttling
- High quality setting

**Solutions**:
- Use lower quality setting (e.g., 720p instead of 1080p)
- Download during off-peak hours
- Check your internet speed with a speed test

### "ERROR: This video is unavailable"

**Possible causes**:
- Video is geo-restricted
- Video is private or deleted
- Video is age-restricted

**Solutions**:
- yt-dlp will skip unavailable videos and continue with the rest
- Check the video manually in a browser
- Some restrictions can be bypassed with VPN (use responsibly)

### Running out of disk space

**Problem**: Large playlists can consume significant disk space.

**Solutions**:
1. Check available disk space: `df -h` (Linux/macOS) or `dir` (Windows)
2. Use lower quality setting to reduce file sizes
3. Download in smaller batches (e.g., 10 videos at a time)
4. Delete unnecessary files to free up space

**Storage estimates**:
- 4K quality: 2-5 GB per hour of video
- 1080p quality: 500 MB - 1 GB per hour
- 720p quality: 200-400 MB per hour
- 480p quality: 100-200 MB per hour

### "Permission denied" when writing files

**Problem**: No write permission for output directory.

**Solutions**:
- Choose a different output directory where you have write permissions
- On Linux/macOS: Use a directory in your home folder
- On Windows: Ensure you're not trying to write to a protected system folder

### Downloads keep failing

**Problem**: Network interruptions or unstable connection.

**Solutions**:
- yt-dlp has built-in retry logic, but you can re-run the command to resume
- Use a wired connection instead of Wi-Fi if possible
- Try downloading during a more stable network time
- Download in smaller batches

### Subtitles are not embedded

**Problem**: ffmpeg might not be working correctly.

**Solutions**:
1. Verify ffmpeg is installed: `ffmpeg -version`
2. Ensure ffmpeg is in your PATH
3. Try re-running the download command
4. Check yt-dlp output for subtitle-related errors

### Update outdated yt-dlp

YouTube frequently changes, so keep yt-dlp updated:

```bash
# Using pip
pip3 install --upgrade yt-dlp

# Using Homebrew (macOS)
brew upgrade yt-dlp

# Using apt (Linux)
sudo apt update && sudo apt upgrade yt-dlp
```

## Performance optimization

### Speed up downloads

1. **Use lower quality**: 720p downloads 30-50% faster than 1080p
2. **Download during off-peak hours**: Less YouTube server load
3. **Close bandwidth-intensive applications**: Browser, streaming services
4. **Use wired connection**: More stable than Wi-Fi

### Save disk space

1. **Use 720p for most content**: Good quality-to-size ratio
2. **Use 480p for podcasts/talk content**: Video quality less important
3. **Download only needed range**: Use `--start` and `--end` wisely
4. **Clean up old downloads**: Remove videos after watching

### Parallel downloads

For multiple playlists, download in parallel (use separate terminal windows):

```bash
# Terminal 1
python scripts/download.py --url "PLAYLIST_1_URL" --output "./playlist1"

# Terminal 2
python scripts/download.py --url "PLAYLIST_2_URL" --output "./playlist2"

# Terminal 3
python scripts/download.py --url "PLAYLIST_3_URL" --output "./playlist3"
```

**Note**: Ensure sufficient bandwidth and CPU capacity.

## Best practices

### 1. Test with small range first

Before downloading a large playlist, test with a small range:

```bash
python scripts/download.py \
  --url "YOUR_PLAYLIST_URL" \
  --start 1 \
  --end 2
```

This verifies the playlist URL and settings work correctly.

### 2. Organize by category

Use descriptive output directories:

```bash
--output "./Courses/Python_Tutorial"
--output "./Music/Jazz_Classics"
--output "./Documentaries/Science"
```

### 3. Choose appropriate quality

- **Courses/tutorials**: 720p is sufficient and saves space
- **Movies/cinematography**: 1080p or higher for quality
- **Podcasts/talks**: 480p or even audio-only formats

### 4. Monitor disk space

Check available space before large downloads:

```bash
# Linux/macOS
df -h

# Windows
dir
```

### 5. Keep dependencies updated

Update yt-dlp regularly to handle YouTube changes:

```bash
pip3 install --upgrade yt-dlp
```

## Limitations

### Technical limitations

- **Rate limiting**: YouTube may throttle downloads if too many are requested too quickly
- **Geo-restrictions**: Some videos may not be available in your region
- **Age restrictions**: Age-restricted content may require additional authentication
- **Private videos**: Cannot download private or unlisted videos you don't have access to

### Practical limitations

- **Time**: Large playlists take hours to download
- **Storage**: High-quality videos require significant disk space
- **Bandwidth**: Downloads consume significant bandwidth
- **Server availability**: YouTube server issues can interrupt downloads

## Legal and ethical considerations

### Fair use

- Download content you have the right to access
- Respect copyright and creator rights
- Use downloads for personal, non-commercial purposes
- Do not redistribute downloaded content

### Terms of service

Downloading YouTube content may violate YouTube's Terms of Service. This tool is provided for:
- Personal archival
- Offline viewing of content you would normally stream
- Educational purposes
- Accessibility needs

**Use responsibly and ethically.**

## Additional resources

- [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#readme)
- [ffmpeg documentation](https://ffmpeg.org/documentation.html)
- [EXAMPLES.md](EXAMPLES.md) - Detailed usage examples
- [SKILL.md](SKILL.md) - Skill overview and quick reference

## Support

For issues with:
- **This skill**: Check the troubleshooting section above
- **yt-dlp**: Visit [yt-dlp GitHub issues](https://github.com/yt-dlp/yt-dlp/issues)
- **ffmpeg**: Visit [ffmpeg documentation](https://ffmpeg.org/documentation.html)

## Version information

- **Skill version**: 1.0
- **Minimum yt-dlp version**: 2023.01.01 or later
- **Minimum ffmpeg version**: 4.0 or later
- **Python version**: 3.7 or later
