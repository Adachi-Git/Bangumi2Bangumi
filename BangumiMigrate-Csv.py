import requests
import pandas as pd
import time
import logging

# 提前定义 API 地址和常量
API_URL = 'https://api.bgm.tv/v0/users/-/collections/'
WAIT_TIME = 5

# 设置日志级别
logging.basicConfig(level=logging.INFO)

def map_status_to_type(status):
    # 根据状态映射到对应的 type，这里需要根据实际情况进行调整
    if "想" in status:
        return 1
    elif "读过" in status or "看过" in status or "玩过" in status or "听过" in status:
        return 2
    elif "在读" in status or "在看" in status or "在玩" in status or "在听" in status:
        return 3
    elif "搁置" in status:
        return 4
    elif "抛弃" in status:
        return 5
    else:
        return 0  # 未知状态

def make_request(session, url, method='GET', data=None):
    base_headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
        'User-Agent': 'Adachi/BangumiMigrate(https://github.com/Adachi-Git/BangumiMigrate)',  # 替换成你的自定义 User-Agent
        'Authorization': 'Bearer *****************************'  # 替换成你的访问令牌
    }

    try:
        response = session.request(method, url, headers=base_headers, json=data)
        response.raise_for_status()  # 检查请求是否成功

        # 记录日志
        logging.info(f"Request to {url} - Status Code: {response.status_code}")
        logging.debug("Request Headers:")
        logging.debug(base_headers)

    except requests.exceptions.RequestException as e:
        # 处理请求失败的情况，例如重试等
        logging.error(f"Request to {url} failed: {e}")

def process_row(row):
    # 获取 'ID'、'状态'、'评分'、'我的简评'、'私密' 和 '标签' 列的值
    collection_id = row.ID
    status = row.状态
    rate = row.我的评价
    comment = row.我的简评
    private = row.私密
    tags = row.标签.split() if not pd.isna(row.标签) else []

    # 根据状态映射到对应的 type
    type_value = map_status_to_type(status)

    # 动态生成请求的 URL
    url = f'{API_URL}{collection_id}'

    # 准备请求体数据
    data = {
        "type": type_value,
        "rate": int(float(rate)) if (not pd.isna(rate) and rate != '') else 0,
        "comment": str(comment).strip() if not pd.isna(comment) else "",
        "private": bool(private) if not pd.isna(private) else False,
        "tags": [tag.strip() for tag in tags] if tags else [""]
    }

    # 发送请求
    with requests.Session() as session:
        make_request(session, url, method='POST', data=data)

    # 等待一定时间
    time.sleep(WAIT_TIME)

# 读取 CSV 文件
df = pd.read_csv('F:\\Downlord\\1.csv')

# 处理每一行数据
for row in df.itertuples(index=False):
    process_row(row)