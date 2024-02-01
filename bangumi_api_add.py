import requests
from concurrent.futures import ThreadPoolExecutor
import re

def add_bangumi_collection(entry, access_token):
    subject_id = entry.get('subject_id')
    type = entry.get('type')
    rate = entry.get('rate', 0)
    private = entry.get('private', True)
    comment = entry.get('comment', '')
    tags = entry.get('tags', [])

    # 处理评论
    if comment is not None and isinstance(comment, str):
        comment = re.sub(r'[\x00-\x1F\x7F-\x9F\u200B-\u200F\u2028-\u202F\u2060-\u206F]', '', comment)

    # 处理标签
    cleaned_tags = [tag.strip() for tag in tags] if tags else [""]

    # 构建请求的 URL
    url = f'https://api.bgm.tv/v0/users/-/collections/{subject_id}'

    # 构建请求的 JSON 数据
    # 处理评论部分，去除不可见字符
    if comment is not None and isinstance(comment, str):
        comment = re.sub(r'[\x00-\x1F\x7F-\x9F\u200B-\u200F\u2028-\u202F\u2060-\u206F]', '', comment)
    data = {
        "type": type,
        "rate": rate,
        "comment": comment,
        "private": private,
        "tags": cleaned_tags
    }

    # 构建请求头部信息
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Adachi/BangumiMigrate(https://github.com/Adachi-Git/BangumiMigrate)'
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, json=data)

        # 检查响应状态码
        if response.status_code == 202:
            print(f"Collection added successfully for subject_id {subject_id}.")
        else:
            print(f"Failed to add collection for subject_id {subject_id}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while processing subject_id {subject_id}: {str(e)}")

def bangumi_api_add_collection(bangumi_collections, access_token):
    try:
        # 使用线程池进行并发请求
        with ThreadPoolExecutor() as executor:
            # 提交每个 entry 的处理任务
            futures = [executor.submit(add_bangumi_collection, entry, access_token) for entry in bangumi_collections]

            # 等待所有任务完成
            for future in futures:
                future.result()

        print("All collections added successfully.")

    except Exception as e:
        print("An error occurred:", str(e))