# lottery
B站参加抽奖

### 使用方法
1. 使用 `requirements.txt` 文件安装依赖
2. 使用下方表结构代码建表
3. 修改配置文件中的信息

### 表结构
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
