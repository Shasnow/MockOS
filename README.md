# MockOS

是时候玩一下模拟终端游戏了！

天哪，我早就想执行 `rm -rf /` 来删除整个文件系统了！

尽在MockOS，您可以安全地执行 `rm -rf /` 来删除整个文件系统！

这是一个用Python实现的 `Linux风味` 模拟操作系统，提供基本的命令行界面和系统操作功能。

> **注意**：本项目仅供**娱乐和学习**使用，是一个模拟的操作系统环境，并非真实的Linux系统  
> 本项目中的命令实现不代表真实的Linux命令行为   
> 执行某些恶意命令可能会真实的影响您的计算机！  

## 功能特性

- **命令行界面**：提供类似Linux的交互式shell
- **核心命令**：实现了常用的Linux命令

## 安装

### 前置要求

- Python 3.6+

### 安装步骤

1. 克隆或下载项目到本地
2. 确保 Python 已安装并添加到 PATH
3. 运行 MockOS :

```bash
cd MockOS
python MockOS.py
```

## 使用方法

### 启动 MockOS

```bash
python MockOS.py
```

### 退出 MockOS

在命令行中输入：
```
exit
```
或按 `Ctrl+Z`

## 支持的命令列表

| 命令        | 描述         |
|-----------|------------|
| `ls`      | 列出目录内容     |
| `mkdir`   | 创建目录       |
| `rm`      | 删除文件或目录    |
| `cat`     | 查看文件内容     |
| `cd`      | 切换工作目录     |
| `python3` | Python解释器  |
| `echo`    | 输出文本       |
| `nl`      | 显示带行号的文件内容 |
| `pwd`     | 显示当前工作目录   |
| `grep`    | 文本搜索       |
| `whoami`  | 显示当前用户名    |

## 环境变量

MockOS支持以下环境变量：

| 变量名              | 描述            | 默认值           |
|------------------|---------------|---------------|
| MOCKOS_BASE_PATH | MockOS文件系统根目录 | mockos/       |
| MOCKOS_CWD       | 当前工作目录        | /root         |
| MOCKOS_USR_NAME  | 当前用户名         | root          |
| MOCKOS_USR_HOME  | 用户主目录         | /root         |
| MOCKOS_HOSTNAME  | 主机名           | localhost     |
| MOCKOS_PATH      | 命令搜索路径        | /bin:/usr/bin |

## 项目结构

```
MockOS/
├── MockOS.py              # 主程序入口
├── kernel/                # “内核”风味模块
├── mockos/                # 虚拟文件系统
│   ├── bin/               # 系统命令
│   ├── usr/
│   ├── etc/
│   └── root/              # root用户主目录
└── clean.py               # 清理脚本
```

## 更新日志

详细的版本历史和更新记录请查看 [CHANGELOG.md](CHANGELOG.md)

## 免责声明

本项目仅用于娱乐和学习目的，不提供任何形式的保证。使用本软件所产生的一切后果由使用者自行承担。本项目不保证：
- 系统的稳定性和可靠性
- 数据的安全性和完整性
- 与真实 Linux 系统的兼容性
- 任何特定用途的适用性

在任何情况下，作者或贡献者都不对任何直接、间接、偶然、特殊、惩罚性或后果性的损害（包括但不限于替代商品或服务的采购、使用、数据或利润的损失或业务中断）承担责任，无论是基于合同、严格责任还是侵权（包括过失或其他），即使已被告知此类损害的可能性。

## 许可证
```
MIT License

Copyright (c) 2025 Shasnow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
## 贡献

欢迎提交问题和改进建议！
