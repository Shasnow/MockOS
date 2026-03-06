import os
import sys
import stat
import argparse
from datetime import datetime

def main():
    """List files in the current directory."""
    parser = argparse.ArgumentParser(description="List files in the current directory")
    parser.add_argument("-a", "--all", action="store_true", help="show all files, including hidden files")
    parser.add_argument("-l", "--long", action="store_true", help="use a long listing format")
    parser.add_argument("-1", "--one-per-line", dest="one_per_line", action="store_true", help="list one file per line")
    parser.add_argument("path", nargs="?", default=".", help="directory or file to list")
    
    args = parser.parse_args()
    
    base_path = os.environ.get("MOCKOS_BASE_PATH", "mockos")
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    path = args.path
    
    if path.startswith("/"):
        full_path = f"{base_path}{path}"
    else:
        if cwd == "/":
            full_path = f"{base_path}/{path}"
        else:
            full_path = f"{base_path}{cwd}/{path}"
    
    if not os.path.exists(full_path):
        print(f"ls: cannot access '{path}': No such file or directory", file=sys.stderr)
        exit(2)
    
    if os.path.isfile(full_path):
        if args.long:
            print(get_file_info(full_path))
        else:
            print(os.path.basename(full_path))
        exit(0)  # 成功
    
    if not os.path.isdir(full_path):
        print(f"ls: cannot access '{path}': No such file or directory", file=sys.stderr)
        exit(2)
    
    try:
        entries = os.listdir(full_path)
    except PermissionError:
        print(f"ls: cannot open directory '{path}': Permission denied", file=sys.stderr)
        exit(1)
    
    entries.sort()
    entries = [entry.replace(".bin.py", "") for entry in entries]
    
    if args.long:
        total = 0
        items = []
        for entry in entries:
            if not args.all and entry.startswith("."):
                continue
            entry_path = os.path.join(full_path, entry)
            items.append(get_file_info(entry_path))
            total += os.path.getsize(entry_path) if os.path.isfile(entry_path) else 4096
        print(f"total {total // 1024}")
        for item in items:
            print(item)
    else:
        if args.one_per_line:
            # 每行一个文件
            for entry in entries:
                if not args.all and entry.startswith("."):
                    continue
                print(entry)
        else:
            # 使用原来的格式（一行多个文件）
            display_items = []
            for entry in entries:
                if not args.all and entry.startswith("."):
                    continue
                entry_path = os.path.join(full_path, entry)
                if os.path.isdir(entry_path):
                    display_items.append(f"\033[34m{entry}\033[0m")
                else:
                    display_items.append(entry)
            print("  ".join(display_items))
    
    exit(0)  # 成功


def get_file_info(path: str) -> str:
    """Get detailed file information."""
    stat_info = os.stat(path)
    name = os.path.basename(path)
    
    perms = get_permissions(stat_info.st_mode)
    nlink = stat_info.st_nlink
    size = stat_info.st_size
    mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime("%b %d %H:%M")
    
    return f"{perms} {nlink:>2} root root {size:>8} {mtime} {name}"


def get_permissions(mode: int) -> str:
    """Get permission string from mode."""
    perms = ""
    perms += "d" if stat.S_ISDIR(mode) else "-"
    perms += "r" if mode & stat.S_IRUSR else "-"
    perms += "w" if mode & stat.S_IWUSR else "-"
    perms += "x" if mode & stat.S_IXUSR else "-"
    perms += "r" if mode & stat.S_IRGRP else "-"
    perms += "w" if mode & stat.S_IWGRP else "-"
    perms += "x" if mode & stat.S_IXGRP else "-"
    perms += "r" if mode & stat.S_IROTH else "-"
    perms += "w" if mode & stat.S_IWOTH else "-"
    perms += "x" if mode & stat.S_IXOTH else "-"
    return perms


if __name__ == "__main__":
    main()
