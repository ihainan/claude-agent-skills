#!/usr/bin/env python3
"""
YouTube playlist video download script
Supports specifying playlist URL and download range
"""

import argparse
import subprocess
import sys
from pathlib import Path


def download_playlist(
    playlist_url: str,
    start_index: int = 1,
    end_index: int = 38,
    output_dir: str = ".",
    quality: str = "best",
    quiet: bool = False
):
    """
    Download videos from a YouTube playlist within a specified range

    Args:
        playlist_url: YouTube playlist URL
        start_index: Starting video index (1-based)
        end_index: Ending video index
        output_dir: Output directory
        quality: Video quality (best/worst or specific format)
        quiet: Quiet mode, reduces output (recommended for LLM/automation scenarios)
    """
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build yt-dlp command
    cmd = [
        "yt-dlp",
        "--playlist-start", str(start_index),
        "--playlist-end", str(end_index),
        "-o", f"{output_dir}/%(playlist_index)s - %(title)s.%(ext)s",
        "-f", quality,
        "--merge-output-format", "mp4",
        "--write-sub",  # Download subtitles
        "--sub-lang", "zh-Hans,zh-Hant,en",  # Chinese and English subtitles
        "--embed-subs",  # Embed subtitles
        "--write-auto-sub",  # Download auto-generated subtitles if manual ones unavailable
    ]

    # Quiet mode: reduce output but still show video titles and errors
    if quiet:
        cmd.extend([
            "--no-progress",  # Don't show progress bar
            "--console-title",  # Don't update console title
        ])

    cmd.append(playlist_url)

    print(f"Starting playlist download: {playlist_url}")
    print(f"Download range: videos {start_index} to {end_index}")
    print(f"Output directory: {output_path.absolute()}")
    print(f"Video quality: {quality}")
    if quiet:
        print(f"Mode: Quiet mode (reduced progress output)")
    print("-" * 60)

    if not quiet:
        print(f"Executing command: {' '.join(cmd)}")
        print("-" * 60)
    else:
        print("Download in progress, please wait...")
        print("Tip: You can monitor progress by checking the output directory")
        print("-" * 60)

    try:
        # Execute download command
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("Download complete!")
        print("=" * 60)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\nError: Download failed (exit code: {e.returncode})", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("\nError: yt-dlp command not found, please install yt-dlp first", file=sys.stderr)
        print("Installation: pip install yt-dlp", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Download videos from a YouTube playlist within a specified range",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download entire playlist
  %(prog)s -u "https://www.youtube.com/playlist?list=PLAYLIST_ID"

  # Download videos 1-10 from a playlist
  %(prog)s -u "https://www.youtube.com/playlist?list=PLAYLIST_ID" -s 1 -e 10

  # Download to a specific directory
  %(prog)s -u "https://www.youtube.com/playlist?list=PLAYLIST_ID" -o /path/to/output

  # Specify video quality
  %(prog)s -u "https://www.youtube.com/playlist?list=PLAYLIST_ID" -q "bestvideo[height<=1080]+bestaudio/best"

  # Quiet mode (recommended for LLM/automation scenarios, reduced output)
  %(prog)s -u "https://www.youtube.com/playlist?list=PLAYLIST_ID" --quiet
        """
    )

    parser.add_argument(
        "-u", "--url",
        required=True,
        help="YouTube playlist URL"
    )

    parser.add_argument(
        "-s", "--start",
        type=int,
        default=1,
        help="Starting video index (default: 1)"
    )

    parser.add_argument(
        "-e", "--end",
        type=int,
        default=38,
        help="Ending video index (default: 38)"
    )

    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory (default: current directory)"
    )

    parser.add_argument(
        "-q", "--quality",
        default="best",
        help="Video quality (default: best)"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Quiet mode: reduce output, only show video titles and errors (recommended for LLM/automation scenarios)"
    )

    args = parser.parse_args()

    # Validate parameters
    if args.start < 1:
        print("Error: Starting index must be >= 1", file=sys.stderr)
        return 1

    if args.end < args.start:
        print("Error: Ending index must be >= starting index", file=sys.stderr)
        return 1

    # Execute download
    return download_playlist(
        playlist_url=args.url,
        start_index=args.start,
        end_index=args.end,
        output_dir=args.output,
        quality=args.quality,
        quiet=args.quiet
    )


if __name__ == "__main__":
    sys.exit(main())
