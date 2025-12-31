# MockOS 项目上下文文档

## 项目概述

MockOS 是一个用 Python 实现的 Linux 风格模拟操作系统，提供基本的命令行界面和文件系统操作功能。该项目仅供娱乐和学习使用，允许用户安全地执行 `rm -rf /` 等危险命令而不会对真实系统造成影响。

### 核心技术栈

- **编程语言**: Python 3.6+
- **依赖**: 仅使用 Python 标准库，无外部依赖
- **架构模式**: 模块化设计，分为内核模块和命令实现

### 项目架构

```
MockOS/
├── MockOS.py              # 主程序入口，基于 cmd.Cmd 的交互式 shell
├── kernel/                # 内核模块
│   ├── __init__.py        # 模块初始化
│   ├── environment.py     # 环境变量管理
│   └── shell.py           # shell 核心功能
├── mockos/                # 虚拟文件系统
│   ├── bin/               # 系统命令目录
│   │   ├── cat            # 文件内容查看命令
│   │   ├── ls             # 目录列表命令
│   │   ├── mkdir          # 创建目录命令
│   │   └── rm             # 删除文件/目录命令
│   ├── usr/bin/           # 用户命令目录
│   │   └── python3        # Python 解释器
│   ├── etc/               # 系统配置
│   │   └── passwd         # 用户信息
│   └── root/              # root 用户主目录
├── clean.py               # 清理脚本
├── README.md              # 项目说明文档
├── CHANGELOG.md           # 更新日志
└── LICENSE                # MIT 许可证
```

## 构建和运行

### 运行方式

```bash
# 启动交互式 shell
python MockOS.py

# 执行单个命令
python MockOS.py -c "ls -la"
python MockOS.py -e "cat hello.txt"
```

### 环境变量系统

MockOS 使用以下环境变量来管理虚拟环境：

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| MOCKOS_BASE_PATH | MockOS 文件系统根目录 | mockos/ |
| MOCKOS_CWD | 当前工作目录 | /root |
| MOCKOS_USR_NAME | 当前用户名 | root |
| MOCKOS_USR_HOME | 用户主目录 | /root |
| MOCKOS_HOSTNAME | 主机名 | localhost |
| MOCKOS_PATH | 命令搜索路径 | /bin:/usr/bin |

## 开发指南

### 添加新命令

1. 在 `mockos/bin/` 或 `mockos/usr/bin/` 目录下创建新的命令文件
2. 使用 `argparse` 解析命令行参数
3. 从环境变量中获取 MockOS 环境信息
4. 实现命令逻辑
5. 添加 `if __name__ == "__main__": main()` 入口

### 命令模板

```python
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Command description")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("file", help="File to process")
    
    args = parser.parse_args()
    
    base_path = os.environ.get("MOCKOS_BASE_PATH", "mockos")
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    # 实现命令逻辑
    print(f"Processing {args.file}")

if __name__ == "__main__":
    main()
```

### 路径处理

命令需要正确处理绝对路径和相对路径：

```python
if path.startswith("/"):
    full_path = f"{base_path}{path}"
else:
    if cwd == "/":
        full_path = f"{base_path}/{path}"
    else:
        full_path = f"{base_path}{cwd}/{path}"
```

## 已实现命令

| 命令 | 功能 | 支持参数 |
|------|------|----------|
| `ls` | 列出目录内容 | `-a` (显示隐藏文件), `-l` (详细列表) |
| `mkdir` | 创建目录 | `-p` (递归创建), `-v` (显示信息) |
| `rm` | 删除文件或目录 | `-r` (递归), `-f` (强制), `-v` (显示信息) |
| `cat` | 显示文件内容 | `-n` (显示行号), `-E` (显示行尾) |
| `cd` | 切换工作目录 | 支持绝对路径、相对路径、`~`、`..`、`.` |
| `python3` | Python 解释器 | 支持交互模式和脚本执行 |

## 内核模块

### environment.py

管理 MockOS 的环境变量系统，使用 `@dataclasses.dataclass` 定义环境变量结构：

- `MockOSEnv` 类：存储所有环境变量
- `store()` 方法：将环境变量转换为字典格式
- `restore()` 方法：从系统环境变量恢复状态

### shell.py

实现 shell 核心功能，主要包含：

- `cd()` 方法：目录切换逻辑，支持各种路径格式
- 路径解析：正确处理绝对路径、相对路径和特殊符号

## 命令执行机制

MockOS 使用 Python 的 `subprocess` 模块执行命令：

1. 解析命令行（支持带空格的参数）
2. 在 PATH 中查找命令脚本
3. 设置环境变量（用户环境 + MockOS 环境）
4. 使用 `subprocess.run()` 执行 Python 脚本
5. 处理输出和错误

## 测试和验证

### 测试方式

1. 启动 MockOS 并测试各个命令
2. 验证路径解析和环境变量
3. 测试命令参数和错误处理

### 常见测试用例

```bash
# 基本命令测试
ls -la
mkdir test_dir
cd test_dir
echo "hello" > test.txt
cat test.txt
rm test.txt
cd ..
rm -r test_dir

# 路径测试
cd /
cd ~
cd ..
cd ./test
cd /bin

# 错误处理测试
ls nonexistent_file
rm nonexistent_file
mkdir existing_file
```

## 注意事项

1. **安全性**: 虽然是模拟系统，但仍需注意恶意命令可能影响真实系统
2. **兼容性**: 命令实现不代表真实 Linux 命令的完整行为
3. **路径处理**: 所有路径操作都需要正确处理 MockOS 虚拟文件系统路径
4. **环境变量**: 命令应通过环境变量获取 MockOS 状态，而非硬编码路径

## 免责声明

本项目仅用于娱乐和学习目的，不提供任何形式的保证。使用本软件所产生的一切后果由使用者自行承担。