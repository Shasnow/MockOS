import os
import sys
import shutil
import argparse


def main():
    """Remove files or directories."""
    parser = argparse.ArgumentParser(description="Remove files or directories")
    parser.add_argument("-r", "-R", "--recursive", action="store_true", help="remove directories and their contents recursively")
    parser.add_argument("-f", "--force", action="store_true", help="ignore nonexistent files and arguments, never prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")
    parser.add_argument("targets", nargs="+", help="files or directories to remove")
    
    args = parser.parse_args()
    
    base_path = os.environ.get("MOCKOS_BASE_PATH", "mockos")
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    exit_code = 0  # 默认成功
    
    for target in args.targets:
        if not remove_target(base_path, cwd, target, args.recursive, args.force, args.verbose):
            exit_code = 1  # 至少有一个目标删除失败
    
    exit(exit_code)


def remove_target(base_path: str, cwd: str, path: str, recursive: bool, force: bool, verbose: bool) -> bool:
    """Remove a single file or directory. Returns True if successful, False otherwise."""
    if path.startswith("/"):
        full_path = f"{base_path}{path}"
    else:
        if cwd == "/":
            full_path = f"{base_path}/{path}"
        else:
            full_path = f"{base_path}{cwd}/{path}"

    if not os.path.exists(full_path):
        if not force:
            print(f"rm: cannot remove '{path}': No such file or directory", file=sys.stderr)
            return False
        else:
            return True  # 使用了 -f 选项，文件不存在不算错误

    if os.path.isfile(full_path) or os.path.islink(full_path):
        try:
            os.remove(full_path)
            if verbose:
                print(f"removed '{path}'")
            return True
        except PermissionError:
            if not force:
                print(f"rm: cannot remove '{path}': Permission denied", file=sys.stderr)
                return False
            else:
                return True  # 使用了 -f 选项，权限错误不算错误
        except OSError as e:
            if not force:
                print(f"rm: cannot remove '{path}': {e}", file=sys.stderr)
                return False
            else:
                return True  # 使用了 -f 选项，其他错误不算错误
    elif os.path.isdir(full_path):
        if not recursive:
            if not force:
                print(f"rm: cannot remove '{path}': Is a directory", file=sys.stderr)
                return False
            else:
                return True  # 使用了 -f 选项，目录不算错误

        try:
            shutil.rmtree(full_path)
            if verbose:
                print(f"removed directory '{path}'")
            return True
        except PermissionError:
            if not force:
                print(f"rm: cannot remove '{path}': Permission denied", file=sys.stderr)
                return False
            else:
                return True  # 使用了 -f 选项，权限错误不算错误
        except OSError as e:
            if not force:
                print(f"rm: cannot remove '{path}': {e}", file=sys.stderr)
                return False
            else:
                return True  # 使用了 -f 选项，其他错误不算错误
    
    return True


if __name__ == "__main__":
    main()
