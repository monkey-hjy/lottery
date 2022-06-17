# lottery
B站参加抽奖

## 使用方法
1. 使用 `requirements.txt` 文件安装依赖
2. 使用下方表结构代码建表
3. code目录下新建config.ini文件，内容如下

#### 表结构
```sql
create table lottery
(
    id          int auto_increment
        primary key,
    l_id        varchar(100)                       null comment '抽奖动态ID',
    uid         varchar(100)                       null comment '用户ID',
    open_time   int                                null comment '开奖时间戳',
    my_cv_id    varchar(100)                       null comment '转发的动态ID',
    create_time datetime default CURRENT_TIMESTAMP null
)
    comment 'b站抽奖信息';
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
