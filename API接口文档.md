# 1 用户接口

## 1.1 用户登录验证

- 请求路径：user/login
- 请求方法：post
- 请求参数

|  参数名  | 数据类型 | 是否为空 |     描述     |
| :------: | :------: | :------: | :----------: |
| username |  string  |    否    | 用户登录账号 |
| password |  string  |    否    | 用户登录密码 |

- 响应参数

|  参数名  | 数据类型 | 是否为空 |      描述      |
| :------: | :------: | :------: | :------------: |
| username |  string  |    否    |     用户名     |
|  token   |  string  |    否    | 客户端请求令牌 |

- 请求示例

```json
{
    "username":"xuhao",
    "password":"2016"
    }
```

- 响应示例

```json
{
    "token": "Inh1aGFvIg:1khFS6:f79SUdueIkbWILD2WTkrVRmNCEJahyrB0bLFqugHxHo",
    "username": "xuhao"
}
```

## 1.2 用户注册

- 请求路径

## 1.3 用户密码修改

## 1.4 用户个人信息

## 1.5 页面菜单

# 2 稿件记录模块

