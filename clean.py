import os
import shutil

def should_skip_directory(path):
    """检查是否应该跳过某个目录"""
    skip_dirs = {'.venv', '.mypy_cache', '.git'}
    return any(skip_dir in path for skip_dir in skip_dirs)

for root, dirs, files in os.walk('.'):
    # 先处理 __pycache__ 目录
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        shutil.rmtree(pycache_path)
        print(f"已删除: {pycache_path}")
        dirs.remove('__pycache__')  # 从列表中移除，避免遍历其子目录
    
    # 排除不需要遍历的目录
    dirs[:] = [d for d in dirs if not should_skip_directory(os.path.join(root, d))]
