import os
import shutil

for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        shutil.rmtree(pycache_path)
        print(f"已删除: {pycache_path}")
