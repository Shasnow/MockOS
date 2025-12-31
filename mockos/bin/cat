import os
import sys
import argparse

def main():
    """Concatenate and display files."""
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(description="Concatenate and display files")
    parser.add_argument("-n", "--number", action="store_true", help="number all output lines")
    parser.add_argument("-E", "--show-ends", action="store_true", help="display $ at end of each line")
    parser.add_argument("files", nargs="+", help="files to display")
    
    args = parser.parse_args()
    
    base_path = os.environ.get("MOCKOS_BASE_PATH", "mockos")
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    exit_code = 0  # 默认成功
    
    for file_arg in args.files:
        if file_arg.startswith("/"):
            full_path = f"{base_path}{file_arg}"
        else:
            if cwd == "/":
                full_path = f"{base_path}/{file_arg}"
            else:
                full_path = f"{base_path}{cwd}/{file_arg}"
        
        if not os.path.exists(full_path):
            print(f"cat: {file_arg}: No such file or directory", file=sys.stderr)
            exit_code = 1  # 文件不存在
            continue
        
        if os.path.isdir(full_path):
            print(f"cat: {file_arg}: Is a directory", file=sys.stderr)
            exit_code = 1  # 是目录而不是文件
            continue
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
                if args.number:
                    for i, line in enumerate(lines, 1):
                        if args.show_ends:
                            line = line.rstrip("\n") + "$\n"
                        sys.stdout.write(f"{i:>6}\t{line}")
                else:
                    for line in lines:
                        if args.show_ends:
                            line = line.rstrip("\n") + "$\n"
                        sys.stdout.write(line)
        except PermissionError:
            print(f"cat: {file_arg}: Permission denied", file=sys.stderr)
            exit_code = 1  # 权限错误
        except Exception as e:
            print(f"cat: {file_arg}: {str(e)}", file=sys.stderr)
            exit_code = 1  # 其他错误
    
    exit(exit_code)


if __name__ == "__main__":
    main()
