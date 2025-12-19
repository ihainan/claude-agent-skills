# Imgur Authentication Guide

Complete guide to obtaining Imgur API credentials for uploading images.

## Two Authentication Methods

| Method | Client ID | Access Token |
|--------|-----------|--------------|
| **Difficulty** | ⭐ Easy | ⭐⭐⭐ Complex |
| **Expires** | Never | 28 days |
| **Images in account** | No | Yes |
| **Recommended for** | Most users | Advanced users |

## Method 1: Client ID (Recommended)

**Best for:** Anonymous uploads, simple sharing, most use cases

### Steps

#### 1. Login to Imgur

Go to https://imgur.com and sign in (or create an account)

#### 2. Register application

Visit: https://api.imgur.com/oauth2/addclient

**Important:** You must be logged in, or the page will redirect to homepage.

#### 3. Fill the form

```
Application name: My Upload Tool (or any name)
Authorization type: "OAuth 2 authorization without a callback URL" ← Select this!
Authorization callback URL: https://localhost (or leave empty)
Email: your@email.com
Description: Image upload tool (or any description)
```

#### 4. Submit

Complete the CAPTCHA and click submit.

#### 5. Get your Client ID

After submission, you'll see:
- **Client ID**: `abc123def456` ← This is what you need!
- **Client Secret**: (not needed for anonymous uploads)

**Save your Client ID somewhere safe.**

#### 6. Use it

```bash
# Set environment variable
export IMGUR_CLIENT_ID="abc123def456"

# Upload images
python scripts/upload.py image.png
```

#### 7. Find it later

If you forget your Client ID, visit: https://imgur.com/account/settings/apps

---

## Method 2: Access Token (Advanced)

**Best for:** Uploading to your account, managing images through Imgur

### Prerequisites

- Client ID (from Method 1 above)
- Client Secret (from registration)

### Quick method: Use helper script

```bash
python scripts/get_token.py
```

This interactive script will:
1. Open authorization URL in browser
2. Guide you through OAuth flow
3. Extract Access Token automatically
4. Optionally save credentials

### Manual method

#### 1. Build authorization URL

```
https://api.imgur.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&response_type=token&state=mystate
```

Replace `YOUR_CLIENT_ID` with your actual Client ID.

#### 2. Open URL in browser

Paste the URL in your browser and press Enter.

#### 3. Authorize

Click "Allow" to authorize the application.

#### 4. Get token from redirect URL

After authorization, browser will redirect to a URL like:

```
https://localhost/#access_token=YOUR_ACCESS_TOKEN&expires_in=2419200&token_type=bearer&refresh_token=YOUR_REFRESH_TOKEN&account_username=USERNAME
```

The page may show "Cannot connect" - **this is normal**. The important part is the URL.

#### 5. Extract Access Token

From the URL above, copy the value after `access_token=` and before `&`.

Example:
```
URL: https://localhost/#access_token=abc123xyz789&expires_in=...
Token: abc123xyz789
```

#### 6. Use it

```bash
# Set environment variable
export IMGUR_ACCESS_TOKEN="abc123xyz789"

# Upload to your account
python scripts/upload.py image.png
```

The script will automatically use Access Token if available, otherwise fall back to Client ID.

---

## Troubleshooting

### Problem: Page redirects when visiting registration URL

**Solution:** You must be logged in to Imgur first.

1. Go to https://imgur.com
2. Click "Sign in" and login
3. Then visit https://api.imgur.com/oauth2/addclient

### Problem: "Invalid client_id" error

**Solution:**
- Check for typos in your Client ID
- Remove any extra spaces before/after
- Verify the Client ID at https://imgur.com/account/settings/apps

### Problem: Access Token expired

**Solution:**
- Access Tokens expire after 28 days
- Use Refresh Token to get a new one (advanced)
- Or simply go through OAuth flow again

### Problem: "Rate limit exceeded"

**Solution:**
- You've hit the daily limit (1,250 uploads/day)
- Wait until tomorrow for the limit to reset
- Or create another application with a different Client ID

### Problem: Can't open authorization URL

**Solution:**
- Copy the URL manually and paste in browser
- Make sure you're using the correct Client ID
- Try in incognito/private browsing mode

---

## Security Best Practices

### 1. Never commit credentials

Add to `.gitignore`:
```
# Imgur credentials
imgur_credentials.txt
scripts/config.json
.env
```

### 2. Use environment variables

Better than hardcoding in scripts:

```bash
# Add to ~/.bashrc or ~/.zshrc
export IMGUR_CLIENT_ID="your_client_id"
export IMGUR_ACCESS_TOKEN="your_access_token"
```

### 3. Limit application scope

When registering, only request permissions you need.

### 4. Regenerate if compromised

If your credentials are leaked:
1. Go to https://imgur.com/account/settings/apps
2. Delete the compromised application
3. Create a new one with new credentials

### 5. Don't share delete links publicly

Delete links allow anyone to remove your images. Keep them private.

---

## Rate Limits

Both methods have the same limits:

| Limit | Amount |
|-------|--------|
| Uploads per day | ~1,250 |
| API requests per day | ~12,500 |
| Concurrent requests | Reasonable |

**Note:** If you hit the limit 5 times in a month, the app will be blocked for the rest of the month.

---

## Comparison Table

| Feature | Client ID | Access Token |
|---------|-----------|--------------|
| Setup time | 2 minutes | 5-10 minutes |
| Technical difficulty | Easy | Medium |
| Expires | Never | 28 days |
| Renewal | Not needed | Manual or with refresh token |
| Images in account | No | Yes |
| Delete images | Via delete link only | Via Imgur web interface |
| Edit metadata | No | Yes |
| View in gallery | No (unless manually added) | Yes |
| Organize in albums | No | Yes |
| Usage analytics | No | Yes (in Imgur account) |

---

## Quick Start Commands

### Using Client ID

```bash
# One-time setup
export IMGUR_CLIENT_ID="your_client_id"

# Upload
python scripts/upload.py image.png
```

### Using Access Token

```bash
# Get token (one-time)
python scripts/get_token.py

# Setup
export IMGUR_ACCESS_TOKEN="your_access_token"

# Upload
python scripts/upload.py image.png
```

### Using both

```bash
# Priority: Access Token > Client ID
export IMGUR_CLIENT_ID="client_id"
export IMGUR_ACCESS_TOKEN="access_token"

# This will use Access Token
python scripts/upload.py image.png
```

---

## Next Steps

Once you have your credentials:

1. **Test the upload**: `python scripts/upload.py test_image.png`
2. **Save the credentials**: Add to your shell config file
3. **Read examples**: See [EXAMPLES.md](EXAMPLES.md) for common use cases
4. **Check the main guide**: Return to [SKILL.md](SKILL.md) for full documentation
