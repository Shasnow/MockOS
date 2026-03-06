import os
import sys
import argparse

def count_file_stats(file_path):
    """统计文件的行数、字数和字节数"""
    lines = 0
    words = 0
    bytes_count = 0
    chars = 0
    full_path = os.path.join(os.environ.get("MOCKOS_BASE_PATH", "mockos"), file_path.lstrip("/"))
    try:
        with open(full_path, 'rb') as f:
            content = f.read()
            bytes_count = len(content)
            
            # 尝试以文本模式读取以统计行数和字数
            try:
                with open(full_path, 'r', encoding='utf-8') as text_f:
                    text_content = text_f.read()
                    chars = len(text_content)
                    lines = text_content.count('\n')
                    # 如果文件不以换行符结尾，行数加1
                    if text_content and not text_content.endswith('\n'):
                        lines += 1
                    words = len(text_content.split())
            except UnicodeDecodeError:
                # 如果无法以UTF-8解码，尝试其他编码
                try:
                    with open(full_path, 'r', encoding='latin-1') as text_f:
                        text_content = text_f.read()
                        chars = len(text_content)
                        lines = text_content.count('\n')
                        if text_content and not text_content.endswith('\n'):
                            lines += 1
                        words = len(text_content.split())
                except:
                    # 如果仍然无法解码，只能统计字节数
                    lines = 0
                    words = 0
                    chars = 0
                    
    except FileNotFoundError:
        print(f"wc: {file_path}: No such file or directory", file=sys.stderr)
        return None
    except PermissionError:
        print(f"wc: {file_path}: Permission denied", file=sys.stderr)
        return None
    except IsADirectoryError:
        print(f"wc: {file_path}: Is a directory", file=sys.stderr)
        return None
    
    return lines, words, bytes_count, chars

def count_stdin_stats():
    """统计标准输入的行数、字数和字节数"""
    lines = 0
    words = 0
    bytes_count = 0
    chars = 0
    
    try:
        content = sys.stdin.read()
        chars = len(content)
        bytes_count = len(content.encode('utf-8'))
        lines = content.count('\n')
        if content and not content.endswith('\n'):
            lines += 1
        words = len(content.split())
    except KeyboardInterrupt:
        pass
    
    return lines, words, bytes_count, chars

def main():
    """Main function for wc command"""
    parser = argparse.ArgumentParser(description="Count lines, words, and bytes in files")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    parser.add_argument("-m", "--chars", action="store_true", help="print the character counts")
    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    parser.add_argument("files", nargs="*", help="input files")
    
    args = parser.parse_args()
    
    cwd = os.environ.get("MOCKOS_CWD", "/root")
    
    total_lines = 0
    total_words = 0
    total_bytes = 0
    total_chars = 0
    
    file_count = len(args.files)
    
    if file_count == 0:
        # 没有指定文件，从标准输入读取
        stats = count_stdin_stats()
        if stats:
            lines, words, bytes_count, chars = stats
            
            # 根据参数决定输出哪些统计信息
            output = []
            if args.lines or not any([args.bytes, args.chars, args.lines, args.words]):
                output.append(str(lines))
            if args.words or not any([args.bytes, args.chars, args.lines, args.words]):
                output.append(str(words))
            if args.bytes or not any([args.bytes, args.chars, args.lines, args.words]):
                output.append(str(bytes_count))
            if args.chars:
                output.append(str(chars))
            
            print(" ".join(output))
    else:
        # 处理指定的文件
        for file_path in args.files:
            # 解析文件路径
            if not file_path.startswith("/"):
                file_path = os.path.join(cwd, file_path)
            
            stats = count_file_stats(file_path)
            if stats:
                lines, words, bytes_count, chars = stats
                total_lines += lines
                total_words += words
                total_bytes += bytes_count
                total_chars += chars
                
                # 根据参数决定输出哪些统计信息
                output = []
                if args.lines or not any([args.bytes, args.chars, args.lines, args.words]):
                    output.append(str(lines))
                if args.words or not any([args.bytes, args.chars, args.lines, args.words]):
                    output.append(str(words))
                if args.bytes or not any([args.bytes, args.chars, args.lines, args.words]):
                    output.append(str(bytes_count))
                if args.chars:
                    output.append(str(chars))
                
                output.append(file_path)
                print(" ".join(output))
        
        # 如果处理了多个文件，输出总计
        if file_count > 1:
            output = []
            if args.lines or not any([args.bytes, args.chars, args.lines, args.words]):
                output.append(str(total_lines))
            if args.words or not any([args.bytes, args.chars, args.lines, args.words]):
                output.append(str(total_words))
            if args.bytes or not any([args.bytes, args.chars, args.lines, args.words]):
                output.append(str(total_bytes))
            if args.chars:
                output.append(str(total_chars))
            
            output.append("total")
            print(" ".join(output))
    
    exit(0)

if __name__ == "__main__":
    main()