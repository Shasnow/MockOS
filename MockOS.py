import cmd
import os
import sys
import subprocess
from kernel import MockOSEnv, MockOSShell

class MockOS(cmd.Cmd):
    intro = "Welcome to MockOS. Type help or ? to list commands.\n"
    mock_env = MockOSEnv()
    shell = MockOSShell(mock_env)
    prompt = mock_env.prompt
    bin_dir = f"{mock_env.BASE_PATH}/bin"
    
    def update_prompt(self):
        self.prompt = self.mock_env.prompt

    def do_exit(self, _):
        """Exit the program."""
        return True

    def do_EOF(self, _):
        """Exit the program."""
        print()  # 打印一个换行符
        return True

    def emptyline(self):
        return
    
    def onecmd(self, line):
        """重写 onecmd 方法以支持命令链操作符和管道"""
        # 解析包含 &&、|| 和 | 操作符的命令行
        commands = self.parse_command_line(line)
        last_exit_code = 0
        should_execute = True  # 当前命令是否应该执行
        
        i = 0
        while i < len(commands):
            cmd, operator = commands[i]
            
            # 检查是否需要执行管道命令序列
            if operator == '|':
                # 收集管道中的所有命令
                pipe_commands = [cmd]
                i += 1
                while i < len(commands) and commands[i][1] == '|':
                    pipe_commands.append(commands[i][0])
                    i += 1
                # 最后一个命令（没有管道操作符）
                if i < len(commands):
                    pipe_commands.append(commands[i][0])
                    i += 1
                
                # 执行管道命令
                if should_execute:
                    pipe_exit_code = self.execute_pipe_commands(pipe_commands)
                    last_exit_code = pipe_exit_code
                continue
            
            # 对于第一个命令之后的命令，检查是否应该执行
            if i > 0:
                # 前一个命令和当前命令之间的操作符
                prev_operator_after = commands[i-1][1]  # 前一个命令后面的操作符
                
                if prev_operator_after == '&&' and last_exit_code != 0:
                    should_execute = False
                elif prev_operator_after == '||' and last_exit_code == 0:
                    should_execute = False
                else:
                    should_execute = True
            
            if should_execute:
                # 调用父类的 onecmd 方法执行单个命令
                stop = super().onecmd(cmd)
                
                # 获取命令的退出码
                if hasattr(self, '_last_exit_code'):
                    last_exit_code = self._last_exit_code
                else:
                    last_exit_code = 0 if stop is None else 1
                
                # 如果命令要求停止，则立即返回
                if stop:
                    return True
            else:
                # 跳过不执行的命令
                i += 1
                continue
            
            i += 1
        
        return None  # onecmd 应该返回是否停止的标志

    def cmdloop(self, intro = None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                if readline.backend == "editline":
                    if self.completekey == 'tab':
                        # libedit uses "^I" instead of "tab"
                        command_string = "bind ^I rl_complete"
                    else:
                        command_string = f"bind {self.completekey} rl_complete"
                else:
                    command_string = f"{self.completekey}: complete"
                readline.parse_and_bind(command_string)
            except (ImportError, AttributeError):
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not stop:
                self.update_prompt()
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            line = input(self.prompt)
                        except EOFError:
                            line = 'EOF'
                        except KeyboardInterrupt:
                            self.stdout.write('\n')
                            line = ''
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = 'EOF'
                        else:
                            line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except (ImportError, KeyboardInterrupt):
                    pass

    def parse_command_line(self, line):
        """解析包含 &&、|| 和 | 操作符的命令行"""
        commands = []
        current_cmd = ""
        
        i = 0
        while i < len(line):
            # 检查是否遇到 && 操作符
            if i + 1 < len(line) and line[i] == '&' and line[i+1] == '&':
                if current_cmd.strip():
                    commands.append((current_cmd.strip(), '&&'))  # 当前命令后面是&&
                current_cmd = ""
                i += 2
            # 检查是否遇到 || 操作符
            elif i + 1 < len(line) and line[i] == '|' and line[i+1] == '|':
                if current_cmd.strip():
                    commands.append((current_cmd.strip(), '||'))  # 当前命令后面是||
                current_cmd = ""
                i += 2
            # 检查是否遇到管道操作符 |
            elif line[i] == '|':
                if current_cmd.strip():
                    commands.append((current_cmd.strip(), '|'))  # 当前命令后面是管道
                current_cmd = ""
                i += 1
            else:
                current_cmd += line[i]
                i += 1
        
        # 添加最后一个命令（后面没有操作符）
        if current_cmd.strip():
            commands.append((current_cmd.strip(), None))
        
        return commands

    def execute_pipe_commands(self, pipe_commands):
        """执行管道命令序列"""
        processes = []
        
        try:
            # 准备传递给子进程的环境变量（传递用户环境变量 + MockOS环境变量）
            env = os.environ.copy()
            env.update(self.mock_env.store())
            
            # 创建管道中的所有进程
            for i, cmd_line in enumerate(pipe_commands):
                try:
                    import shlex
                    parts = shlex.split(cmd_line)
                    command = parts[0]
                    cmd_args = parts[1:]
                except Exception:
                    print(f"Invalid command format: {cmd_line}")
                    return 1
                
                # 检查是否为内置命令
                if self.shell.is_builtin_command(command):
                    # 内置命令在管道中的处理
                    # 注意：大多数内置命令不适合在管道中使用，这里简化处理
                    print(f"bash: {command}: command not found")
                    return 127
                
                cmd_script = self.find_command_script(command)
                
                if not cmd_script or not os.path.exists(cmd_script):
                    print(f"bash: {command}: command not found")
                    return 127
                
                # 构建子进程命令：python 脚本路径 命令参数
                subprocess_cmd = [
                    sys.executable,  # 当前Python解释器路径
                    cmd_script
                ] + cmd_args
                
                # 设置 stdin 和 stdout
                stdin = sys.stdin if i == 0 else processes[i-1].stdout
                stdout = sys.stdout if i == len(pipe_commands) - 1 else subprocess.PIPE
                
                # 创建进程
                process = subprocess.Popen(
                    subprocess_cmd,
                    env=env,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=sys.stderr,
                    text=True,
                    encoding="utf-8"
                )
                processes.append(process)
                
                # 如果不是最后一个进程，关闭前一个进程的 stdout
                if i > 0:
                    processes[i-1].stdout.close()
            
            # 等待所有进程完成并收集退出码
            exit_codes = []
            for process in processes:
                process.wait()
                exit_codes.append(process.returncode)
            
            # 返回管道中最后一个命令的退出码
            return exit_codes[-1] if exit_codes else 0
            
        except KeyboardInterrupt:
            # 中断所有进程
            for process in processes:
                try:
                    process.terminate()
                except:
                    pass
            return 130  # 标准的 SIGINT 退出码
        except Exception as e:
            print(f"Pipe execution failed: {str(e)}")
            return 1

    def find_command_script(self, command):
        """查找命令脚本路径"""
        command_name = None
        
        # 处理绝对路径或相对路径的命令（如 /bin/ls 或 ./ls）
        if command.startswith("./"):
            # 相对路径：在当前工作目录下查找
            command_name = os.path.basename(command)
            # 获取当前工作目录的实际路径
            cwd_path = os.path.join(self.mock_env.BASE_PATH, self.mock_env.CWD.lstrip("/"))
            cmd_script = os.path.join(cwd_path, command_name)
        elif command.startswith("/"):
            # 绝对路径：在指定的绝对路径中查找
            # 将 MockOS 的绝对路径转换为实际文件系统路径
            abs_path = command.lstrip("/")
            cmd_script = os.path.join(self.mock_env.BASE_PATH, abs_path)
        else:
            # 普通命令：在 PATH 中的所有目录中查找
            command_name = command
            for path_dir in self.mock_env.PATH:
                # 将 PATH 目录转换为实际文件系统路径
                if path_dir.startswith("/"):
                    real_path = os.path.join(self.mock_env.BASE_PATH, path_dir.lstrip("/"))
                else:
                    real_path = path_dir
                cmd_script = os.path.join(real_path, command_name)
                if os.path.exists(cmd_script):
                    break
            else:
                # PATH 中所有目录都找不到
                cmd_script = None
        
        return cmd_script

    def default(self, line):
        """Handle commands by calling Python interpreter to execute script"""
        # 拆分命令行（支持带空格的参数，如ls "my folder"）
        try:
            import shlex
            parts = shlex.split(line)
            command = parts[0]
            cmd_args = parts[1:]
        except Exception:
            print(f"Invalid command format: {line}")
            return
        
        # 首先检查是否为内置命令
        if self.shell.is_builtin_command(command):
            self._last_exit_code = self.shell.execute_builtin_command(command, cmd_args)
            return
        
        cmd_script = self.find_command_script(command)
        
        if not cmd_script or not os.path.exists(cmd_script):
            print(f"bash: {command}: command not found")
            self._last_exit_code = 127  # 标准的"command not found"退出码
            return
        
        # 准备传递给子进程的环境变量（传递用户环境变量 + MockOS环境变量）
        env = os.environ.copy()
        env.update(self.mock_env.store())
        
        # 构建子进程命令：python 脚本路径 命令参数
        subprocess_cmd = [
            sys.executable,  # 当前Python解释器路径
            cmd_script
        ] + cmd_args
        
        try:
            # 执行命令，输出stdout/stderr
            result = subprocess.run(
                subprocess_cmd,
                env=env,
                stdout=sys.stdout,
                stderr=sys.stderr,
                # stdin=sys.stdin,
                text=True,
                encoding="utf-8"
            )
            # 设置退出码供操作符逻辑使用
            self._last_exit_code = result.returncode
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Failed to execute command {command}: {str(e)}")
            self._last_exit_code = 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MockOS - A simulated Linux operating system")
    parser.add_argument("-c", "--command", type=str, help="execute a single command")
    parser.add_argument("-e", "--execute", type=str, help="execute a single command (alias for -c)")
    
    args = parser.parse_args()
    
    if args.command:
        MockOS().onecmd(args.command)
    elif args.execute:
        MockOS().onecmd(args.execute)
    else:
        MockOS().cmdloop()

