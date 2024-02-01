# Bangumi2Bangumi

Bangumi2Bangumi，一个用于将您在    [Bangumi](https://bgm.tv/)    网站上的收藏数据，从一个账号迁移到另一个账号的工具。通过调用 Bangumi API，您可以更新收藏状态、评分、评价等信息。

## 使用方法

1.  **安装**: 将存储库克隆到本地计算机。

   ```bash
   git clone https://github.com/Adachi-Git/Bangumi2Bangumi.git
   cd Bangumi2Bangumi
   ```

2. **安装依赖**  
   ```bash
   pip install -r requirements.txt

2.  **配置**：创建一个 config.ini 文件，包含您的 API 访问令牌和用户ID

[API_FETCH]
user_id = 您的UID(设置了用户名之后无法使用 UID ，写用户名即可)
Aaccess_token = 您的大号

[API_ADD]
access_token = 您的小号


3.  **使用**

```bash
python B2B.py
```

## 已知问题
Bangumi2Bangumi-Csv版还没写获取收藏导出为csv，用的    [Bangumi](https://github.com/czy0729/Bangumi)    本地备份导出csv。

我认为 CSV 在某种程度上更方便，所以还没有丢弃这个版本。

## 注意事项
请确保您的网络连接正常，Bangumi API 可以访问，并且您的令牌设置正确。

请谨慎使用此工具，确保您了解 Bangumi API 的使用规则，以及对数据更新操作的后果。

请备份好您的数据，特别是在大量更新操作之前。

## 免责声明
本工具由用户自行使用，使用过程中的任何问题或数据丢失，开发者概不负责。请谨慎操作，确保数据安全。
