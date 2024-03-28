import requests
import json
import configparser


def bangumi_api_fetch(user_id, Access_token, limit=50):
    base_url = "https://api.bgm.tv/v0/users"
    collections_endpoint = f"{base_url}/{user_id}/collections"

    headers = {
        'Authorization': 'Bearer ' + Access_token,
        'accept': 'application/json',
        'User-Agent': 'Adachi/BangumiMigrate(https://github.com/Adachi-Git/Bangumi2Bangumi)'
    }

    all_collections = []
    offset = 0

    while True:
        params = {
          #  'subject_type': 2,  # Anime
            'limit': limit,
            'offset': offset
        }

        response = requests.get(collections_endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)

            if total == 0:
                print("No Bangumi collections found.")
                break

            all_collections.extend(data.get('data', []))

            if len(all_collections) >= total:
                print(f"Total number of Bangumi collections: {total}")
                break

            offset += limit
        else:
            print(f"Failed to fetch Bangumi collections. Status code: {response.status_code}")
            break

    # 输出到默认的 JSON 文件中
    output_filename = 'bangumi_collections.json'
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(all_collections, json_file, ensure_ascii=False, indent=2)

    print(f"Bangumi collections saved to {output_filename}")
    return all_collections

if __name__ == "__main__":
    # 从配置文件读取 Access_token 和 user_id
    config = configparser.ConfigParser()
    config.read('config.ini')
    Access_token = config.get('API_FETCH', 'Access_token')
    user_id = config.get('API_FETCH', 'user_id')

    limit = 50

    # 获取收藏信息
    bangumi_collections = bangumi_api_fetch(Access_token, user_id, limit)

    # 打印获取到的收藏信息
    print(bangumi_collections)