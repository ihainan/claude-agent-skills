#!/usr/bin/env python3
"""
GitHub 用户数据获取工具

通过 GitHub API 获取指定用户的所有公开数据，并以目录/文件的方式存储到本地文件系统。

使用方法:
    python fetch_github_user_data.py <username> [--token <github_token>] [--output <output_dir>]

示例:
    python fetch_github_user_data.py torvalds --token ghp_xxxx --output ./github_data
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

import requests


class GitHubUserDataFetcher:
    """GitHub 用户数据获取器"""

    def __init__(self, username: str, token: Optional[str] = None, output_dir: str = "./github_user_data"):
        """
        初始化

        Args:
            username: GitHub 用户名
            token: GitHub Personal Access Token（可选）
            output_dir: 输出目录
        """
        self.username = username
        self.token = token
        self.output_dir = Path(output_dir) / username
        self.base_url = "https://api.github.com"
        self.session = requests.Session()

        # 设置请求头
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        })

        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}"
            })

        # 统计信息
        self.stats = {
            "requests_made": 0,
            "data_fetched": {},
            "errors": []
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        发起 API 请求

        Args:
            endpoint: API 端点（不包含 base_url）
            params: 查询参数

        Returns:
            Response 对象
        """
        url = f"{self.base_url}{endpoint}"
        self.stats["requests_made"] += 1

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            error_msg = f"请求失败: {endpoint} - {str(e)}"
            self.stats["errors"].append(error_msg)
            print(f"❌ {error_msg}", file=sys.stderr)
            raise

    def _fetch_paginated_data(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        获取分页数据

        Args:
            endpoint: API 端点
            params: 查询参数

        Returns:
            所有分页数据的列表
        """
        all_data = []
        page = 1
        per_page = 100

        if params is None:
            params = {}

        params["per_page"] = per_page

        while True:
            params["page"] = page
            print(f"  正在获取第 {page} 页...")

            try:
                response = self._make_request(endpoint, params)
                data = response.json()

                if not data:
                    break

                all_data.extend(data)

                # 检查是否还有下一页
                link_header = response.headers.get("Link", "")
                if 'rel="next"' not in link_header:
                    break

                page += 1

            except Exception as e:
                print(f"  获取第 {page} 页时出错: {str(e)}", file=sys.stderr)
                break

        return all_data

    def _save_json(self, data: Any, filepath: Path):
        """保存 JSON 数据到文件"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ 已保存到: {filepath}")

    def fetch_profile(self) -> Dict:
        """获取用户基本信息"""
        print(f"\n📝 获取用户基本信息...")
        response = self._make_request(f"/users/{self.username}")
        profile = response.json()

        self._save_json(profile, self.output_dir / "profile.json")
        self.stats["data_fetched"]["profile"] = True
        return profile

    def fetch_repositories(self):
        """获取用户仓库"""
        print(f"\n📦 获取用户仓库...")
        repos = self._fetch_paginated_data(
            f"/users/{self.username}/repos",
            {"type": "all", "sort": "updated"}
        )

        # 保存仓库列表摘要
        repos_summary = [{
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"],
            "updated_at": repo["updated_at"],
            "html_url": repo["html_url"]
        } for repo in repos]

        self._save_json(repos_summary, self.output_dir / "repositories" / "list.json")

        # 保存每个仓库的详细信息
        details_dir = self.output_dir / "repositories" / "details"
        for repo in repos:
            repo_name = repo["name"]
            self._save_json(repo, details_dir / f"{repo_name}.json")

        self.stats["data_fetched"]["repositories"] = len(repos)
        print(f"  共获取 {len(repos)} 个仓库")

    def fetch_gists(self):
        """获取用户 Gists"""
        print(f"\n📄 获取用户 Gists...")
        gists = self._fetch_paginated_data(f"/users/{self.username}/gists")

        # 保存 gists 列表
        gists_summary = [{
            "id": gist["id"],
            "description": gist["description"],
            "public": gist["public"],
            "files": list(gist["files"].keys()),
            "created_at": gist["created_at"],
            "updated_at": gist["updated_at"],
            "html_url": gist["html_url"]
        } for gist in gists]

        self._save_json(gists_summary, self.output_dir / "gists" / "list.json")

        # 保存每个 gist 的详细信息
        details_dir = self.output_dir / "gists" / "details"
        for gist in gists:
            gist_id = gist["id"]
            self._save_json(gist, details_dir / f"{gist_id}.json")

        self.stats["data_fetched"]["gists"] = len(gists)
        print(f"  共获取 {len(gists)} 个 Gists")

    def fetch_starred(self):
        """获取用户 starred 的仓库"""
        print(f"\n⭐ 获取 Starred 仓库...")
        starred = self._fetch_paginated_data(
            f"/users/{self.username}/starred",
            {"sort": "created"}
        )

        # 保存 starred 仓库列表
        starred_summary = [{
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "html_url": repo["html_url"]
        } for repo in starred]

        self._save_json(starred_summary, self.output_dir / "starred" / "repositories.json")
        self.stats["data_fetched"]["starred"] = len(starred)
        print(f"  共获取 {len(starred)} 个 Starred 仓库")

    def fetch_followers(self):
        """获取用户的 Followers"""
        print(f"\n👥 获取 Followers...")
        followers = self._fetch_paginated_data(f"/users/{self.username}/followers")

        # 保存 followers 列表
        followers_summary = [{
            "login": user["login"],
            "id": user["id"],
            "avatar_url": user["avatar_url"],
            "html_url": user["html_url"],
            "type": user["type"]
        } for user in followers]

        self._save_json(followers_summary, self.output_dir / "social" / "followers.json")
        self.stats["data_fetched"]["followers"] = len(followers)
        print(f"  共获取 {len(followers)} 个 Followers")

    def fetch_following(self):
        """获取用户 Following 的人"""
        print(f"\n👤 获取 Following...")
        following = self._fetch_paginated_data(f"/users/{self.username}/following")

        # 保存 following 列表
        following_summary = [{
            "login": user["login"],
            "id": user["id"],
            "avatar_url": user["avatar_url"],
            "html_url": user["html_url"],
            "type": user["type"]
        } for user in following]

        self._save_json(following_summary, self.output_dir / "social" / "following.json")
        self.stats["data_fetched"]["following"] = len(following)
        print(f"  共获取 {len(following)} 个 Following")

    def fetch_organizations(self):
        """获取用户所属的组织"""
        print(f"\n🏢 获取用户组织...")
        try:
            orgs = self._fetch_paginated_data(f"/users/{self.username}/orgs")

            # 保存组织列表
            orgs_summary = [{
                "login": org["login"],
                "id": org["id"],
                "description": org.get("description"),
                "avatar_url": org["avatar_url"],
                "html_url": f"https://github.com/{org['login']}"
            } for org in orgs]

            self._save_json(orgs_summary, self.output_dir / "organizations.json")
            self.stats["data_fetched"]["organizations"] = len(orgs)
            print(f"  共获取 {len(orgs)} 个组织")
        except Exception as e:
            print(f"  获取组织失败: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["organizations"] = 0

    def fetch_events(self):
        """获取用户的公开活动事件"""
        print(f"\n📅 获取公开活动事件...")
        try:
            events = self._fetch_paginated_data(f"/users/{self.username}/events/public")

            # 保存事件列表（只保存最近的，因为 API 限制最多 300 条）
            events_summary = [{
                "id": event["id"],
                "type": event["type"],
                "repo": event["repo"]["name"],
                "created_at": event["created_at"],
                "public": event["public"]
            } for event in events]

            self._save_json(events_summary, self.output_dir / "events" / "public_events.json")
            self.stats["data_fetched"]["events"] = len(events)
            print(f"  共获取 {len(events)} 个公开事件（最近 30 天内）")
        except Exception as e:
            print(f"  获取事件失败: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["events"] = 0

    def fetch_subscriptions(self):
        """获取用户订阅的仓库"""
        print(f"\n🔔 获取订阅的仓库...")
        try:
            # 注意：这个端点可能需要认证，并且只能获取认证用户自己的订阅
            subscriptions = self._fetch_paginated_data(f"/users/{self.username}/subscriptions")

            subscriptions_summary = [{
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo["description"],
                "html_url": repo["html_url"]
            } for repo in subscriptions]

            self._save_json(subscriptions_summary, self.output_dir / "subscriptions.json")
            self.stats["data_fetched"]["subscriptions"] = len(subscriptions)
            print(f"  共获取 {len(subscriptions)} 个订阅")
        except Exception as e:
            print(f"  获取订阅失败（可能需要认证）: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["subscriptions"] = 0

    def _make_graphql_request(self, query: str) -> Dict:
        """
        发起 GraphQL API 请求

        Args:
            query: GraphQL 查询语句

        Returns:
            响应数据
        """
        url = "https://api.github.com/graphql"
        self.stats["requests_made"] += 1

        try:
            response = self.session.post(url, json={"query": query}, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"GraphQL 请求失败: {str(e)}"
            self.stats["errors"].append(error_msg)
            print(f"❌ {error_msg}", file=sys.stderr)
            raise

    def fetch_contribution_calendar(self):
        """获取用户贡献日历（使用 GraphQL API）"""
        print(f"\n📊 获取贡献日历...")
        try:
            query = """
            {
              user(login: "%s") {
                contributionsCollection {
                  contributionCalendar {
                    totalContributions
                    weeks {
                      contributionDays {
                        contributionCount
                        date
                        weekday
                      }
                    }
                  }
                  restrictedContributionsCount
                }
              }
            }
            """ % self.username

            result = self._make_graphql_request(query)

            if "data" in result and result["data"]["user"]:
                contribution_data = result["data"]["user"]["contributionsCollection"]
                self._save_json(contribution_data, self.output_dir / "contributions" / "calendar.json")

                total = contribution_data["contributionCalendar"]["totalContributions"]
                self.stats["data_fetched"]["contribution_calendar"] = total
                print(f"  共获取 {total} 次贡献记录")
            else:
                print(f"  获取贡献日历失败", file=sys.stderr)
                self.stats["data_fetched"]["contribution_calendar"] = 0
        except Exception as e:
            print(f"  获取贡献日历失败: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["contribution_calendar"] = 0

    def fetch_pull_requests(self):
        """获取用户创建的 Pull Requests"""
        print(f"\n🔀 获取 Pull Requests...")
        try:
            # 使用 Search API 搜索用户创建的 PR
            response = self._make_request(
                "/search/issues",
                {"q": f"author:{self.username} type:pr", "per_page": 100, "sort": "created", "order": "desc"}
            )
            search_result = response.json()
            total_count = search_result.get("total_count", 0)

            # 获取前 100 个 PR 的详细信息
            prs = search_result.get("items", [])
            prs_summary = [{
                "title": pr["title"],
                "state": pr["state"],
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
                "closed_at": pr.get("closed_at"),
                "repository": pr["repository_url"].split("/")[-2:],
                "html_url": pr["html_url"],
                "comments": pr.get("comments", 0),
                "labels": [label["name"] for label in pr.get("labels", [])]
            } for pr in prs]

            self._save_json({
                "total_count": total_count,
                "fetched_count": len(prs),
                "pull_requests": prs_summary
            }, self.output_dir / "pull_requests" / "created.json")

            self.stats["data_fetched"]["pull_requests"] = total_count
            print(f"  共找到 {total_count} 个 PR，已保存前 {len(prs)} 个详情")
        except Exception as e:
            print(f"  获取 Pull Requests 失败: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["pull_requests"] = 0

    def fetch_issues(self):
        """获取用户创建的 Issues"""
        print(f"\n🐛 获取 Issues...")
        try:
            # 使用 Search API 搜索用户创建的 issue
            response = self._make_request(
                "/search/issues",
                {"q": f"author:{self.username} type:issue", "per_page": 100, "sort": "created", "order": "desc"}
            )
            search_result = response.json()
            total_count = search_result.get("total_count", 0)

            # 获取前 100 个 issue 的详细信息
            issues = search_result.get("items", [])
            issues_summary = [{
                "title": issue["title"],
                "state": issue["state"],
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                "closed_at": issue.get("closed_at"),
                "repository": issue["repository_url"].split("/")[-2:],
                "html_url": issue["html_url"],
                "comments": issue.get("comments", 0),
                "labels": [label["name"] for label in issue.get("labels", [])]
            } for issue in issues]

            self._save_json({
                "total_count": total_count,
                "fetched_count": len(issues),
                "issues": issues_summary
            }, self.output_dir / "issues" / "created.json")

            self.stats["data_fetched"]["issues"] = total_count
            print(f"  共找到 {total_count} 个 Issue，已保存前 {len(issues)} 个详情")
        except Exception as e:
            print(f"  获取 Issues 失败: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["issues"] = 0

    def fetch_language_stats(self):
        """获取用户的编程语言统计"""
        print(f"\n💻 统计编程语言分布...")
        try:
            # 读取已保存的仓库数据
            repos_dir = self.output_dir / "repositories" / "details"
            if not repos_dir.exists():
                print("  需要先获取仓库数据", file=sys.stderr)
                return

            language_stats = {}
            total_size = 0

            # 遍历所有仓库，统计语言
            for repo_file in repos_dir.glob("*.json"):
                with open(repo_file, 'r', encoding='utf-8') as f:
                    repo = json.load(f)
                    language = repo.get("language")
                    size = repo.get("size", 0)

                    if language:
                        if language not in language_stats:
                            language_stats[language] = {
                                "repo_count": 0,
                                "total_size_kb": 0
                            }
                        language_stats[language]["repo_count"] += 1
                        language_stats[language]["total_size_kb"] += size
                        total_size += size

            # 计算百分比
            for lang in language_stats:
                language_stats[lang]["percentage"] = round(
                    (language_stats[lang]["total_size_kb"] / total_size * 100) if total_size > 0 else 0,
                    2
                )

            # 排序
            sorted_languages = dict(
                sorted(language_stats.items(), key=lambda x: x[1]["total_size_kb"], reverse=True)
            )

            self._save_json({
                "languages": sorted_languages,
                "total_size_kb": total_size,
                "language_count": len(sorted_languages)
            }, self.output_dir / "statistics" / "languages.json")

            self.stats["data_fetched"]["language_stats"] = len(sorted_languages)
            print(f"  共统计 {len(sorted_languages)} 种编程语言")
        except Exception as e:
            print(f"  统计编程语言失败: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["language_stats"] = 0

    def fetch_repository_stats(self):
        """获取仓库的详细统计信息"""
        print(f"\n📈 获取仓库统计信息...")
        try:
            # 读取已保存的仓库列表
            repos_list_file = self.output_dir / "repositories" / "list.json"
            if not repos_list_file.exists():
                print("  需要先获取仓库数据", file=sys.stderr)
                return

            with open(repos_list_file, 'r', encoding='utf-8') as f:
                repos = json.load(f)

            stats_summary = {
                "total_stars": 0,
                "total_forks": 0,
                "total_watchers": 0,
                "total_repos": len(repos),
                "by_language": {}
            }

            # 统计所有仓库的数据
            for repo in repos:
                stats_summary["total_stars"] += repo.get("stars", 0)
                stats_summary["total_forks"] += repo.get("forks", 0)

                language = repo.get("language")
                if language:
                    if language not in stats_summary["by_language"]:
                        stats_summary["by_language"][language] = {
                            "repos": 0,
                            "stars": 0,
                            "forks": 0
                        }
                    stats_summary["by_language"][language]["repos"] += 1
                    stats_summary["by_language"][language]["stars"] += repo.get("stars", 0)
                    stats_summary["by_language"][language]["forks"] += repo.get("forks", 0)

            self._save_json(stats_summary, self.output_dir / "statistics" / "repositories.json")
            self.stats["data_fetched"]["repository_stats"] = True
            print(f"  总计: {stats_summary['total_stars']} Stars, {stats_summary['total_forks']} Forks")
        except Exception as e:
            print(f"  获取仓库统计失败: {str(e)}", file=sys.stderr)
            self.stats["data_fetched"]["repository_stats"] = False

    def save_metadata(self):
        """保存元数据"""
        print(f"\n💾 保存元数据...")
        metadata = {
            "username": self.username,
            "fetched_at": datetime.now().isoformat(),
            "output_directory": str(self.output_dir),
            "statistics": self.stats,
            "api_version": "2022-11-28"
        }

        self._save_json(metadata, self.output_dir / "metadata.json")

    def fetch_all(self):
        """获取所有数据"""
        print(f"🚀 开始获取 GitHub 用户 '{self.username}' 的数据...\n")
        print(f"输出目录: {self.output_dir}")

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 依次获取各类数据
        try:
            # 基础数据
            self.fetch_profile()
            self.fetch_repositories()
            self.fetch_gists()
            self.fetch_starred()

            # 社交数据
            self.fetch_followers()
            self.fetch_following()
            self.fetch_organizations()

            # 活动数据
            self.fetch_events()
            self.fetch_subscriptions()

            # 贡献数据（需要 token，使用 GraphQL）
            if self.token:
                self.fetch_contribution_calendar()
            else:
                print("\n⚠️  跳过贡献日历获取（需要 Personal Access Token）")

            # 协作数据
            self.fetch_pull_requests()
            self.fetch_issues()

            # 统计数据（依赖前面获取的数据）
            self.fetch_language_stats()
            self.fetch_repository_stats()

        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断操作")
        except Exception as e:
            print(f"\n\n❌ 发生错误: {str(e)}", file=sys.stderr)
        finally:
            # 保存元数据
            self.save_metadata()

            # 打印统计信息
            self.print_summary()

    def print_summary(self):
        """打印统计摘要"""
        print("\n" + "=" * 60)
        print("📊 数据获取完成！统计信息:")
        print("=" * 60)
        print(f"总共发起的 API 请求数: {self.stats['requests_made']}")
        print(f"\n已获取的数据:")
        for key, value in self.stats['data_fetched'].items():
            if isinstance(value, int):
                print(f"  - {key}: {value} 条")
            else:
                print(f"  - {key}: ✓")

        if self.stats['errors']:
            print(f"\n⚠️  错误数: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # 只显示前 5 个错误
                print(f"  - {error}")

        print(f"\n数据已保存到: {self.output_dir}")
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="获取 GitHub 用户的所有公开数据并保存到本地文件系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 获取用户数据（不使用 token）
  python fetch_github_user_data.py torvalds

  # 使用 Personal Access Token（可以提高 rate limit）
  python fetch_github_user_data.py torvalds --token ghp_xxxxxxxxxxxx

  # 指定输出目录
  python fetch_github_user_data.py torvalds --output ./my_data

  # 从环境变量读取 token
  export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
  python fetch_github_user_data.py torvalds
        """
    )

    parser.add_argument(
        "username",
        help="GitHub 用户名"
    )

    parser.add_argument(
        "-t", "--token",
        help="GitHub Personal Access Token（可选，可以从环境变量 GITHUB_TOKEN 读取）",
        default=os.environ.get("GITHUB_TOKEN")
    )

    parser.add_argument(
        "-o", "--output",
        help="输出目录（默认: ./github_user_data）",
        default="./github_user_data"
    )

    args = parser.parse_args()

    # 创建 fetcher 并执行
    fetcher = GitHubUserDataFetcher(
        username=args.username,
        token=args.token,
        output_dir=args.output
    )

    fetcher.fetch_all()


if __name__ == "__main__":
    main()
