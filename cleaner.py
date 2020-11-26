# /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import hashlib


def count_file():
    file_num = 0
    for _, __, files in os.walk(os.getcwd()):
        file_num += len(files)
    return file_num


def count_printer(func):
    def wrapper():
        origin_file = count_file()
        print("执行函数：{0} 清洗前有: {1} 个文件".format(func.__name__, origin_file))
        print('清洗中...')
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        new_amount = count_file()
        print('清洗后剩余：{} 个文件'.format(new_amount))
        print('移除了 {} 个文件, 耗时：{} s\n'.format(origin_file - new_amount, end - start))

    return wrapper


def get_md5(filename):
    md5 = hashlib.md5()
    try:
        f = open(filename, 'rb')
    except FileNotFoundError:
        print("Error: 没有找到文件或读取文件失败")
        return False
    else:
        while True:
            fb = f.read(8096)
            if not fb:
                break
            md5.update(fb)
        f.close()
        return md5.hexdigest()


@count_printer
def del_md5_duplicates():
    md5_dict = {}
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            full_path_file = os.path.join(root, file)
            md5_value = get_md5(full_path_file)
            if not md5_value:
                pass
            elif md5_value in md5_dict.values():
                os.remove(full_path_file)
            else:
                md5_dict[full_path_file] = md5_value


@count_printer
def del_size_0_files():
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            try:
                file_full_path = os.path.join(root, file)
                if os.path.getsize(file_full_path) < 500:  # 500 单位为字节
                    os.remove(file_full_path)
            except FileNotFoundError:
                print("Error: 删除文件失败")


@count_printer
def del_non_jpg_files():
    black_list = {'jpeg', 'png', 'gif', 'bmp'}
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            _, suffix = file.rsplit('.')
            if suffix in black_list:
                try:
                    os.remove(os.path.join(root, file))
                except FileNotFoundError:
                    print("Error: 删除文件失败")


if __name__ == '__main__':
    if sys.argv[1] == 'count':
        print("\n共有：{1} 个文件 \n执行文件夹: {0}\n".format(os.getcwd(), count_file()))
    # del_non_jpg_files()
    # del_size_0_files()
    # del_md5_duplicates()
