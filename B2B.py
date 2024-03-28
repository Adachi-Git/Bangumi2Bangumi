# main.py
import configparser
from bangumi_api_fetch import bangumi_api_fetch
from bangumi_api_add import bangumi_api_add_collection

if __name__ == "__main__":
    # 从配置文件读取 user_id 、Access_token 和 access_token
    config = configparser.ConfigParser()
    config.read('config.ini')
    user_id_fetch = config.get('API_FETCH', 'user_id')
    access_token_fetch = config.get('API_FETCH', 'Access_token')

    access_token_add = config.get('API_ADD', 'access_token')

    limit = 50

    # 获取收藏信息
    bangumi_collections = bangumi_api_fetch(user_id_fetch, access_token_fetch, limit)

    # 向API发送收藏请求
    bangumi_api_add_collection(bangumi_collections, access_token_add)
