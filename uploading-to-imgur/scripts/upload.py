#!/usr/bin/env python3
"""
Imgur 图片上传工具

支持两种上传方式：
1. 匿名上传：使用 Client ID（图片不关联账号）
2. 账号上传：使用 Access Token（图片关联到你的账号）

获取认证信息：https://api.imgur.com/oauth2/addclient
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

import requests


# 默认 Client ID（用户需要替换为自己的）
DEFAULT_CLIENT_ID = "YOUR_CLIENT_ID_HERE"

# Imgur API 端点
IMGUR_UPLOAD_URL = "https://api.imgur.com/3/image"


def upload_image_to_imgur(
    image_path: str,
    client_id: str = None,
    access_token: str = None,
    title: str = None,
    description: str = None
) -> Dict[str, Any]:
    """
    上传单张图片到 Imgur

    Args:
        image_path: 图片文件路径
        client_id: Imgur Client ID（匿名上传）
        access_token: Imgur Access Token（账号上传）
        title: 图片标题（可选）
        description: 图片描述（可选）

    Returns:
        包含上传结果的字典
    """
    result = {
        "original_path": image_path,
        "filename": os.path.basename(image_path),
        "success": False,
        "error": None,
        "upload_type": "authenticated" if access_token else "anonymous",
        "imgur_data": None
    }

    # 检查文件是否存在
    if not os.path.exists(image_path):
        result["error"] = "File not found"
        return result

    # 检查是否是图片文件
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    file_ext = Path(image_path).suffix.lower()
    if file_ext not in valid_extensions:
        result["error"] = f"Invalid image format: {file_ext}"
        return result

    try:
        # 读取图片并转换为 base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # 准备请求头 - 根据认证类型选择
        if access_token:
            # 使用 Access Token（账号上传）
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        elif client_id:
            # 使用 Client ID（匿名上传）
            headers = {
                "Authorization": f"Client-ID {client_id}"
            }
        else:
            result["error"] = "No authentication provided (need client_id or access_token)"
            return result

        # 准备请求数据
        payload = {
            "image": image_data,
            "type": "base64"
        }

        if title:
            payload["title"] = title
        if description:
            payload["description"] = description

        # 发送请求
        print(f"Uploading: {image_path}...", end=" ", flush=True)
        response = requests.post(IMGUR_UPLOAD_URL, headers=headers, data=payload, timeout=30)

        # 处理响应
        if response.status_code == 200:
            response_data = response.json()

            if response_data.get("success"):
                data = response_data.get("data", {})

                # 提取关键信息
                result["success"] = True
                result["imgur_data"] = {
                    "id": data.get("id"),
                    "link": data.get("link"),
                    "deletehash": data.get("deletehash"),
                    "datetime": data.get("datetime"),
                    "type": data.get("type"),
                    "width": data.get("width"),
                    "height": data.get("height"),
                    "size": data.get("size"),
                    "bandwidth": data.get("bandwidth"),
                    "views": data.get("views"),
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "delete_link": f"https://imgur.com/delete/{data.get('deletehash')}" if data.get('deletehash') else None
                }
                print("✓ Success")
            else:
                result["error"] = "Imgur API returned success=false"
                print("✗ Failed")
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text}"
            print(f"✗ Failed (HTTP {response.status_code})")

    except requests.exceptions.Timeout:
        result["error"] = "Request timeout"
        print("✗ Timeout")
    except requests.exceptions.RequestException as e:
        result["error"] = f"Network error: {str(e)}"
        print(f"✗ Network error")
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        print(f"✗ Error: {e}")

    return result


def upload_multiple_images(
    image_paths: List[str],
    client_id: str = None,
    access_token: str = None
) -> Dict[str, Any]:
    """
    上传多张图片到 Imgur

    Args:
        image_paths: 图片文件路径列表
        client_id: Imgur Client ID（匿名上传）
        access_token: Imgur Access Token（账号上传）

    Returns:
        包含所有上传结果的字典
    """
    results = {
        "total": len(image_paths),
        "successful": 0,
        "failed": 0,
        "uploads": []
    }

    for image_path in image_paths:
        result = upload_image_to_imgur(
            image_path,
            client_id=client_id,
            access_token=access_token
        )
        results["uploads"].append(result)

        if result["success"]:
            results["successful"] += 1
        else:
            results["failed"] += 1

    return results


def get_authentication():
    """
    获取认证信息（从环境变量或默认值）

    返回 (client_id, access_token) 元组，至少一个不为 None
    """
    # 尝试获取 Access Token（优先级最高）
    access_token = os.environ.get("IMGUR_ACCESS_TOKEN")

    # 尝试获取 Client ID
    client_id = os.environ.get("IMGUR_CLIENT_ID")
    if not client_id and DEFAULT_CLIENT_ID != "YOUR_CLIENT_ID_HERE":
        client_id = DEFAULT_CLIENT_ID

    # 如果两者都没有，显示错误
    if not access_token and not client_id:
        print("Error: No Imgur authentication found!", file=sys.stderr)
        print("", file=sys.stderr)
        print("Please provide authentication by either:", file=sys.stderr)
        print("", file=sys.stderr)
        print("Option 1 - Anonymous upload (Client ID):", file=sys.stderr)
        print("  export IMGUR_CLIENT_ID='your_client_id'", file=sys.stderr)
        print("  or use --client-id argument", file=sys.stderr)
        print("", file=sys.stderr)
        print("Option 2 - Upload to your account (Access Token):", file=sys.stderr)
        print("  export IMGUR_ACCESS_TOKEN='your_access_token'", file=sys.stderr)
        print("  or use --access-token argument", file=sys.stderr)
        print("", file=sys.stderr)
        print("Get credentials at: https://api.imgur.com/oauth2/addclient", file=sys.stderr)
        sys.exit(1)

    return client_id, access_token


def get_client_id() -> str:
    """获取 Client ID（从环境变量或默认值）- 已弃用，保留兼容性"""
    client_id, _ = get_authentication()
    return client_id


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Upload images to Imgur (anonymous or to your account)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Anonymous upload with Client ID
  %(prog)s image.png --client-id YOUR_CLIENT_ID

  # Upload to your account with Access Token
  %(prog)s image.png --access-token YOUR_ACCESS_TOKEN

  # Upload multiple images
  %(prog)s image1.png image2.jpg image3.gif

  # Save results to JSON file
  %(prog)s image.png --output result.json --pretty

Authentication Methods:
  1. Anonymous upload (Client ID):
     - Images are NOT associated with your account
     - Use --client-id or IMGUR_CLIENT_ID env variable
     - Get it at: https://api.imgur.com/oauth2/addclient

  2. Account upload (Access Token):
     - Images are saved to your Imgur account
     - Use --access-token or IMGUR_ACCESS_TOKEN env variable
     - Get it from OAuth flow (see Imgur API docs)

Environment variables:
  IMGUR_CLIENT_ID       Client ID for anonymous upload
  IMGUR_ACCESS_TOKEN    Access Token for account upload
        """
    )

    parser.add_argument(
        "images",
        nargs="+",
        help="One or more image file paths to upload"
    )

    parser.add_argument(
        "--client-id",
        help="Imgur Client ID for anonymous upload"
    )

    parser.add_argument(
        "--access-token",
        help="Imgur Access Token for account upload"
    )

    parser.add_argument(
        "--output",
        "-o",
        help="Save result to JSON file (default: print to stdout)"
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print JSON output"
    )

    args = parser.parse_args()

    # 获取认证信息
    # 优先使用命令行参数，否则从环境变量获取
    if args.client_id or args.access_token:
        client_id = args.client_id
        access_token = args.access_token
    else:
        client_id, access_token = get_authentication()

    # 显示上传模式
    upload_mode = "account" if access_token else "anonymous"
    print(f"Upload mode: {upload_mode}")
    print(f"Uploading {len(args.images)} image(s) to Imgur...")
    print("")

    # 上传图片
    results = upload_multiple_images(
        args.images,
        client_id=client_id,
        access_token=access_token
    )

    print("")
    print("=" * 60)
    print(f"Upload Summary: {results['successful']} succeeded, {results['failed']} failed")
    print("=" * 60)

    # 格式化输出
    if args.pretty:
        json_output = json.dumps(results, indent=2, ensure_ascii=False)
    else:
        json_output = json.dumps(results, ensure_ascii=False)

    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"\nResults saved to: {args.output}")
    else:
        print("\nJSON Output:")
        print(json_output)

    # 显示成功上传的链接
    successful_uploads = [u for u in results["uploads"] if u["success"]]
    if successful_uploads:
        print("\n" + "=" * 60)
        print("Uploaded Image Links:")
        print("=" * 60)
        for upload in successful_uploads:
            print(f"\n{upload['filename']}:")
            print(f"  Link:   {upload['imgur_data']['link']}")
            if upload['imgur_data']['delete_link']:
                print(f"  Delete: {upload['imgur_data']['delete_link']}")

    # 返回适当的退出码
    sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
