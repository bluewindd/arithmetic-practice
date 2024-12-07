# 算术练习软件

一个帮助小学生练习基础算术的 Web 应用。

## 功能特点

- 支持加减乘除四则运算
- 可自定义题目数量和难度
- 实时评分和错题提示
- 错题集功能
- 九九乘法表和练习模式
- 详细的解题步骤说明

## 技术栈

- 后端：Flask
- 前端：HTML5, CSS3, JavaScript
- 无需数据库，使用会话存储

## 安装和运行

1. 克隆仓库：
bash
git clone https://github.com/bluewindd/arithmetic-practice.git
cd arithmetic-practice
2. 创建并激活虚拟环境：
bash
python -m venv venv
3. 安装依赖：
bash
pip install -r requirements.txt
4. 运行应用：
bash
python suanshu.py
5. 访问应用：
   打开浏览器访问 `http://localhost:5001`

## 使用说明

1. 基本设置：
   - 设置题目数量（1-50题）
   - 设置数字范围（1-100）
   - 选择运算符（加减乘除）
   - 设置结果范围

2. 特色功能：
   - 实时评分和错题提示
   - 详细的解题步骤说明
   - 错题集管理和复习
   - 九九乘法表练习

## 项目结构
arithmetic-practice/
   ├── static/
   │ └── css/
   │ └── style.css
   ├── templates/
   │ └── index.html
   ├── suanshu.py
   ├── requirements.txt
   ├── README.md
   └── .gitignore
## 开发计划

- [ ] 添加用户系统
- [ ] 添加练习历史记录
- [ ] 支持自定义题目模板
- [ ] 添加更多的可视化解题步骤
- [ ] 优化移动端体验
- [ ] 直接做成安卓应用

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
