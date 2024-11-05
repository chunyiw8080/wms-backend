# Users route
定义了用户相关功能的路由路径

| 路径                    |请求类型| 功能            |
|:----------------------|:--:|:--------------|
| /users/all            |GET| 获取全部的用户信息     |
| /users/<user_id>      |GET| 获取指定用户id的信息   |
| /users/login          |POST| 用户登录验证        |
| /users/create         |POST| 新建用户          |
| /users/delete/<user_id>|DELETE| 根据user_id删除用户 |
| /users/update/<user_id>|PATCH| 根据user_id更新用户信息|

# Employees route
| 路径                     |请求类型| 功能                |
|:-----------------------|:--:|:------------------|
| /employees/all         |GET| 获取全部员工信息          |
| /employees/create      |POST| 创建新的员工            |
| /employees/<employee_id>|GET| 根据employee_id获取员工信息|