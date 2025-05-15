#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：auto_nep
@File ：find_train.py
@Author ：RongYi
@Date ：2025/5/15 15:32
@E-mail ：2071914258@qq.com
"""
from ase.io import read, write
import numpy as np


def find_struc(train_xyz, dataset):
    """
    从数据集里面找 train.xyz
    :param train_xyz:
    :param dataset:
    :return:
    """
    shifted_xyz = read(train_xyz, format='extxyz', index=':')
    no_shifted_xyz = read(dataset, format='extxyz', index=':')

    len1 = len(shifted_xyz)
    len2 = len(no_shifted_xyz)
    print("shifted_xyz length:", len1)
    print("no_shifted_xyz length:", len2)

    # no_shifted_xyz -> shifted_xyz:
    # shifted_index (0, 439)

    # if no_shifted_xyz[no_shifted_index] = shifted_xyz[shifted_index] : ok
    # else no_shifted_index += 1

    # # test
    # test1 = np.around(shifted_xyz[1].get_positions(), 3)
    # test2 = np.around(no_shifted_xyz[2].get_positions(), 3)
    # print((test1 == test2).all())

    total_index = []
    for shifted_index in range(len1):
        # 初始化 pos1 pos2 no_shifted_index
        no_shifted_index = 0
        pos1 = np.around(shifted_xyz[shifted_index].get_positions(), 1)
        pos2 = np.around(no_shifted_xyz[no_shifted_index].get_positions(), 1)

        while True:
            if len(pos1) != len(pos2):
                no_shifted_index += 1
                pos2 = np.around(no_shifted_xyz[no_shifted_index].get_positions(), 1)
            else:
                # 位置一样 跳出循环
                if ((pos1 == pos2).all()):
                    # print(f"shifted_index: {shifted_index} -> no_shifted_index: {no_shifted_index}")
                    total_index.append(no_shifted_index)
                    break
                else:
                    no_shifted_index += 1
                    pos2 = np.around(no_shifted_xyz[no_shifted_index].get_positions(), 1)

    select_no_shifted_xyz = [no_shifted_xyz[index] for index in total_index]
    write('./find_no_shifted.xyz', select_no_shifted_xyz, format='extxyz')
    print("OK!Write find_no_shifted.xyz")


if __name__ == '__main__':
    find_struc_from_dataset("./train.xyz", "./v8-no-shifted.xyz")