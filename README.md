# lottery
B站参加抽奖

## 使用方法
1. 使用 `requirements.txt` 文件安装依赖
2. 使用下方表结构代码建表
3. code目录下新建config.ini文件，内容如下

#### 表结构
```sql
CREATE TABLE `lottery`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `l_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '抽奖动态ID',
  `uid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户ID',
  `my_cv_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '转发的动态ID',
  `open_time` int NULL DEFAULT NULL COMMENT '开奖时间戳',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `win_uid` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '中奖用户ID\r\n',
  `me_win` int NULL DEFAULT NULL COMMENT '是否是我中奖。0-否   1-是',
  `is_delete` int NOT NULL DEFAULT 0 COMMENT '0-正常   1-删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 165 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'b站抽奖信息' ROW_FORMAT = Dynamic;
```

#### config.ini
```ini
[mysql_info]
host = localhost
user = root
passwd = root
db = demo
port = 3306

[cookie]
cookie = B站登录后的cookie

[keywords]
keywords = 抽奖三原则: ①从不缺席[doge] ②从不中奖[doge] ③从不放弃[doge]

[redis]
host = localhost
port = 6379
password = redis密码
db = 0
```
