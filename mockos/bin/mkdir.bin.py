import os
import sys
import argparse


def main():
    """Create directories."""
    parser = argparse.ArgumentParser(description="Create directories")
    parser.add_argument("-p", "--parents", action="store_true", help="no error if existing, make parent directories as needed")
    parser.add_argument("-v", "--verbose", action="store_true", help="print a message for each created directory")
    parser.add_argument("directories", nargs="+", help="directories to create")
    
    args = parser.parse_args()
    
    base_path = os.environ.get("MOCKOS_BASE_PATH", "mockos")
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    exit_code = 0  # 默认成功
    
    for directory in args.directories:
        if not create_directory(base_path, cwd, directory, args.parents, args.verbose):
            exit_code = 1  # 至少有一个目录创建失败
    
    exit(exit_code)


def create_directory(base_path: str, cwd: str, path: str, create_parents: bool, verbose: bool) -> bool:
    """Create a single directory. Returns True if successful, False otherwise."""
    if path.startswith("/"):
        full_path = f"{base_path}{path}"
    else:
        if cwd == "/":
            full_path = f"{base_path}/{path}"
        else:
            full_path = f"{base_path}{cwd}/{path}"
    
    if os.path.exists(full_path):
        if os.path.isdir(full_path):
            if not create_parents:
                print(f"mkdir: cannot create directory '{path}': File exists", file=sys.stderr)
                return False
            else:
                return True  # 目录已存在，且使用了 -p 选项，视为成功
        else:
            print(f"mkdir: cannot create directory '{path}': File exists", file=sys.stderr)
            return False
    
    if create_parents:
        try:
            os.makedirs(full_path, exist_ok=True)
            if verbose:
                print(f"mkdir: created directory '{path}'")
            return True
        except PermissionError:
            print(f"mkdir: cannot create directory '{path}': Permission denied", file=sys.stderr)
            return False
        except OSError as e:
            print(f"mkdir: cannot create directory '{path}': {e}", file=sys.stderr)
            return False
    else:
        parent_dir = os.path.dirname(full_path)
        
        if parent_dir and not os.path.exists(parent_dir):
            print(f"mkdir: cannot create directory '{path}': No such file or directory", file=sys.stderr)
            return False
        
        try:
            os.mkdir(full_path)
            if verbose:
                print(f"mkdir: created directory '{path}'")
            return True
        except PermissionError:
            print(f"mkdir: cannot create directory '{path}': Permission denied")
            return False
        except OSError as e:
            print(f"mkdir: cannot create directory '{path}': {e}")
            return False


if __name__ == "__main__":
    main()
