from .environment import MockOSEnv
import os


class MockOSShell:
    def __init__(self, env: MockOSEnv):
        self.env = env

    def cd(self, arg):
        """Change the current working directory."""
        if not arg:
            arg = "~"
        
        target = arg
        
        if target == "~":
            target = self.env.USR_HOME
        elif target == "-":
            print(f"cd: OLDPWD not set")
            return
        
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
            print(f"cd: {arg}: No such file or directory")
            return
        
        if not os.path.isdir(full_path):
            print(f"cd: {arg}: Not a directory")
            return
        
        self.env.CWD = new_cwd