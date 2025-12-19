# Usage Examples

Common use cases and practical examples for uploading images to Imgur.

## Basic Examples

### Example 1: Upload a single image

```bash
python scripts/upload.py photo.png
```

Output:
```
Upload mode: anonymous
Uploading 1 image(s) to Imgur...

Uploading: photo.png... ✓ Success

============================================================
Upload Summary: 1 succeeded, 0 failed
============================================================

photo.png:
  Link:   https://i.imgur.com/abc123.png
  Delete: https://imgur.com/delete/xyz789
```

### Example 2: Upload multiple images

```bash
python scripts/upload.py image1.png image2.jpg image3.gif
```

Returns links for all three images.

### Example 3: Save results to JSON

```bash
python scripts/upload.py photo.png --output result.json --pretty
```

Creates `result.json` with detailed upload information.

---

## Workflow Examples

### Example 4: Screenshot sharing workflow

Upload screenshots and get shareable links:

```bash
# Take screenshot (macOS)
screencapture -i screenshot.png

# Upload to Imgur
python scripts/upload.py screenshot.png

# Link is printed to console, ready to share
```

### Example 5: Batch processing workflow

Upload all images from a directory:

```bash
# Upload all PNG files
python scripts/upload.py images/*.png --output results.json

# Upload all images (multiple formats)
python scripts/upload.py photos/*.{png,jpg,jpeg,gif}
```

### Example 6: Automated backup workflow

Save important images with organized results:

```bash
#!/bin/bash
# backup_to_imgur.sh

DATE=$(date +%Y-%m-%d)
OUTPUT="imgur_backup_${DATE}.json"

python scripts/upload.py \
  backup_folder/*.png \
  --output "$OUTPUT" \
  --pretty

echo "Backup saved to $OUTPUT"
```

---

## Advanced Examples

### Example 7: Using specific Client ID

Override environment variable:

```bash
python scripts/upload.py image.png \
  --client-id "abc123def456"
```

### Example 8: Authenticated upload

Upload to your Imgur account:

```bash
# Set Access Token
export IMGUR_ACCESS_TOKEN="your_token_here"

# Upload
python scripts/upload.py profile_photo.png
```

Images will appear in your Imgur account.

### Example 9: Process JSON output with jq

Extract specific information:

```bash
# Get all image links
python scripts/upload.py *.png --output result.json
cat result.json | jq -r '.uploads[].imgur_data.link'

# Get only successful uploads
cat result.json | jq '.uploads[] | select(.success == true)'

# Count successful/failed
cat result.json | jq '{successful: .successful, failed: .failed}'
```

### Example 10: Error handling in scripts

```bash
#!/bin/bash
# smart_upload.sh

if python scripts/upload.py "$@"; then
  echo "✓ All uploads successful"
else
  echo "✗ Some uploads failed, check output"
  exit 1
fi
```

---

## Integration Examples

### Example 11: Integration with image generation

Combine with image generation and upload:

```bash
# Generate image
python scripts/generate.py --prompt "sunset landscape" --output generated.png

# Upload to Imgur
python scripts/upload.py generated.png

# Result: shareable link to generated image
```

### Example 12: Markdown documentation

Generate markdown with Imgur links:

```bash
# Upload images
python scripts/upload.py img1.png img2.png --output links.json

# Extract links and create markdown
cat links.json | jq -r '.uploads[] | "![\(.filename)](\(.imgur_data.link))"'
```

Output:
```markdown
![img1.png](https://i.imgur.com/abc123.png)
![img2.png](https://i.imgur.com/def456.png)
```

### Example 13: Slack/Discord integration

Upload and share in chat:

```bash
#!/bin/bash
# share_to_slack.sh

IMAGE=$1
OUTPUT=$(python scripts/upload.py "$IMAGE" --output /tmp/imgur.json)
LINK=$(cat /tmp/imgur.json | jq -r '.uploads[0].imgur_data.link')

# Post to Slack (using webhook)
curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"New image: $LINK\"}" \
  YOUR_SLACK_WEBHOOK_URL
```

---

## Troubleshooting Examples

### Example 14: Check which files failed

```bash
python scripts/upload.py *.png --output result.json --pretty

# View failed uploads
cat result.json | jq '.uploads[] | select(.success == false)'
```

### Example 15: Retry failed uploads

```bash
# Get list of failed files
FAILED=$(cat result.json | jq -r '.uploads[] | select(.success == false) | .original_path')

# Retry them
python scripts/upload.py $FAILED
```

### Example 16: Test with a small image first

```bash
# Create a small test image (requires ImageMagick)
convert -size 100x100 xc:blue test.png

# Upload test image
python scripts/upload.py test.png

# If successful, upload real images
python scripts/upload.py real_images/*.png
```

---

## Output Format Examples

### Example 17: Minimal output

Just get the links:

```bash
python scripts/upload.py image.png 2>/dev/null | \
  grep -o 'https://i.imgur.com/[^[:space:]]*'
```

### Example 18: Pretty JSON output

```bash
python scripts/upload.py image.png --output - --pretty
```

Prints to stdout instead of file.

### Example 19: CSV format conversion

```bash
# Upload and convert to CSV
python scripts/upload.py *.png --output result.json

# Convert JSON to CSV
cat result.json | jq -r '.uploads[] |
  [.filename, .success, .imgur_data.link // "N/A", .error // ""] |
  @csv'
```

Output:
```csv
"image1.png",true,"https://i.imgur.com/abc.png",""
"image2.png",false,"N/A","File not found"
```

---

## Real-World Scenarios

### Example 20: Blog post images

Upload all images for a blog post:

```bash
# Upload images
python scripts/upload.py blog_post_images/*.png \
  --output blog_images.json \
  --pretty

# Generate HTML img tags
cat blog_images.json | jq -r '.uploads[] |
  "<img src=\"\(.imgur_data.link)\" alt=\"\(.filename)\">"'
```

### Example 21: Portfolio website

Upload portfolio pieces and organize links:

```bash
#!/bin/bash
# upload_portfolio.sh

# Create organized JSON structure
echo '{"projects": []}' > portfolio.json

for dir in project_*/; do
  PROJECT=$(basename "$dir")
  python scripts/upload.py "$dir"/*.png --output "/tmp/${PROJECT}.json"

  # Merge into portfolio.json
  # (using jq to combine)
done

echo "Portfolio images uploaded and organized in portfolio.json"
```

### Example 22: GitHub issue attachments

Upload images for GitHub issues:

```bash
# Upload screenshot
python scripts/upload.py bug_screenshot.png

# Output:
# Link: https://i.imgur.com/abc123.png

# Paste link directly in GitHub issue markdown:
# ![Bug screenshot](https://i.imgur.com/abc123.png)
```

---

## Tips and Best Practices

### Tip 1: Save delete links

```bash
# Save links to a file for later reference
python scripts/upload.py *.png --output uploads_$(date +%Y%m%d).json

# Later, if you need to delete:
cat uploads_20250101.json | jq -r '.uploads[].imgur_data.delete_link'
```

### Tip 2: Check before uploading large batches

```bash
# Count files first
echo "Found $(ls *.png | wc -l) images"

# Check total size
du -sh *.png

# Then upload if reasonable
python scripts/upload.py *.png
```

### Tip 3: Use descriptive output filenames

```bash
python scripts/upload.py \
  vacation_photos/*.jpg \
  --output vacation_imgur_links_$(date +%Y-%m-%d).json
```

### Tip 4: Verify uploads

```bash
# Upload
python scripts/upload.py image.png --output result.json

# Verify by downloading
LINK=$(cat result.json | jq -r '.uploads[0].imgur_data.link')
curl -I "$LINK"  # Check if accessible
```

### Tip 5: Environment-specific configs

```bash
# Development
export IMGUR_CLIENT_ID="dev_client_id"

# Production
export IMGUR_CLIENT_ID="prod_client_id"

# Script uses appropriate credentials automatically
python scripts/upload.py image.png
```

---

## Common Patterns

### Pattern 1: Upload → Share → Archive

```bash
# 1. Upload
python scripts/upload.py photo.png --output result.json

# 2. Get link and share
LINK=$(cat result.json | jq -r '.uploads[0].imgur_data.link')
echo "Shared: $LINK" >> shared_links.txt

# 3. Archive JSON
mv result.json archive/photo_$(date +%s).json
```

### Pattern 2: Conditional upload

```bash
# Only upload if file is under 10MB
if [ $(stat -f%z image.png) -lt 10485760 ]; then
  python scripts/upload.py image.png
else
  echo "File too large, skipping"
fi
```

### Pattern 3: Parallel uploads (advanced)

```bash
# Upload multiple images in parallel
for img in *.png; do
  python scripts/upload.py "$img" --output "${img%.png}.json" &
done
wait

# Combine results
jq -s '{uploads: [.[] | .uploads[]] | add}' *.json > all_results.json
```

---

## Quick Reference

```bash
# Basic upload
python scripts/upload.py image.png

# Multiple files
python scripts/upload.py img1.png img2.jpg img3.gif

# With output
python scripts/upload.py image.png --output result.json --pretty

# Using wildcards
python scripts/upload.py photos/*.png

# Custom Client ID
python scripts/upload.py image.png --client-id "your_id"

# Authenticated upload
python scripts/upload.py image.png --access-token "your_token"

# Get help
python scripts/upload.py --help
```
