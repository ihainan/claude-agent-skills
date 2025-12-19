# Authentication Guide

This guide explains how to authenticate with GitHub API to access more data and higher rate limits.

## Why Authenticate?

### Without Token (Public Access)
- ✅ Access all public user data
- ✅ 60 requests per hour
- ❌ No contribution calendar
- ❌ Limited rate for batch operations

### With Personal Access Token
- ✅ Access all public user data
- ✅ 5,000 requests per hour (83x more!)
- ✅ Contribution calendar and activity data
- ✅ Better for batch operations

## Getting a Personal Access Token

### Step 1: Go to GitHub Settings

1. Log in to GitHub
2. Click your profile picture → **Settings**
3. Scroll down to **Developer settings** (left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**

### Step 2: Generate New Token

1. Click **Generate new token (classic)**
2. Give your token a descriptive name (e.g., "GitHub Data Fetcher")
3. Select expiration (recommend: 90 days or custom)
4. Select scopes:
   - ✅ `read:user` - Read user profile data
   - ✅ `read:org` - Read organization data (optional)
   - ✅ `repo` - Only if you need private repo access (usually not needed)

### Step 3: Copy Token

1. Click **Generate token**
2. **IMPORTANT**: Copy the token immediately - you won't see it again!
3. Store it securely (password manager recommended)

## Using Your Token

### Method 1: Command Line Argument (Quick)

```bash
python scripts/fetch.py \
  --username "yourusername" \
  --token "ghp_YOUR_TOKEN_HERE"
```

### Method 2: Environment Variable (Recommended)

**On macOS/Linux:**
```bash
export GITHUB_TOKEN="ghp_YOUR_TOKEN_HERE"
python scripts/fetch.py --username "yourusername"
```

**On Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_YOUR_TOKEN_HERE"
python scripts/fetch.py --username "yourusername"
```

**On Windows (CMD):**
```cmd
set GITHUB_TOKEN=ghp_YOUR_TOKEN_HERE
python scripts/fetch.py --username "yourusername"
```

### Method 3: Use GitHub CLI Token (Easiest)

If you have GitHub CLI (`gh`) installed and authenticated:

```bash
# Authenticate once with gh
gh auth login

# The script will automatically use gh token
python scripts/fetch.py --username "yourusername"
```

## Token Security Best Practices

### ✅ DO:
- Store tokens in environment variables or password managers
- Use tokens with minimal required scopes
- Set expiration dates
- Rotate tokens regularly
- Revoke unused tokens

### ❌ DON'T:
- Commit tokens to git repositories
- Share tokens publicly
- Use tokens in screenshots or logs
- Give tokens more permissions than needed

## Revoking a Token

If your token is compromised:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Find the token in the list
3. Click **Delete** or **Revoke**
4. Generate a new token

## Rate Limits

### Check Your Current Rate Limit

```bash
# Without token
curl https://api.github.com/rate_limit

# With token
curl -H "Authorization: Bearer ghp_YOUR_TOKEN" \
  https://api.github.com/rate_limit
```

### Rate Limit Details

**Unauthenticated:**
- 60 requests per hour per IP
- Resets every hour

**Authenticated:**
- 5,000 requests per hour per token
- Resets every hour
- Includes GraphQL API quota

## Troubleshooting

### "Bad credentials" error
- Check token is copied correctly
- Ensure token hasn't expired
- Verify token has required scopes

### "Rate limit exceeded"
- Wait for rate limit to reset (check reset time)
- Use a Personal Access Token for higher limits
- Reduce number of requests

### Token not working
- Check token hasn't been revoked
- Ensure environment variable is set correctly
- Try generating a new token

## GitHub CLI Integration

The script automatically detects and uses GitHub CLI authentication:

```bash
# Check if gh is authenticated
gh auth status

# If not authenticated
gh auth login

# Now the script can use gh token automatically
python scripts/fetch.py --username "anyuser"
```

## Fine-Grained Personal Access Tokens (Beta)

GitHub now offers fine-grained tokens with more precise permissions:

1. Go to Settings → Developer settings → Personal access tokens → **Fine-grained tokens**
2. Click **Generate new token**
3. Configure:
   - Repository access: "Public Repositories (read-only)"
   - Permissions:
     - Metadata: Read-only
     - Contents: Read-only (optional)

Fine-grained tokens provide better security but require more configuration.

## Additional Resources

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Authentication](https://docs.github.com/en/authentication)
- [Managing Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
