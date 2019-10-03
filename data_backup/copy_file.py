# -*- coding: utf-8 -*-

import os
import time

import shutil

import tools

"""
将文件或文件夹复制到指定目录并解压
"""


def copy_file(srcfile, filename):
    tools.print_a('开始进行文件复制')
    if not os.path.isfile(srcfile):
        last_name = os.path.basename(srcfile)
        destination_name = filename + "\\" + last_name
        shutil.copytree(srcfile, destination_name)
        print('\033[0;37;0m[INFO] {} -> {}\033[0m'.format(str(srcfile), str(destination_name)))
    else:
        shutil.copy2(srcfile, filename)
        print('\033[0;37;0m[INFO] {} -> {}\033[0m'.format(str(srcfile), str(filename)))
    tools.print_d('文件复制成功')


def copy_and_zip(file_list, dst_folder_name, zip_and_del, folder_add_now):
    """
    批量复制文件到指定文件夹，然后把指定文件夹的内容压缩成ZIP并且删掉该文件夹
    :param folder_add_now:
    :param zip_and_del:
    :param file_list: 文件或文件夹
    :param dst_folder_name: 目标压缩文件的名称
    :return:
    """

    if folder_add_now == 1:
        now = time.strftime("%Y%m%d_%H%M%S")
        dst_folder_name = dst_folder_name + now

    if not os.path.exists(dst_folder_name):
        os.makedirs(dst_folder_name)  # 创建路径

    # for item in file_list:
    copy_file(file_list, dst_folder_name)

    if zip_and_del == 1:
        tools.print_a('开始进行文件压缩')
        shutil.make_archive(dst_folder_name, "zip", dst_folder_name, )
        print('\033[0;37;0m[INFO] {} -> {}.zip\033[0m'.format(str(dst_folder_name), str(dst_folder_name)))
        tools.print_d('文件压缩成功')
        # 删除原有的文件夹
        shutil.rmtree(dst_folder_name)
    return dst_folder_name + ".zip"