import os
import sys
import argparse
import re

def main():
    """Search for patterns in files or stdin."""
    parser = argparse.ArgumentParser(description="Search for patterns in files or stdin")
    parser.add_argument("pattern", help="pattern to search for")
    parser.add_argument("files", nargs="*", help="files to search (if none, read from stdin)")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case distinctions")
    parser.add_argument("-n", "--line-number", action="store_true", help="prefix each line of output with the line number")
    parser.add_argument("-v", "--invert-match", action="store_true", help="select non-matching lines")
    
    args = parser.parse_args()
    
    base_path = os.environ.get("MOCKOS_BASE_PATH", "mockos")
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    # 编译正则表达式
    flags = re.IGNORECASE if args.ignore_case else 0
    try:
        pattern = re.compile(args.pattern, flags)
    except re.error as e:
        print(f"grep: {e}", file=sys.stderr)
        exit(2)
    
    exit_code = 1  # 默认没有匹配
    
    def search_lines(lines, filename=""):
        """搜索行并输出匹配的行"""
        nonlocal exit_code
        for line_num, line in enumerate(lines, 1):
            match = pattern.search(line)
            if (match and not args.invert_match) or (not match and args.invert_match):
                if args.line_number:
                    if filename:
                        print(f"{filename}:{line_num}:{line.rstrip()}")
                    else:
                        print(f"{line_num}:{line.rstrip()}")
                else:
                    print(line.rstrip())
                exit_code = 0  # 找到匹配
    
    try:
        if args.files:
            # 处理文件
            for file_arg in args.files:
                if file_arg.startswith("/"):
                    full_path = f"{base_path}{file_arg}"
                else:
                    if cwd == "/":
                        full_path = f"{base_path}/{file_arg}"
                    else:
                        full_path = f"{base_path}{cwd}/{file_arg}"
                
                if not os.path.exists(full_path):
                    print(f"grep: {file_arg}: No such file or directory", file=sys.stderr)
                    continue
                
                if os.path.isdir(full_path):
                    print(f"grep: {file_arg}: Is a directory", file=sys.stderr)
                    continue
                
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        search_lines(lines, file_arg if len(args.files) > 1 else "")
                except Exception as e:
                    print(f"grep: {file_arg}: {str(e)}", file=sys.stderr)
        else:
            # 从标准输入读取
            try:
                lines = sys.stdin.readlines()
                if lines:
                    search_lines(lines)
            except Exception as e:
                print(f"grep: error reading stdin: {str(e)}", file=sys.stderr)
                exit(2)
    
    except KeyboardInterrupt:
        exit(130)  # SIGINT
    except Exception as e:
        print(f"grep: {str(e)}", file=sys.stderr)
        exit(2)
    
    exit(exit_code)

if __name__ == "__main__":
    main()