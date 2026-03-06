import os
import sys
import argparse

def main():
    """Echo arguments to standard output."""
    parser = argparse.ArgumentParser(description="Echo arguments to standard output")
    parser.add_argument("text", nargs="*", help="text to echo")
    parser.add_argument("-n", action="store_true", help="do not output the trailing newline")
    
    args = parser.parse_args()
    
    try:
        output = " ".join(args.text)
        
        if args.n:
            print(output, end="")
        else:
            print(output)
        
        exit(0)  # 成功
    except Exception as e:
        print(f"echo: {str(e)}", file=sys.stderr)
        exit(1)  # 错误

if __name__ == "__main__":
    main()