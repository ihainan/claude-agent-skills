# GitHub 用户数据获取与工程师能力评估分析

## 概述

本文档分析了通过 GitHub API 可以合法获取的用户数据，并从工程师能力评估的角度进行了详细说明。

## 可获取的数据清单

### 1. 基础数据

#### 用户基本信息 (`profile.json`)
- 用户名、ID、头像
- 个人简介、博客、公司、位置
- 邮箱、Twitter 账号
- 账号创建和更新时间
- 公开仓库数、公开 Gists 数
- Followers 和 Following 数量

**评估价值**：了解工程师的背景信息、活跃度

---

#### 仓库列表 (`repositories/`)
- 所有公开仓库的详细信息
- 包括：仓库名、描述、语言、Stars、Forks、更新时间等

**评估价值**：
- 项目数量和质量
- 技术栈广度
- 项目受欢迎程度（Stars/Forks）

---

#### Gists (`gists/`)
- 所有公开的代码片段
- 包括：描述、文件列表、创建/更新时间

**评估价值**：
- 代码分享习惯
- 解决问题的思路
- 代码质量

---

### 2. 社交数据

#### Followers / Following (`social/`)
- 关注该用户的人列表
- 该用户关注的人列表

**评估价值**：
- 社区影响力
- 技术圈人脉

---

#### 组织 (`organizations.json`)
- 用户所属的组织列表

**评估价值**：
- 工作经历推断
- 参与的技术社区

---

#### Starred 仓库 (`starred/repositories.json`)
- 用户 Star 的所有仓库（最多 670 个）

**评估价值**：
- 技术兴趣方向
- 学习和关注的技术

---

### 3. 活动数据

#### 公开活动事件 (`events/public_events.json`)
- 最近 30 天的公开活动（最多 300 条）
- 包括：Push、Issue、PR、Star 等事件

**评估价值**：
- 近期活跃度
- 主要活动类型

---

#### 订阅的仓库 (`subscriptions.json`)
- 用户 watching 的仓库

**评估价值**：
- 持续关注的项目
- 技术领域深度

---

### 4. 贡献数据 ⭐（需要 Token）

#### 贡献日历 (`contributions/calendar.json`)
- 过去一年每天的贡献次数
- 总贡献数

**评估价值**：⭐⭐⭐
- **编码频率和持续性**
- **工作习惯**
- **活跃程度**

**注意**：需要 Personal Access Token，使用 GraphQL API

---

### 5. 协作能力数据 ⭐

#### Pull Requests (`pull_requests/created.json`)
- 用户创建的所有 PR
- 包括：标题、状态、创建/更新/关闭时间、仓库、评论数、标签

**评估价值**：⭐⭐⭐
- **代码贡献能力**
- **开源贡献经验**
- **协作能力**
- **PR 合并率**（成功率）

---

#### Issues (`issues/created.json`)
- 用户创建的所有 Issue
- 包括：标题、状态、创建/更新/关闭时间、仓库、评论数、标签

**评估价值**：⭐⭐⭐
- **问题发现能力**
- **技术沟通能力**
- **参与开源社区的积极性**

---

### 6. 技术深度数据 ⭐

#### 编程语言统计 (`statistics/languages.json`)
- 各编程语言的仓库数量
- 各语言的代码量（KB）
- 百分比分布

**评估价值**：⭐⭐⭐
- **技术栈广度**
- **主要技术方向**
- **多语言能力**

---

#### 仓库统计 (`statistics/repositories.json`)
- 总 Stars 数
- 总 Forks 数
- 按语言分类的统计

**评估价值**：⭐⭐⭐
- **项目影响力**
- **代码质量间接指标**
- **技术实力**

---

## 数据是否足够评估工程师能力？

### ✅ 已经足够的方面

1. **技术栈广度** - 通过语言统计和仓库信息
2. **项目经验** - 通过仓库列表和详情
3. **开源贡献** - 通过 PR、Issue、Starred 仓库
4. **社区影响力** - 通过 Followers、Stars、Forks
5. **编码活跃度** - 通过贡献日历（需要 token）
6. **协作能力** - 通过 PR 和 Issue 的数量和质量

### ⚠️ 仍然缺失的重要数据

#### 1. 代码质量指标
- ❌ **Commit 质量**：无法直接获取每个 commit 的详细信息（commit message 质量、代码变更量）
- ❌ **Code Review 参与度**：无法获取用户参与 review 其他人 PR 的数据
- ❌ **测试覆盖率**：无法获取仓库的测试覆盖率
- ❌ **代码规范**：无法获取代码风格和规范遵守情况

**解决方案**：
- 需要深入分析每个仓库的 commits（会消耗大量 API 请求）
- 可以使用 `/repos/{owner}/{repo}/commits` 端点
- 可以使用 `/repos/{owner}/{repo}/pulls/{pull_number}/reviews` 获取 review 数据

#### 2. 技术深度指标
- ❌ **单个项目的贡献深度**：无法获取用户在每个仓库的具体贡献量（commits 数、代码行数）
- ❌ **技术难度评估**：无法自动评估项目的技术难度

**解决方案**：
- 使用 `/repos/{owner}/{repo}/stats/contributors` 获取每个仓库的贡献者统计
- 但此 API 计算开销大，且有 10,000 commits 限制

#### 3. 项目维护能力
- ❌ **Issue 处理速度**：无法获取用户解决 issue 的平均时间
- ❌ **PR Review 质量**：无法获取 review 的详细评论内容和质量
- ❌ **项目持续性**：难以评估长期维护项目的能力

#### 4. 团队协作深度
- ❌ **团队项目占比**：无法区分个人项目和团队项目
- ❌ **在团队中的角色**：无法判断是核心开发者还是偶尔贡献者

### 📊 数据完整性评分

| 评估维度 | 数据完整性 | 说明 |
|---------|----------|------|
| 技术栈广度 | ⭐⭐⭐⭐⭐ | 非常完整，可以准确评估 |
| 项目经验 | ⭐⭐⭐⭐ | 较完整，缺少项目难度评估 |
| 开源贡献 | ⭐⭐⭐⭐ | 较完整，缺少贡献深度 |
| 代码质量 | ⭐⭐ | 不足，需要深入分析 commits |
| 协作能力 | ⭐⭐⭐ | 中等，缺少 code review 数据 |
| 活跃度 | ⭐⭐⭐⭐⭐ | 非常完整（需要 token） |
| 影响力 | ⭐⭐⭐⭐ | 较完整 |
| 技术深度 | ⭐⭐⭐ | 中等，缺少具体贡献量 |

## 改进建议

### 短期改进（可立即实现）

1. **获取贡献日历** - 需要用户提供 Personal Access Token
2. **分析 PR 和 Issue 的质量** - 分析标题、描述、评论数、标签等
3. **计算活跃度指标** - 基于事件、PR、Issue 计算综合活跃度

### 中期改进（需要额外开发）

1. **深入分析主要仓库的 Commits**
   - 获取每个仓库的 commit 历史
   - 分析 commit message 质量
   - 统计代码变更量

2. **获取 Code Review 数据**
   - 分析用户参与 review 的 PR
   - 统计 review 评论的数量和质量

3. **计算仓库贡献占比**
   - 使用 `/repos/{owner}/{repo}/stats/contributors` API
   - 计算用户在每个仓库的贡献百分比

### 长期改进（需要大量 API 调用）

1. **完整的代码质量分析**
   - 分析所有 commits
   - 获取所有 PR 的详细信息
   - 分析代码变更的质量

2. **项目难度评估**
   - 基于项目的技术栈、代码量、复杂度评估
   - 需要使用机器学习或规则引擎

## 结论

当前脚本已经可以获取到**相当丰富的数据**，足以从以下角度评估工程师能力：

✅ **技术栈广度和深度**
✅ **项目经验和数量**
✅ **开源贡献积极性**
✅ **社区影响力**
✅ **编码活跃度**（需要 token）
✅ **基础协作能力**

但仍然**缺少一些关键的深度数据**：

❌ **代码质量的详细指标**
❌ **Code Review 参与度**
❌ **具体项目贡献深度**
❌ **团队协作角色定位**

### 建议的评估方案

对于**初步筛选**：当前数据已经足够
对于**深度评估**：建议补充以下数据
1. 贡献日历（必须，需要 token）
2. 主要仓库的 commits 分析（可选）
3. Code review 数据（可选）

---

## 目录结构

```
github_user_data/{username}/
├── profile.json                    # 用户基本信息
├── repositories/
│   ├── list.json                   # 仓库列表摘要
│   └── details/{repo_name}.json    # 每个仓库详细信息
├── gists/
│   ├── list.json                   # Gists 列表
│   └── details/{gist_id}.json      # 每个 gist 详细信息
├── starred/repositories.json       # Starred 仓库
├── social/
│   ├── followers.json              # Followers
│   └── following.json              # Following
├── organizations.json              # 组织
├── events/public_events.json       # 公开活动
├── subscriptions.json              # 订阅的仓库
├── contributions/calendar.json     # 贡献日历（需要 token）
├── pull_requests/created.json      # 创建的 PR
├── issues/created.json             # 创建的 Issue
├── statistics/
│   ├── languages.json              # 编程语言统计
│   └── repositories.json           # 仓库统计
└── metadata.json                   # 元数据
```

## 参考资料

- [GitHub REST API - Users](https://docs.github.com/en/rest/users/users)
- [GitHub REST API - Repositories](https://docs.github.com/en/rest/repos/repos)
- [GitHub REST API - Repository Statistics](https://docs.github.com/en/rest/metrics/statistics)
- [GitHub GraphQL API - Contributions](https://docs.github.com/en/graphql/reference/objects#contributioncalendar)
- [How to Query GitHub for User Contributions](https://www.metachris.dev/2025/10/how-to-query-github-for-user-contributions-in-a-specific-timeframe/)
