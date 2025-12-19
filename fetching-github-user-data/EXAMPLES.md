# Usage Examples

Comprehensive examples for fetching GitHub user data in various scenarios.

## Basic Examples

### Example 1: Fetch Public Data (No Token)

Simplest usage - fetch public data for any GitHub user:

```bash
python scripts/fetch.py --username "torvalds"
```

**What you get:**
- User profile
- Public repositories
- Gists
- Followers/Following
- Starred repositories
- Organizations
- Recent public events
- Pull requests and issues created

**Note:** No contribution calendar without token.

---

### Example 2: Fetch with Token (Recommended)

Get complete data including contribution calendar:

```bash
python scripts/fetch.py \
  --username "torvalds" \
  --token "ghp_YOUR_TOKEN_HERE"
```

**Additional data with token:**
- ✅ Contribution calendar (activity graph)
- ✅ Higher rate limits (5,000/hour)
- ✅ Faster batch operations

---

### Example 3: Custom Output Directory

Organize data in your preferred location:

```bash
python scripts/fetch.py \
  --username "gvanrossum" \
  --output "./python_creator_data"
```

**Output:**
```
./python_creator_data/
└── gvanrossum/
    ├── profile.json
    ├── repositories/
    ├── contributions/
    └── ...
```

---

## Advanced Examples

### Example 4: Analyze Multiple Users

Fetch data for multiple developers:

```bash
#!/bin/bash
USERS=("torvalds" "gvanrossum" "dhh" "addyosmani")

for user in "${USERS[@]}"; do
  echo "Fetching data for $user..."
  python scripts/fetch.py \
    --username "$user" \
    --output "./github_developers"
  sleep 2  # Be nice to the API
done
```

---

### Example 5: Using Environment Variable for Token

Set token once, use multiple times:

```bash
# Set token in current session
export GITHUB_TOKEN="ghp_YOUR_TOKEN_HERE"

# Fetch multiple users
python scripts/fetch.py --username "torvalds"
python scripts/fetch.py --username "gvanrossum"
python scripts/fetch.py --username "dhh"
```

---

### Example 6: Fetch Your Own Data

Analyze your own GitHub profile:

```bash
# Using gh CLI (easiest)
gh auth login
python scripts/fetch.py --username "YOUR_USERNAME"

# Or with token
export GITHUB_TOKEN="ghp_YOUR_TOKEN"
python scripts/fetch.py --username "YOUR_USERNAME"
```

---

## Use Case Examples

### Use Case 1: Engineer Evaluation

Evaluate a potential hire or collaborator:

```bash
# Fetch candidate data
python scripts/fetch.py \
  --username "candidate_username" \
  --token "$GITHUB_TOKEN" \
  --output "./evaluations"

# Then analyze the data
cat ./evaluations/candidate_username/statistics/languages.json
cat ./evaluations/candidate_username/statistics/repositories.json
cat ./evaluations/candidate_username/pull_requests/created.json
```

**Key metrics to check:**
- Programming languages (technical breadth)
- Total stars/forks (project impact)
- Pull requests (collaboration)
- Contribution calendar (activity level)

---

### Use Case 2: Open Source Contributor Research

Study contributions of active open source developers:

```bash
# Fetch data for well-known contributors
for user in "sindresorhus" "tj" "substack"; do
  python scripts/fetch.py \
    --username "$user" \
    --token "$GITHUB_TOKEN" \
    --output "./opensource_research"
done

# Analyze their starred repos to find trending projects
cat ./opensource_research/*/starred/repositories.json | \
  jq '.[] | .full_name' | \
  sort | uniq -c | sort -rn | head -20
```

---

### Use Case 3: Track Your Progress

Monitor your own GitHub activity over time:

```bash
# Create monthly snapshots
DATE=$(date +%Y-%m)
python scripts/fetch.py \
  --username "YOUR_USERNAME" \
  --token "$GITHUB_TOKEN" \
  --output "./my_github_snapshots/$DATE"

# Compare growth
diff \
  ./my_github_snapshots/2024-11/YOUR_USERNAME/metadata.json \
  ./my_github_snapshots/2024-12/YOUR_USERNAME/metadata.json
```

---

### Use Case 4: Build Developer Portfolio

Generate data for your portfolio website:

```bash
# Fetch your data
python scripts/fetch.py \
  --username "YOUR_USERNAME" \
  --token "$GITHUB_TOKEN" \
  --output "./portfolio_data"

# Extract key stats for portfolio
cat ./portfolio_data/YOUR_USERNAME/statistics/repositories.json | \
  jq '{total_stars, total_forks, total_repos}'

cat ./portfolio_data/YOUR_USERNAME/statistics/languages.json | \
  jq '.languages | to_entries | sort_by(-.value.percentage) | .[0:5]'
```

---

### Use Case 5: Team Analysis

Analyze your entire development team:

```bash
#!/bin/bash
TEAM=("alice" "bob" "charlie" "diana")
OUTPUT_DIR="./team_analysis"

echo "Fetching data for team members..."
for member in "${TEAM[@]}"; do
  echo "Processing $member..."
  python scripts/fetch.py \
    --username "$member" \
    --token "$GITHUB_TOKEN" \
    --output "$OUTPUT_DIR"
done

echo "Generating team summary..."
# Aggregate total contributions
for member in "${TEAM[@]}"; do
  echo -n "$member: "
  cat "$OUTPUT_DIR/$member/statistics/repositories.json" | \
    jq '.total_stars'
done
```

---

## Data Analysis Examples

### Example: Find Top Languages

```bash
# After fetching data
cat ./github_user_data/USERNAME/statistics/languages.json | \
  jq -r '.languages | to_entries |
         sort_by(-.value.percentage) |
         .[] | "\(.key): \(.value.percentage)%"'
```

**Output:**
```
Java: 35.2%
Python: 28.5%
JavaScript: 18.3%
Go: 12.1%
...
```

---

### Example: Count Open vs Closed PRs

```bash
cat ./github_user_data/USERNAME/pull_requests/created.json | \
  jq '.pull_requests | group_by(.state) |
      map({state: .[0].state, count: length})'
```

**Output:**
```json
[
  {"state": "closed", "count": 45},
  {"state": "open", "count": 3}
]
```

---

### Example: Most Starred Projects

```bash
cat ./github_user_data/USERNAME/repositories/list.json | \
  jq 'sort_by(-.stars) | .[0:10] |
      .[] | "\(.name): \(.stars) ⭐"'
```

**Output:**
```
awesome-project: 1234 ⭐
cool-library: 567 ⭐
useful-tool: 234 ⭐
...
```

---

## Automation Examples

### Example: Daily Backup Script

Create a cron job to backup your GitHub data daily:

```bash
#!/bin/bash
# save as: backup_github_data.sh

DATE=$(date +%Y%m%d)
USERNAME="YOUR_USERNAME"
TOKEN="$GITHUB_TOKEN"
BACKUP_DIR="$HOME/github_backups"

python /path/to/scripts/fetch.py \
  --username "$USERNAME" \
  --token "$TOKEN" \
  --output "$BACKUP_DIR/$DATE"

# Keep only last 30 days
find "$BACKUP_DIR" -type d -mtime +30 -exec rm -rf {} +
```

Add to crontab:
```bash
0 2 * * * /path/to/backup_github_data.sh
```

---

### Example: Webhook Integration

Fetch data when a webhook is triggered:

```python
# webhook_handler.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    username = data.get('username')

    if username:
        subprocess.run([
            'python', 'scripts/fetch.py',
            '--username', username,
            '--token', os.environ['GITHUB_TOKEN'],
            '--output', './webhook_data'
        ])
        return {'status': 'success'}, 200

    return {'status': 'error'}, 400
```

---

## Performance Tips

### Tip 1: Use Token for Batch Operations

Always use a token when fetching multiple users:

```bash
export GITHUB_TOKEN="ghp_YOUR_TOKEN"

# This will be much faster
for user in user1 user2 user3; do
  python scripts/fetch.py --username "$user"
done
```

---

### Tip 2: Add Delays Between Requests

Be respectful to GitHub's API:

```bash
for user in $(cat users.txt); do
  python scripts/fetch.py --username "$user"
  sleep 5  # Wait 5 seconds between users
done
```

---

### Tip 3: Parallel Processing (Advanced)

Fetch multiple users in parallel (use with caution):

```bash
#!/bin/bash
USERS=("user1" "user2" "user3" "user4")

for user in "${USERS[@]}"; do
  python scripts/fetch.py --username "$user" &
done

wait  # Wait for all background jobs
```

---

## Troubleshooting Examples

### Debug: Check API Rate Limit

```bash
# See remaining requests
python -c "
import requests
import os

token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'Bearer {token}'} if token else {}
r = requests.get('https://api.github.com/rate_limit', headers=headers)
print(r.json())
"
```

---

### Debug: Test Single Endpoint

```bash
# Test if user exists
curl https://api.github.com/users/USERNAME

# With token
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/users/USERNAME
```

---

## See Also

- [SKILL.md](SKILL.md) - Main documentation
- [AUTHENTICATION.md](AUTHENTICATION.md) - Authentication guide
- [DATA_ANALYSIS.md](DATA_ANALYSIS.md) - Data analysis guide
