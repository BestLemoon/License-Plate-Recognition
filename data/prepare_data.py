import os, cv2
import numpy as np

words_list = [
    "A", "B", "C", "D", "E",
    "F", "G", "H", "J", "K",
    "L", "M", "N", "P", "Q",
    "R", "S", "T", "U", "V",
    "W", "X", "Y", "Z", "0",
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9"]

con_list = [
    "皖", "沪", "津", "渝", "冀",
    "晋", "蒙", "辽", "吉", "黑",
    "苏", "浙", "京", "闽", "赣",
    "鲁", "豫", "鄂", "湘", "粤",
    "桂", "琼", "川", "贵", "云",
    "西", "陕", "甘", "青", "宁",
    "新"]

# 生成train
count = 0
data = open('train_data/train_list.txt', 'w', encoding='UTF-8')
for item in os.listdir('train/images'):
    path = 'train/images/'+item
    _, _, _, points, label, _, _ = item.split('-')
    print(path)

    points = points.split('_')  # 右下角开始顺时针排列
    points = [list(map(int, i.s1('&'))) for i in points]
    print(points)

    pts1 = np.float32(points)
    pts2 = np.float32([[400,200],[0,200],[0,0],[400,0]])

    img = cv2.imread(path)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    home_P = cv2.warpPerspective(img,M,(400,200))

    label = label.split('_')
    con = con_list[int(label[0])]
    words = [words_list[int(i)] for i in label[1:]]
    label = con + ''.join(words)
    print(label)

    # 保存旋转后的图片
    cv2.imwrite('train_data/train/%06d.jpg' % count, home_P)
    data.write('train/%06d.jpg\t%s\n' % (count, label))
    count += 1
data.close()

# 生成val
count = 0
data = open('train_data/val_list.txt', 'w', encoding='UTF-8')
for item in os.listdir('val/images'):
    path = 'val/images/'+item
    _, _, _, points, label, _, _ = item.split('-')
    print(path)

    points = points.split('_')  # 右下角开始顺时针排列
    points = [list(map(int, i.s1('&'))) for i in points]
    print(points)

    pts1 = np.float32(points)
    pts2 = np.float32([[400,200],[0,200],[0,0],[400,0]])

    img = cv2.imread(path)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    home_P = cv2.warpPerspective(img,M,(400,200))

    label = label.split('_')
    con = con_list[int(label[0])]
    words = [words_list[int(i)] for i in label[1:]]
    label = con + ''.join(words)
    print(label)

    # 保存旋转后的图片
    cv2.imwrite('train_data/val/%06d.jpg' % count, home_P)
    data.write('val/%06d.jpg\t%s\n' % (count, label))
    count += 1
data.close()

# 生成test
count = 0
for item in os.listdir('test/images'):
    path = 'test/images/'+item
    _, _, _, points, label, _, _ = item.split('-')
    print(path)

    points = points.split('_')  # 右下角开始顺时针排列
    points = [list(map(int, i.s1('&'))) for i in points]
    print(points)

    pts1 = np.float32(points)
    pts2 = np.float32([[400,200],[0,200],[0,0],[400,0]])

    img = cv2.imread(path)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    home_P = cv2.warpPerspective(img,M,(400,200))

    # 保存旋转后的图片
    cv2.imwrite('test_data/%06d.jpg' % count, home_P)
    count += 1

# 生成img文件夹，用作pyqt5界面默认的检测图片文件夹
# count = 0
# idx = 0
# s = ''
# for item in os.listdir('test/images'):
#     count += 1
#     if count <= 50:
#         continue
#     path = 'test/images/' + item
#     _, _, _, _, label, _, _ = item.split('-')
#     label = label.split('_')
#     con = con_list[int(label[0])]
#     words = [words_list[int(i)] for i in label[1:]]
#     label = con + ''.join(words)
#     s = s+label+'\n'
#     print(label)
#     img = cv2.imread(path)
#     cv2.imwrite('../yolov5/img/%06d.jpg' % idx, img)
#     idx += 1
#
#     if count == 100:
#         with open('../yolov5/answer.txt', 'w', encoding='utf-8') as f:
#             f.write(s)
#         break
