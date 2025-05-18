此项目为[TGP258/chuni_b50](https://github.com/TGP258/chuni_b50)的衍生项目，主要使用了Flask+MySQL实现了一个简单的CHUNITHM乐曲信息查询网站。

> Tips：目前仅实现了查歌功能，B50(B30)功能尚未完整移植

## 关于数据库 

### 数据库设计

该项目使用MySQL作为数据库，建表语句详见此项目的zh

表：songs

| 字段名      | 类型         | 说明         |
| ----------- | ------------ | ------------ |
| id          | int          | 乐曲ID       |
| title       | varchar(255) | 乐曲名       |
| artist      | varchar(255) | 作者         |
| genre       | varchar(100) | 分类         |
| bpm         | int          | 乐曲BPM值    |
| origin_from | varchar(100) | 收录版本     |
| created_at  | timestamp    | 数据创建时间 |
| updated_at  | timestamp    | 数据更新时间 |

表：difficulties

| 字段名          | 类型         | 说明                             |
| --------------- | ------------ | -------------------------------- |
| id              | int          | 主键                             |
| song_id         | int          | 外键 与songs表<br />的id字段关联 |
| difficulty_type | enum         | 难度类型                         |
| level_value     | decimal(4,1) | 难度定数                         |
| level_display   | varchar(10)  | 标识等级                         |
| chart_id        | int          | 谱面ID                           |
| combo           | int          | 该难度的物量                     |
| charter         | varchar(255) | 该难度的谱师名                   |