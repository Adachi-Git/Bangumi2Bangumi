# BangumiMigrate

BangumiMigrate，一个用于将您在    [Bangumi](https://bgm.tv/)    网站上的收藏数据，从一个账号迁移到另一个账号的工具。通过调用 Bangumi API，您可以更新收藏状态、评分、评价等信息。

## 已知问题
BangumiMigrate-Csv版还没写获取收藏导出为csv，用的    [Bangumi](https://github.com/czy0729/Bangumi)    本地备份导出csv。

## 使用前准备

在使用之前，请确保您已经安装了必要的依赖库，您可以使用以下命令安装：

```bash
pip install requests
pip install tqdm
```
## 配置
在代码中提供了一些需要配置的参数，以确保工具能够正确运行。以下是需要注意的配置项：

- `USERNAME_OR_UID`: 大号或要获取收藏信息的账户的用户名或用户ID。
- `ACCESS_TOKEN`: 大号的访问令牌，用于获取收藏信息。
- `ACCESS_TOKEN_2`: 小号的访问令牌，用于进行收藏信息的迁移。

## 运行
1. 运行 `BangumiMigrate.py`：

    ```bash
    python BangumiMigrate.py
    ```

3. 根据提示输入相应的信息，选择是否跳过收藏信息的获取。

4. 等待程序执行完毕，完成收藏信息的迁移。

## 注意事项
请确保您的网络连接正常，Bangumi API 可以访问，并且您的令牌设置正确。

请谨慎使用此工具，确保您了解 Bangumi API 的使用规则，以及对数据更新操作的后果。

请备份好您的数据，特别是在大量更新操作之前。
## 免责声明
本工具由用户自行使用，使用过程中的任何问题或数据丢失，开发者概不负责。请谨慎操作，确保数据安全。
