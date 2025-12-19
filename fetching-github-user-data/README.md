# Fetching GitHub User Data

A comprehensive skill for fetching and analyzing GitHub user data through the GitHub API.

## What This Skill Does

Fetches complete GitHub user data including:
- User profile and basic information
- All public repositories with detailed statistics
- Gists and code snippets
- Social connections (followers, following)
- Organizations and subscriptions
- Contribution calendar and activity
- Pull requests and issues
- Programming language statistics
- Repository analytics

## Quick Start

```bash
# Basic usage (public data only)
python scripts/fetch.py --username "torvalds"

# With authentication (recommended, get contribution calendar)
python scripts/fetch.py --username "torvalds" --token "ghp_YOUR_TOKEN"

# Custom output directory
python scripts/fetch.py --username "torvalds" --output "./my_data"
```

## Installation

No additional dependencies needed! Uses Python standard library and `requests`:

```bash
pip install requests
```

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[AUTHENTICATION.md](AUTHENTICATION.md)** - How to get and use GitHub tokens
- **[EXAMPLES.md](EXAMPLES.md)** - Comprehensive usage examples
- **[DATA_ANALYSIS.md](DATA_ANALYSIS.md)** - Analyzing fetched data for engineer evaluation

## Use Cases

### 🎯 Engineer Evaluation
Assess technical capabilities, project experience, and collaboration skills of developers.

### 📊 Developer Research
Study open source contributions, programming trends, and developer behaviors.

### 💼 Recruitment
Build comprehensive profiles of potential hires based on their GitHub activity.

### 📈 Personal Analytics
Track your own GitHub progress and generate portfolio data.

### 🔍 Team Analysis
Analyze your development team's collective skills and contributions.

## Output Example

After running the script, you get organized data:

```
github_user_data/
└── torvalds/
    ├── profile.json                    # Name, bio, location, etc.
    ├── repositories/
    │   ├── list.json                   # 83 repositories
    │   └── details/*.json              # Each repo details
    ├── contributions/calendar.json     # 1,708 contributions
    ├── pull_requests/created.json      # 10 PRs
    ├── issues/created.json             # 17 issues
    ├── statistics/
    │   ├── languages.json              # Java: 35%, Python: 28%...
    │   └── repositories.json           # 192 stars, 71 forks
    └── metadata.json                   # Fetch info
```

## Key Features

✅ **Complete Data Coverage** - Fetches all available public data
✅ **Smart Organization** - Clean directory structure for easy analysis
✅ **Rate Limit Handling** - Automatic pagination and error recovery
✅ **Token Support** - Works with or without authentication
✅ **Statistics Computation** - Automatic language and repo statistics
✅ **Progress Feedback** - Clear output showing what's being fetched
✅ **Error Resilience** - Continues fetching even if some requests fail

## Requirements

- Python 3.7+
- `requests` library
- GitHub Personal Access Token (optional but recommended)

## Authentication (Optional)

Get a GitHub Personal Access Token for:
- ✅ 5,000 requests/hour (vs 60 without)
- ✅ Contribution calendar data
- ✅ Better rate limits for batch operations

See [AUTHENTICATION.md](AUTHENTICATION.md) for step-by-step guide.

## Performance

- **Typical fetch time**: 30-120 seconds
- **API requests**: 15-50 (varies by user)
- **Storage per user**: 1-50 MB

## Example Output - Statistics

```json
{
  "languages": {
    "Java": {"percentage": 35.2, "repos": 12},
    "Python": {"percentage": 28.5, "repos": 11},
    "JavaScript": {"percentage": 18.3, "repos": 5}
  },
  "total_stars": 192,
  "total_forks": 71,
  "total_repos": 83
}
```

## Common Commands

```bash
# Fetch public data
python scripts/fetch.py --username "username"

# Fetch with token from environment variable
export GITHUB_TOKEN="ghp_YOUR_TOKEN"
python scripts/fetch.py --username "username"

# Fetch multiple users
for user in alice bob charlie; do
  python scripts/fetch.py --username "$user"
done

# Check what data was fetched
cat github_user_data/username/metadata.json | jq .
```

## Limitations

- Public events: Last 300 events (30 days max)
- Contribution calendar: Requires authentication
- Repository stats: Limited for repos with 10,000+ commits
- Search results: Max 100 items per query

## Troubleshooting

**Rate limit exceeded?**
→ Use a Personal Access Token (see AUTHENTICATION.md)

**No contribution calendar?**
→ Must use authentication token

**User not found?**
→ Check username spelling

See [EXAMPLES.md](EXAMPLES.md) for more troubleshooting tips.

## Contributing

This skill is part of the Claude Agent Skills collection.

## License

MIT

## Support

For issues or questions, check the documentation files or open an issue.
