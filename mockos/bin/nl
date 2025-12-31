import os
import sys
import argparse

def main():
    """Display content from stdin or files with line numbers."""
    parser = argparse.ArgumentParser(description="Display content from stdin or files with line numbers")
    parser.add_argument("files", nargs="*", help="files to display (if none, read from stdin)")
    parser.add_argument("-n", "--number", action="store_true", help="number all output lines")
    
    args = parser.parse_args()
    
    base_path = os.environ.get("MOCKOS_BASE_PATH", "mockos")
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    exit_code = 0
    
    def process_content(content_lines):
        """处理内容行并输出"""
        for i, line in enumerate(content_lines, 1):
            if args.number:
                sys.stdout.write(f"{i:>6}\t{line}")
            else:
                sys.stdout.write(f"{i:>6}\t{line}")
    
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
                    print(f"nl: {file_arg}: No such file or directory", file=sys.stderr)
                    exit_code = 1
                    continue
                
                if os.path.isdir(full_path):
                    print(f"nl: {file_arg}: Is a directory", file=sys.stderr)
                    exit_code = 1
                    continue
                
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        process_content(lines)
                except Exception as e:
                    print(f"nl: {file_arg}: {str(e)}", file=sys.stderr)
                    exit_code = 1
        else:
            # 从标准输入读取
            lines = sys.stdin.readlines()
            process_content(lines)
    
    except Exception as e:
        print(f"nl: {str(e)}", file=sys.stderr)
        exit_code = 1
    
    exit(exit_code)

if __name__ == "__main__":
    main()