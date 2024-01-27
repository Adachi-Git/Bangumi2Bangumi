import json
import time
import logging
import requests
from tqdm import tqdm
from requests.exceptions import RequestException

# 设置日志级别
logging.basicConfig(level=logging.INFO)

# 配置大号ID和大小号TOKEN
API_SERVER = "https://api.bgm.tv"
USERNAME_OR_UID = ""  # 大号ID
ACCESS_TOKEN = ""   # 大号
ACCESS_TOKEN_2 =""  # 小号

# 全局等待时间
WAIT_TIME = 5

# 重试次数
MAX_RETRIES = 3

# 用大号token获取大号收藏
def get_json_with_bearer_token(url):
    """
    发送GET请求获取JSON格式数据，使用Bearer令牌进行身份验证。

    Args:
        url (str): 请求的URL。

    Returns:
        dict: 包含JSON格式数据的字典。
    """    
    time.sleep(WAIT_TIME)
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'accept': 'application/json',
        'User-Agent': 'Adachi/BangumiMigrate(https://github.com/Adachi-Git/BangumiMigrate)'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def load_data_until_finish(endpoint, limit=30, name="", show_progress=False):
    """
    从指定API端点加载数据，直到加载完所有数据或达到最大重试次数。

    Args:
        endpoint (str): API端点的URL。
        limit (int, optional): 每次加载的数据量。默认为30。
        name (str, optional): 用于记录日志的加载数据的名称。默认为空字符串。
        show_progress (bool, optional): 是否显示加载进度条。默认为False。

    Returns:
        list or None: 成功加载的数据列表。如果失败则返回None。
    """
    retries = 0

    while retries < MAX_RETRIES:
        try:
            resp = get_json_with_bearer_token(endpoint)

            if name != "":
                logging.debug(f"loading data from {name}")

            if "total" not in resp:
                logging.debug(f"no total {name}")
                return resp

            total = resp["total"]
            logging.debug(f"{name}: total count={total}")
            items = resp["data"]

            if show_progress:
                pbar = tqdm(total=total, desc=name)
                pbar.update(len(items))

            while len(items) < total:
                offset = len(items)
                logging.debug(f"{name}: loading from offset={offset}")
                new_url = f"{endpoint}?limit={limit}&offset={offset}"
                resp = get_json_with_bearer_token(new_url)
                items += resp["data"]
                if show_progress:
                    pbar.update(len(resp["data"]))

            logging.debug(f"{name}: loaded {len(items)} items")

            if show_progress:
                pbar.close()

            return items
        except RequestException as e:
            retries += 1
            logging.warning(f"Error loading data (retry {retries}): {e}")
            time.sleep(5)  # 等待一段时间后重试

    logging.error(f"Failed to load data after {MAX_RETRIES} retries.")
    return None

def load_user_collections():
    """
    从Bangumi API加载用户的收藏信息并将数据保存到本地文件。

    Returns:
        list or None: 成功加载的用户收藏数据列表。如果加载失败则返回None。
    """
    # 构建 获取USERNAME_OR_UID收藏的API端点URL，查看私有收藏需要access token。
    endpoint = f"{API_SERVER}/v0/users/{USERNAME_OR_UID}/collections"
    limit = 30
    # 使用load_data_until_finish函数加载数据，show_progress=True表示显示加载进度
    collections = load_data_until_finish(endpoint, limit, "user collections", show_progress=True)
    logging.info(f"loaded {len(collections)} collections")
    # 将用户收藏数据写入本地文件collections.json
    with open("collections.json", "w", encoding="u8") as f:
        json.dump(collections, f, ensure_ascii=False, indent=4)

    return collections

def migrate_collections():
    # 读取JSON文件
    with open('simplified_collections.json', 'r', encoding='utf-8') as f:
        data_from_json = json.load(f)

    # 处理JSON数据并进行迁移
    for item in data_from_json:
        subject_id = item["subject_id"]
        status = item["type"] 
        rate = item["rate"]
        comment = item["comment"]
        private = item["private"]
        tags = item["tags"]
        tags_list = tags if tags else [""]

        url = f'{API_SERVER}/v0/users/-/collections/{subject_id}'
        data = {
            "type": status,
            "rate": rate,
            "comment": comment,
            "private": private,
            "tags": tags_list
        }

        # 发送请求
        with requests.Session() as session:
            errors = make_request(session, url, method='POST', data=data)

            if errors:
                # 处理请求失败的信息，例如记录到日志中
                for error_message in errors:
                    logging.error(error_message)

        # 等待一定时间
        time.sleep(WAIT_TIME)

def make_request(session, url, method='GET', data=None, max_retries=3, wait_time=5):
    base_headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
        'User-Agent': 'Adachi/BangumiMigrate(https://github.com/Adachi-Git/BangumiMigrate)',
        'Authorization': 'Bearer ' + ACCESS_TOKEN_2,
    }

    errors = []  # 用于存储请求失败的信息

    for attempt in range(max_retries + 1):
        try:
            # 发起HTTP请求
            response = session.request(method, url, headers=base_headers, json=data)
            response.raise_for_status()

            # 记录请求信息
            logging.info(f"Request to {url} - Status Code: {response.status_code}")
            logging.debug("Request Headers:")
            logging.debug(base_headers)

            return response

        except requests.exceptions.RequestException as e:
            # 记录请求失败的错误信息
            error_message = f"Request to {url} failed: {e}"
            errors.append(error_message)
            logging.error(error_message)

            if attempt < max_retries:
                logging.warning(f"Retrying request to {url} (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)

    return errors  # 返回请求失败的信息列表

def main():
    # 检查是否存在本地的simplified_collections.json
    simplified_collections_exists = os.path.isfile('simplified_collections.json')

    if simplified_collections_exists:
        # 询问用户是否跳过collections
        user_choice = input("本地存在simplified_collections.json文件。是否跳过收藏信息采集？ (y/n): ").lower()
        if user_choice == 'n':
            logging.info("开始获取用户收藏信息...")
            user_collections = load_user_collections()

            simplified_collections = []
            for item in user_collections:
                simplified_item = {
                    "updated_at": item["updated_at"],
                    "comment": item["comment"],
                    "tags": item["tags"],
                    "subject_id": item["subject_id"],
                    "vol_status": item["vol_status"],
                    "ep_status": item["ep_status"],
                    "subject_type": item["subject_type"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "private": item["private"]
                }
                simplified_collections.append(simplified_item)

            with open("simplified_collections.json", "w", encoding="u8") as f:
                json.dump(simplified_collections, f, ensure_ascii=False, indent=4)

    logging.info("开始进行收藏信息迁移...")
    migrate_collections()

    logging.info("完成")

if __name__ == "__main__":
    import os  # 添加导入 os 模块
    main()
