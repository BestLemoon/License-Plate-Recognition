# -*- coding: utf-8 -*-
# @Time    : 2022/5/24 8:36
# @Author  : Lemoon
# @FileName: RandomSample.py
# @Software: PyCharm
# Description: Extract samples from CCPD dataset
import random
import numpy as np
import os
import shutil
import pandas as pd
in_dir = "D:\SourceCode\PyCharm\CCPD2020\out\merge_with_green\\"

out_train_dir = "./ccpd_sample_with_green/train/images\\"
out_test_dir = "./ccpd_sample_with_green/test/images\\"
out_val_dir = "./ccpd_sample_with_green/val/images\\"

if not os.path.exists(out_train_dir):
    os.makedirs(out_train_dir)
if not os.path.exists(out_test_dir):
    os.makedirs(out_test_dir)
if not os.path.exists(out_val_dir):
    os.makedirs(out_val_dir)

file_list = os.listdir(in_dir)
df = pd.DataFrame(file_list)
train, validate, test = np.split(df.sample(frac=1), [int(.6 * len(df)), int(.8 * len(df))])

# extract train samples

print("Copying samples to ./ccpd_base_sample/...")
for file_name in train[0]:
    shutil.copyfile(in_dir + file_name, out_train_dir + file_name)

# extract test samples

print("Copying samples to ./ccpd_base_sample/...")
for file_name in test[0]:
    shutil.copyfile(in_dir + file_name, out_test_dir + file_name)

# extract val samples

print("Copying samples to ./ccpd_base_sample/...")
for file_name in validate[0]:
    shutil.copyfile(in_dir + file_name, out_val_dir + file_name)
