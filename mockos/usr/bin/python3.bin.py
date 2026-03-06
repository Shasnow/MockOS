import os
import sys


def main():
    try:
        os.system(f"{sys.executable} {sys.argv[1] if len(sys.argv) > 1 else ''}")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()