# Claude Code Skills

This repository contains Claude Code skills for various tasks including image generation, image upload, and GitHub data fetching.

## Skills

### 1. generating-images

AI-powered image generation via OpenRouter API.

**Features:**
- Text-to-image generation from prompts
- Image-to-image generation with reference images
- Customizable aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4)
- Multiple AI model support

**Quick start:**
```bash
export OPENROUTER_API_KEY="sk-or-v1-YOUR_API_KEY_HERE"
python generating-images/scripts/generate.py --prompt "A serene landscape" --output result.png
```

See [generating-images/SKILL.md](generating-images/SKILL.md) for detailed documentation.

### 2. uploading-to-imgur

Upload images to Imgur and get shareable links.

**Features:**
- Single or batch image uploads
- Anonymous and authenticated upload modes
- Returns shareable URLs with metadata
- Multiple image format support (PNG, JPEG, GIF, BMP, WebP, TIFF)

**Quick start:**
```bash
export IMGUR_CLIENT_ID="your_client_id"
python uploading-to-imgur/scripts/upload.py image.png
```

See [uploading-to-imgur/SKILL.md](uploading-to-imgur/SKILL.md) for detailed documentation.

### 3. fetching-github-user-data

Fetch comprehensive GitHub user data through the GitHub API.

**Features:**
- User profile and basic information
- All public repositories with detailed statistics
- Contributions calendar and activity tracking
- Pull requests and issues analysis
- Programming language statistics
- Social connections (followers, following, organizations)
- Gists and starred repositories

**Quick start:**
```bash
# Without token (public data only)
python fetching-github-user-data/scripts/fetch.py torvalds

# With GitHub token (recommended, includes contribution calendar)
export GITHUB_TOKEN="ghp_YOUR_TOKEN"
python fetching-github-user-data/scripts/fetch.py torvalds
```

See [fetching-github-user-data/SKILL.md](fetching-github-user-data/SKILL.md) for detailed documentation.

## Setup

Skills use environment variables for authentication:

- **generating-images**: Set `OPENROUTER_API_KEY` environment variable
- **uploading-to-imgur**: Set `IMGUR_CLIENT_ID` environment variable
- **fetching-github-user-data**: Set `GITHUB_TOKEN` environment variable (optional but recommended)

Refer to each skill's documentation for detailed setup instructions.

## Documentation

Each skill directory contains:
- `SKILL.md` - Main documentation
- `EXAMPLES.md` - Usage examples
- Additional guides as needed
