# -*- coding: utf-8 -*-
# @Time    : 2022/5/24 8:31
# @Author  : Lemoon
# @FileName: CCPD2YoLo.py
# @Software: PyCharm

import cv2
import os


def getBiggerRec(names):
    b = names.split("-")[3].split("_")
    rb_x = int(b[0].split("&")[0])
    rb_y = int(b[0].split("&")[1])

    lb_x = int(b[1].split("&")[0])
    lb_y = int(b[1].split("&")[1])

    lu_x = int(b[2].split("&")[0])
    lu_y = int(b[2].split("&")[1])

    ru_x = int(b[3].split("&")[0])
    ru_y = int(b[3].split("&")[1])

    # 选最靠外的点
    return min(rb_x, lb_x, lu_x, ru_x), min(rb_y, lb_y, lu_y, ru_y), max(rb_x, lb_x, lu_x, ru_x), max(rb_y, lb_y, lu_y,
                                                                                                      ru_y)


if __name__ == '__main__':
    folder_list = ["train", "test", "val"]
    for name in folder_list:
        input_dir = "ccpd_sample_with_green/" + name + "/images/"
        output_dir = "ccpd_sample_with_green/" + name + "/labels/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        name_list = os.listdir(input_dir)
        for n in name_list:
            img = cv2.imread(input_dir + n)
            sp = img.shape
            height = sp[0]
            width = sp[1]

            lu_1 = getBiggerRec(n)[0]
            lu_2 = getBiggerRec(n)[1]
            rb_1 = getBiggerRec(n)[2]
            rb_2 = getBiggerRec(n)[3]
            # class center_x center_y width height
            # 0 中心点（归一化宽） 中心点（归一化长） 框宽度（归一化） 框长度（归一化）
            mid_x = (rb_1 + lu_1) / 2 / width
            mid_y = (rb_2 + lu_2) / 2 / height
            dis_x = (rb_1 - lu_1) / width
            dic_y = (rb_2 - lu_2) / height

            res = "0 " + str(mid_x) + " " + str(mid_y) + " " + str(dis_x) + " " + str(dic_y)
            print(res)

            f = open(output_dir + n.split(".")[0] + ".txt", 'a')
            f.write(res)
            f.close()
    # Generate data.yaml
    with open("ccpd_sample_with_green/data.yaml", 'w') as f:
        f.write("train: ccpd_sample_with_green/train/images\n")
        f.write("val: ccpd_sample_with_green/val/images\n")
        f.write("nc: 1\n")
        f.write("names: ['0']\n")
