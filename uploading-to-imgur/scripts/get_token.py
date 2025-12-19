#!/usr/bin/env python3
"""
Imgur OAuth 认证辅助工具

帮助用户快速获取 Imgur Access Token
"""

import re
import sys
import webbrowser


def main():
    print("=" * 70)
    print("Imgur Access Token 获取工具")
    print("=" * 70)
    print()

    # 获取 Client ID
    print("请输入你的 Imgur Client ID")
    print("（如果还没有，请访问 https://api.imgur.com/oauth2/addclient 注册）")
    print()

    client_id = input("Client ID: ").strip()

    if not client_id:
        print("错误：Client ID 不能为空")
        sys.exit(1)

    # 构建授权 URL
    auth_url = f"https://api.imgur.com/oauth2/authorize?client_id={client_id}&response_type=token&state=mystate"

    print()
    print("=" * 70)
    print("步骤 1: 浏览器授权")
    print("=" * 70)
    print()
    print("我将在浏览器中打开授权页面...")
    print("如果浏览器没有自动打开，请手动访问以下 URL：")
    print()
    print(auth_url)
    print()

    try:
        webbrowser.open(auth_url)
        print("✓ 已在浏览器中打开")
    except:
        print("✗ 无法自动打开浏览器，请手动复制上面的 URL")

    print()
    print("=" * 70)
    print("步骤 2: 授权应用")
    print("=" * 70)
    print()
    print("1. 在浏览器中点击 'Allow' 按钮授权应用")
    print("2. 授权后浏览器会跳转到一个新的 URL")
    print("   （可能显示 '无法访问此网站' 或类似错误，这是正常的）")
    print("3. 复制浏览器地址栏中的完整 URL")
    print()
    print("=" * 70)
    print("步骤 3: 粘贴重定向 URL")
    print("=" * 70)
    print()
    print("请粘贴浏览器地址栏中的完整 URL：")
    print()

    redirect_url = input("URL: ").strip()

    if not redirect_url:
        print("错误：URL 不能为空")
        sys.exit(1)

    # 解析 URL 提取 token
    print()
    print("正在解析 URL...")

    # 提取 access_token
    access_token_match = re.search(r'access_token=([^&]+)', redirect_url)
    refresh_token_match = re.search(r'refresh_token=([^&]+)', redirect_url)
    expires_match = re.search(r'expires_in=([^&]+)', redirect_url)
    username_match = re.search(r'account_username=([^&]+)', redirect_url)

    if not access_token_match:
        print()
        print("=" * 70)
        print("错误：无法从 URL 中提取 access_token")
        print("=" * 70)
        print()
        print("请确保：")
        print("1. 复制了授权后的完整 URL（包括 # 后面的部分）")
        print("2. URL 中包含 'access_token=' 字段")
        print()
        print("示例 URL 格式：")
        print("https://localhost/#access_token=xxx&expires_in=xxx&...")
        sys.exit(1)

    access_token = access_token_match.group(1)
    refresh_token = refresh_token_match.group(1) if refresh_token_match else None
    expires_in = expires_match.group(1) if expires_match else None
    username = username_match.group(1) if username_match else None

    # 显示结果
    print()
    print("=" * 70)
    print("✓ 成功获取 Access Token！")
    print("=" * 70)
    print()

    if username:
        print(f"账号: {username}")
        print()

    print(f"Access Token:")
    print(f"  {access_token}")
    print()

    if refresh_token:
        print(f"Refresh Token:")
        print(f"  {refresh_token}")
        print()

    if expires_in:
        days = int(expires_in) // 86400
        print(f"有效期: {expires_in} 秒（约 {days} 天）")
        print()

    print("=" * 70)
    print("如何使用")
    print("=" * 70)
    print()
    print("方式 1 - 设置环境变量（推荐）：")
    print()
    print(f'export IMGUR_ACCESS_TOKEN="{access_token}"')
    print()
    print("方式 2 - 命令行参数：")
    print()
    print(f'python3 imgur_upload.py image.png --access-token "{access_token}"')
    print()

    print("=" * 70)
    print("保存凭证")
    print("=" * 70)
    print()

    # 询问是否保存到文件
    save = input("是否保存凭证到 imgur_credentials.txt？(y/n): ").strip().lower()

    if save == 'y':
        try:
            with open("imgur_credentials.txt", "w") as f:
                f.write("# Imgur API Credentials\n")
                f.write("# 获取时间: " + __import__('datetime').datetime.now().isoformat() + "\n\n")
                f.write(f"CLIENT_ID={client_id}\n")
                f.write(f"ACCESS_TOKEN={access_token}\n")
                if refresh_token:
                    f.write(f"REFRESH_TOKEN={refresh_token}\n")
                if expires_in:
                    f.write(f"EXPIRES_IN={expires_in}\n")
                if username:
                    f.write(f"USERNAME={username}\n")
                f.write("\n# 使用方法:\n")
                f.write("# export IMGUR_ACCESS_TOKEN=\"" + access_token + "\"\n")

            print()
            print("✓ 凭证已保存到 imgur_credentials.txt")
            print("  注意：请妥善保管此文件，不要上传到公开仓库！")
        except Exception as e:
            print(f"✗ 保存失败: {e}")

    print()
    print("=" * 70)
    print("完成！现在你可以使用这个 Access Token 上传图片了")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)
