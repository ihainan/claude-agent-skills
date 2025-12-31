# Usage Examples

This document provides practical examples for common YouTube playlist download scenarios.

## Basic examples

### Example 1: Download entire playlist with default settings

Download all videos from a music playlist to the current directory:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
```

**Use case**: Quick download with best quality
**Expected time**: Depends on playlist size (e.g., 30 videos × 3 min/video ≈ 90 minutes)

### Example 2: Download first 5 videos

Download just the first 5 videos from a tutorial series:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --start 1 \
  --end 5
```

**Use case**: Preview a playlist or download specific episodes
**Expected time**: ~10-15 minutes for 5 videos

### Example 3: Download specific range

Download episodes 10-20 from a TV show playlist:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --start 10 \
  --end 20
```

**Use case**: Catch up on specific episodes
**Expected time**: ~30-45 minutes for 10 videos

## Quality and format examples

### Example 4: Download in 720p (faster, smaller files)

Download playlist with 720p quality limit:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --quality "bestvideo[height<=720]+bestaudio/best"
```

**Use case**: Save bandwidth and storage space
**File size**: ~200-400 MB per hour of content
**Expected time**: 30-50% faster than 1080p downloads

### Example 5: Download in 1080p (high quality)

Download playlist with 1080p quality limit:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --quality "bestvideo[height<=1080]+bestaudio/best"
```

**Use case**: Best quality for archival or viewing on large screens
**File size**: ~500-1000 MB per hour of content

### Example 6: Download lowest quality (fastest)

Download playlist in lowest quality for quick preview:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --quality "worst"
```

**Use case**: Quick preview or content analysis, not for watching
**File size**: ~50-100 MB per hour of content
**Expected time**: Very fast, 3-5x faster than best quality

## Organization examples

### Example 7: Download to organized directory structure

Download different playlists to separate folders:

```bash
# Download music playlist
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --output "./Music/Jazz_Classics"

# Download tutorial playlist
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLyyyyyy" \
  --output "./Tutorials/Python_Course"

# Download entertainment playlist
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLzzzzzz" \
  --output "./Entertainment/Comedy_Shows"
```

**Use case**: Organize content by category
**Result**: Clean directory structure for easy access

### Example 8: Download multiple playlists in parallel

Download multiple playlists simultaneously (in separate terminal windows or background):

```bash
# Terminal 1
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PL111111" \
  --output "./Course_1"

# Terminal 2
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PL222222" \
  --output "./Course_2"

# Terminal 3
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PL333333" \
  --output "./Course_3"
```

**Use case**: Download multiple playlists faster
**Note**: Ensure sufficient bandwidth and disk I/O

## Real-world scenarios

### Example 9: Download online course

Download a complete online course playlist:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLComplete_Course_ID" \
  --quality "bestvideo[height<=1080]+bestaudio/best" \
  --output "./Courses/Machine_Learning_2024"
```

**Use case**: Offline study, take notes while watching
**Expected result**: All lectures with subtitles embedded
**Estimated time**: 50-video course ≈ 2-3 hours download time

### Example 10: Download music album playlist

Download music videos from an album release:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLMusic_Album_ID" \
  --quality "bestvideo[height<=1080]+bestaudio/best" \
  --output "./Music/Artist_Name/Album_Name"
```

**Use case**: Create local music video collection
**Expected result**: All tracks in best audio quality

### Example 11: Download podcast episodes

Download specific podcast episodes from a playlist:

```bash
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLPodcast_Series_ID" \
  --start 50 \
  --end 60 \
  --quality "bestvideo[height<=720]+bestaudio/best" \
  --output "./Podcasts/Series_Name/Season_5"
```

**Use case**: Download recent episodes for commute listening
**Note**: 720p is sufficient for podcast videos

### Example 12: Batch download with shell script

Create a shell script to download multiple playlists with custom settings:

```bash
#!/bin/bash
# download_all_courses.sh

# Course 1: Beginner level
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLBeginner" \
  --output "./Courses/Beginner" \
  --quality "bestvideo[height<=720]+bestaudio/best"

# Course 2: Intermediate level
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLIntermediate" \
  --output "./Courses/Intermediate" \
  --quality "bestvideo[height<=1080]+bestaudio/best"

# Course 3: Advanced level
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLAdvanced" \
  --output "./Courses/Advanced" \
  --quality "bestvideo[height<=1080]+bestaudio/best"

echo "All courses downloaded successfully!"
```

**Use case**: Automate downloading of multiple related playlists
**How to use**: `chmod +x download_all_courses.sh && ./download_all_courses.sh`

## Tips and tricks

### Resuming interrupted downloads

If a download is interrupted, yt-dlp will automatically resume from where it left off when you run the same command again:

```bash
# Run this command again if interrupted
python scripts/download.py \
  --url "https://www.youtube.com/playlist?list=PLxxxxxx" \
  --output "./my_videos"
```

yt-dlp skips already-downloaded videos automatically.

### Checking playlist info before downloading

Get playlist information without downloading:

```bash
yt-dlp --flat-playlist "https://www.youtube.com/playlist?list=PLxxxxxx"
```

This shows the number of videos and titles without downloading.

### Estimating download time

Rough estimates:
- 1 video (1080p, 10 min): 2-4 minutes
- 10 videos (1080p): 20-40 minutes
- 50 videos (1080p): 2-3 hours
- 100 videos (1080p): 4-6 hours

Factors affecting speed:
- Your internet speed
- YouTube server speed
- Video quality setting
- Concurrent downloads from other applications

### Storage planning

Average file sizes per video hour:
- 4K quality: 2-5 GB/hour
- 1080p quality: 500 MB - 1 GB/hour
- 720p quality: 200-400 MB/hour
- 480p quality: 100-200 MB/hour
- Worst quality: 50-100 MB/hour

Plan disk space accordingly before downloading large playlists.

## Common patterns

### Pattern 1: Weekly content download

Download new episodes weekly from an ongoing series:

```bash
# Week 1: Download episodes 1-5
python scripts/download.py --url "..." --start 1 --end 5 --output "./Series"

# Week 2: Download episodes 6-10
python scripts/download.py --url "..." --start 6 --end 10 --output "./Series"

# Week 3: Download episodes 11-15
python scripts/download.py --url "..." --start 11 --end 15 --output "./Series"
```

### Pattern 2: Archive entire channel's playlists

Download all playlists from a creator systematically:

```bash
python scripts/download.py --url "https://www.youtube.com/playlist?list=PL_Playlist1" --output "./Creator/Series_1"
python scripts/download.py --url "https://www.youtube.com/playlist?list=PL_Playlist2" --output "./Creator/Series_2"
python scripts/download.py --url "https://www.youtube.com/playlist?list=PL_Playlist3" --output "./Creator/Series_3"
```

### Pattern 3: Quality-based archival strategy

Download recent videos in high quality, older videos in lower quality:

```bash
# Recent videos (high quality)
python scripts/download.py \
  --url "..." --start 1 --end 20 \
  --quality "bestvideo[height<=1080]+bestaudio/best" \
  --output "./Archive/Recent"

# Older videos (standard quality)
python scripts/download.py \
  --url "..." --start 21 --end 100 \
  --quality "bestvideo[height<=720]+bestaudio/best" \
  --output "./Archive/Older"
```

## Troubleshooting examples

### Issue: Download is very slow

Try lower quality:
```bash
python scripts/download.py \
  --url "..." \
  --quality "bestvideo[height<=480]+bestaudio/best"
```

### Issue: Running out of disk space

Check space before downloading and use lower quality or download in batches:
```bash
# Check disk space
df -h

# Download in smaller batches
python scripts/download.py --url "..." --start 1 --end 10
python scripts/download.py --url "..." --start 11 --end 20
```

### Issue: Some videos fail to download

yt-dlp will continue with the next video. Check the output log for specific error messages. Common causes:
- Geo-restricted content
- Deleted or private videos
- Age-restricted content
- Copyright restrictions

The script will skip failed videos and continue downloading the rest.
