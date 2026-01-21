# 家庭财务管理系统  
# Family Finance Management System

一个基于 **Excel + Python + HTML** 的轻量级家庭财务管理系统示例，  
用于个人或家庭进行日常收支记录、分类整理与简单的数据展示。

A lightweight **Family Finance Management System** based on **Excel, Python, and HTML**,  
designed for personal or household income & expense tracking, categorization, and basic visualization.

> ⚠️ 本仓库为 **公开模板项目**，不包含任何真实家庭财务数据。  
> ⚠️ This repository is a **public template project** and contains **no real personal financial data**.

---

## 功能概览 | Features

- 📊 Excel 财务模板（收支记录、分类管理）  
- 🐍 Python 脚本功能：  
  - 初始化家庭财务系统  
  - 同步与处理 Excel 财务数据  
  - 启动本地 Web 服务  
- 🌐 HTML 页面用于数据展示或辅助交互  
- 📄 提供中文《使用说明》和《快速启动指南》

- 📊 Excel templates for income & expense tracking  
- 🐍 Python scripts for:  
  - System initialization  
  - Financial data synchronization and processing  
  - Local web server startup  
- 🌐 HTML page for data visualization or interaction  
- 📄 Chinese documentation (User Guide & Quick Start)

---

## 项目结构 | Project Structure

```text
.
├── 家庭财务管理系统.xlsx              # Excel 财务模板（无真实数据）
├── templete data.xlsx                        # 示例/备份文件（可选）
├── family_finance_web.html            # 前端页面
├── create_family_finance_system.py    # 系统初始化脚本
├── sync_finance_data.py               # 财务数据同步与处理
├── start_server.py                    # Web 服务（完整版）
├── start_server_simple.py             # Web 服务（简化版）
├── install_dependencies.py            # 依赖安装脚本
├── requirements.txt                   # Python 依赖列表
├── README.md
├── 使用说明.docx
└── 快速启动指南.docx
```

---

## 环境要求 | Requirements

- Python 3.8 或以上版本  
- 推荐使用虚拟环境（venv）

- Python 3.8 or later  
- Virtual environment (venv) is recommended

---

## 安装依赖 | Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 快速开始 | Quick Start

### 1️⃣ 初始化家庭财务系统  
### Initialize the finance system

```bash
python create_family_finance_system.py
```

---

### 2️⃣ 启动本地 Web 服务（二选一）  
### Start the local web server (choose one)

```bash
python start_server.py
```

或 / or：

```bash
python start_server_simple.py
```

---

### 3️⃣ 打开网页页面  
### Open the web page

- 直接打开：
```text
family_finance_web.html
```

- 或在浏览器中访问 Python 服务启动后提示的本地地址

Open `family_finance_web.html` directly,  
or access the local address printed after starting the Python server.

---

## Excel 使用说明 | Excel Usage

- `家庭财务管理系统.xlsx` 为 **模板文件**  
- 建议复制一份后再填写真实财务数据  
- 请勿将包含真实财务数据的 Excel 文件上传至公开仓库

- `家庭财务管理系统.xlsx` is a **template file**  
- Make a copy before entering real financial data  
- Do **not** upload files containing real financial information to public repositories

---

## 数据与隐私声明 | Data & Privacy Notice

- 本仓库不包含任何真实家庭财务数据  
- 所有 Excel 文件仅用于模板或示例  
- 使用者需自行做好数据备份与隐私保护

- This repository contains **no real personal financial data**  
- All Excel files are templates or examples only  
- Users are responsible for their own data backup and privacy protection

---

## 适用人群 | Intended Audience

- 希望使用 Excel + Python 管理家庭账目的用户  
- Python 初学者或数据处理练习者  
- 轻量级个人/家庭财务系统示例参考

- Users who want to manage household finances using Excel and Python  
- Python beginners or data processing learners  
- Reference implementation of a lightweight personal finance system

---

## License

MIT License (optional – can be added if needed)

