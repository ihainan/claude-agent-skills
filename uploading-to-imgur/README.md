# Uploading to Imgur - Claude Agent Skill

Upload images to Imgur and get shareable links. This skill enables Claude to upload images via Imgur API with full metadata support.

## Features

- ✅ Upload single or multiple images
- ✅ Anonymous upload (Client ID) or authenticated upload (Access Token)
- ✅ Complete JSON output with URLs, delete links, metadata
- ✅ Support for PNG, JPEG, GIF, BMP, WebP, TIFF
- ✅ Detailed error handling
- ✅ Rate limit: ~1,250 uploads/day

## Quick Start

### 1. Get Imgur Client ID

Visit https://api.imgur.com/oauth2/addclient and register an application.

See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed guide.

### 2. Configure

Set environment variable:

```bash
export IMGUR_CLIENT_ID="your_client_id_here"
```

Or edit `scripts/config.json`:

```json
{
  "client_id": "your_client_id_here"
}
```

### 3. Upload

```bash
python scripts/upload.py image.png
```

## Installation

### Install to Claude Code

Copy this skill to Claude Code's skills directory:

```bash
# User-level (available in all projects)
cp -r uploading-to-imgur ~/.claude/skills/

# Project-level (current project only)
cp -r uploading-to-imgur .claude/skills/
```

### Configure credentials

```bash
# Method 1: Environment variable (recommended)
echo 'export IMGUR_CLIENT_ID="your_client_id"' >> ~/.bashrc
source ~/.bashrc

# Method 2: Edit config file
vim ~/.claude/skills/uploading-to-imgur/scripts/config.json
```

## Usage with Claude Agent SDK

Once installed, Claude will automatically use this skill when you ask to upload images:

**Python:**
```python
from claude_agent_sdk import query

async for message in query({
    "prompt": "Upload these screenshots to Imgur",
    "options": {
        "settingSources": ["user", "project"]  # Required to load skills
    }
}):
    print(message)
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Upload this image to Imgur and give me the link",
  options: {
    settingSources: ["user", "project"]
  }
})) {
  console.log(message);
}
```

## Manual Usage

You can also use the scripts directly:

```bash
# Upload single image
python scripts/upload.py photo.png

# Upload multiple images
python scripts/upload.py img1.png img2.jpg img3.gif

# Save results to JSON
python scripts/upload.py photo.png --output result.json --pretty

# Use specific Client ID
python scripts/upload.py photo.png --client-id "your_client_id"

# Authenticated upload (to your account)
python scripts/upload.py photo.png --access-token "your_access_token"
```

## Directory Structure

```
uploading-to-imgur/
├── SKILL.md              # Main skill documentation
├── AUTHENTICATION.md     # How to get credentials
├── EXAMPLES.md           # Usage examples
├── README.md             # This file
└── scripts/
    ├── upload.py         # Main upload script
    ├── get_token.py      # Helper to get Access Token
    ├── config.json       # Configuration file
    └── config.json.example  # Configuration template
```

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[AUTHENTICATION.md](AUTHENTICATION.md)** - Get your Imgur credentials
- **[EXAMPLES.md](EXAMPLES.md)** - Usage examples and patterns

## Output Format

The script returns JSON with complete upload information:

```json
{
  "total": 1,
  "successful": 1,
  "failed": 0,
  "uploads": [
    {
      "original_path": "photo.png",
      "filename": "photo.png",
      "success": true,
      "upload_type": "anonymous",
      "imgur_data": {
        "id": "abc123",
        "link": "https://i.imgur.com/abc123.png",
        "delete_link": "https://imgur.com/delete/xyz789",
        "width": 1920,
        "height": 1080,
        "size": 256789,
        "type": "image/png"
      }
    }
  ]
}
```

## Authentication Methods

### Anonymous Upload (Client ID)

Default method. Images are not associated with your account.

**Pros:**
- Simple setup
- Never expires
- No account management

**Cons:**
- Can only delete via delete link
- Cannot manage in Imgur account

### Authenticated Upload (Access Token)

Upload to your Imgur account.

**Pros:**
- Images appear in your account
- Manage via Imgur web interface
- Edit metadata

**Cons:**
- Token expires in 28 days
- More complex OAuth setup

See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed setup.

## Testing

Test the skill:

```bash
# Set your Client ID
export IMGUR_CLIENT_ID="your_client_id"

# Test upload
python scripts/upload.py test_image.png

# Test multiple uploads
python scripts/upload.py img1.png img2.png --output test.json --pretty
```

## Troubleshooting

**Problem:** "No Imgur authentication found"

**Solution:** Set environment variable or edit config.json with your Client ID.

**Problem:** "Invalid client_id"

**Solution:** Check your Client ID at https://imgur.com/account/settings/apps

**Problem:** "Rate limit exceeded"

**Solution:** You've hit the daily limit (1,250 uploads). Wait until tomorrow.

See [AUTHENTICATION.md](AUTHENTICATION.md) for more troubleshooting.

## Requirements

- Python 3.6+
- `requests` library (usually pre-installed)

Install dependencies if needed:
```bash
pip install requests
```

## Rate Limits

- **~1,250 uploads per day**
- **~12,500 API requests per day**

Sufficient for most personal use cases.

## Security

- Never commit `config.json` with real credentials
- Use environment variables for production
- Keep delete links private
- Regenerate credentials if compromised

## License

This skill is provided as-is for use with Claude Agent SDK.

## Support

For issues with:
- **This skill**: Check documentation in this directory
- **Imgur API**: Visit https://imgur.com/account/settings/apps
- **Claude Agent SDK**: Visit https://platform.claude.com/docs

## Version

Version: 1.0.0
Created: 2025-12-18
Compatible with: Claude Agent SDK v1.0+
