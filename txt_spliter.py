# 将text文件分割成n个文件

import os
import sys
import math

def split_file(file_path, n):
    # 读取文件内容
    with open(file_path
                , 'r', encoding='utf-8') as f:
            content = f.read()
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(file_path)
    # 计算每个文件的大小
    file_size = len(content)
    part_size = math.ceil(file_size / n)
    # 分割文件
    for i in range(n):
        start = i * part_size
        end = (i + 1) * part_size
        file_part_path = f'{file_name}_{i+1}{file_extension}'
        with open(file_part_path, 'w', encoding='utf-8') as f:
            f.write(content[start:end])
        print(f'文件 {file_part_path} 创建成功')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python txt_spliter.py file_path n')
        sys.exit(1)
    file_path = sys.argv[1]
    n = int(sys.argv[2])
    split_file(file_path, n)
    print('文件分割完成')
