from .environment import MockOSEnv
import os
import sys


class MockOSShell:
    def __init__(self, env: MockOSEnv):
        self.env = env
    
    def is_builtin_command(self, command:str) -> bool:
        """检查是否为内置命令"""
        return hasattr(self, command) and callable(getattr(self, command))
    
    def execute_builtin_command(self, command:str, args:list) -> int:
        """执行内置命令"""
        try:
            func = getattr(self, command)
            return func(args)
        except AttributeError:
            return 1  # 命令不存在

    def cd(self, args:list) -> int:
        """Change the current working directory."""
        arg = args[0] if args else ""
        if not arg:
            arg = "~"
        
        target = arg
        
        if target == "~":
            target = self.env.USR_HOME
        elif target == "-":
            print(f"cd: OLDPWD not set", file=sys.stderr)
            return 1
        
        if target.startswith("/"):
            new_cwd = target
        else:
            if target == ".":
                new_cwd = self.env.CWD
            elif target == "..":
                if self.env.CWD == "/":
                    new_cwd = "/"
                else:
                    new_cwd = os.path.dirname(self.env.CWD)
                    if not new_cwd:
                        new_cwd = "/"
            else:
                if self.env.CWD == "/":
                    new_cwd = f"/{target}"
                else:
                    new_cwd = f"{self.env.CWD}/{target}"
        
        full_path = os.path.join(self.env.BASE_PATH, new_cwd.lstrip("/"))
        
        if not os.path.exists(full_path):
            print(f"cd: {arg}: No such file or directory", file=sys.stderr)
            return 1
        
        if not os.path.isdir(full_path):
            print(f"cd: {arg}: Not a directory", file=sys.stderr)
            return 1
        
        self.env.CWD = new_cwd
        return 0

    def pwd(self, _):
        """Print the current working directory."""
        print(self.env.CWD)
        return 0
    
    def whoami(self, _):
        """Print the current user."""
        print(self.env.USR_NAME)
        return 0

    def true(self, _):
        """Return true."""
        return 0

    def false(self, _):
        """Return false."""
        return 1

    def hostname(self, _):
        """Print the hostname."""
        print(self.env.HOST_NAME)
        return 0
