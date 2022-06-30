# author: avenuewl
# 6.19 图片输出列表splist_points数量控制；寻找上下边界；异常检测与记录；
# 6.20 异常处理；243添加首尾端代码完善；314添加分割点问题完善；
# 6.24 完成与pyqt5界面的数据传送和交互功能
# 6.25 完善添加首尾端的判断条件；327添加分割点问题之条件添加；去除过近分割点的一处bug,使split_points其能够正常访问到尾部

# 识别的裁剪后的车牌图像大小为(400,200)
import cv2
import matplotlib.pyplot as plt


def two(img):
    ret, thresh_binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    ret, thresh_binary_inv = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh_trunc = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh_tozero = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh_tozero_inv = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)

    names = ['Oiriginal Image', 'BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO', 'THRESH_TOZERO_INV']
    images = img, thresh_binary, thresh_binary_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv

    for i in range(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(names[i])
        plt.xticks([]), plt.yticks([])
    plt.show()


def aotu_fit(img):
    ret, thresh_global = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # here 11 is the pixel neighbourhood that is used to calculate the threshold value
    thresh_mean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    thresh_gaussian = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    names = ['Original Image', 'Global Thresholding', 'Adaptive Mean Threshold', 'Adaptive Gaussian Thresholding']
    images = [img, thresh_global, thresh_mean, thresh_gaussian]

    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(names[i])
        plt.xticks([]), plt.yticks([])

    plt.show()


# s = os.listdir('./img')
# for name in s:
def cut_char(path):
    # imgname = os.path.basename(name).split('.')[0]
    # img = cv2.imread('./img/' + name, 0)
    # bin = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 111, 3)
    # r2, binary = cv2.threshold(bin, retval, 255, cv2.THRESH_BINARY)

    img = cv2.imread(path,0)
    retval, binary = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    (h, w) = binary.shape  # 返回高和宽
    binary = cv2.bitwise_not(binary)

    # print(imgname)

    # sum = 0
    # flag = 0  # 蓝绿牌标志，0为绿牌，1为蓝牌
    # for i in range(len(binary)):
    #     for j in range(len(binary[0])):
    #         sum += binary[i][j]
    # print(sum / (h * w))
    # if sum / (h * w) < 128:
    #     binary = cv2.bitwise_not(binary)  # 进行反色处理
    #     flag = 1


    # 水平投影，得到图像水平方向上的直方图
    hproject = binary.copy()
    b = [0 for x in range(0, h)]
    for j in range(0, h):
        for i in range(0, w):
            if hproject[j, i] == 0:  # 如果该点为黑点
                b[j] += 1  # 该列的计数器加1计数
                hproject[j, i] = 255  # 记录完后将其变为白色
    for j in range(0, h):  # 遍历每一行
        for i in range(0, b[j]):  # 从左至右，根据b[j]中的数量，将该像素点图成黑色
            hproject[j, i] = 0

    sum = 0
    for i in b:
        sum += i
    avr = sum / len(b) / 2
    h_start, h_end = 0, 0  # 记录水平方向的上下分界线
    s1 = []
    s2 = []
    for i in range(1, len(b) - 1):
        der1 = b[i] - b[i - 1]
        der2 = b[i + 1] - b[i]
        if der1 <= 0 and der2 > 0 and b[i] < avr:
            s1.append(i)
        elif der1 < 0 and der2 == 0 and b[i] < avr and i>len(b)//2:
            s2.append(i)

    print(s1,s2)
    if len(s1) <= 1:
        print('***********************************************************************')
        h_start = 30
        h_end = 160
        # split_points = [5, 50, 125, 175, 230, 285, 335, 395]
        # src = binary.copy()
        # re = []
        # for i in range(len(split_points) - 1):
        #     re.append(src[h_start:h_end, split_points[i]:split_points[i + 1]])
        # for i in range(len(re)):
        #     plt.subplot(1, len(re), i + 1), plt.imshow(re[i], 'gray')
        #     plt.xticks([]), plt.yticks([])
        # plt.show()
        #
        # for i in range(len(re)):
        #     re[i] = cv2.resize(re[i], (32, 40))
        #     re[i] = cv2.bitwise_not(re[i])
        #     cv2.imwrite('../reg/cut_result/' + str(i) + '.jpg', re[i])
        # # with open('exp.txt',mode='a',encoding='utf_8') as f:
        # #     f.write(imgname+'\n')
        ## continue
        # return

    # 图像上下边界
    if s1[-1] > len(b) // 2:  # 图像右部存在波谷
        if len(s2) != 0:
            for i in range(len(s1)):
                if s1[i] >= len(b) / 2:  # 最靠近中值的左方波谷和右方波谷即为上下边界线
                    h_start = s1[i - 1]
                    h_end = s1[i]
                    break
            if h_end > s2[0]:
                h_end = s2[0]
        else:
            for i in range(len(s1)):
                if s1[i] >= len(b) / 2:  # 最靠近中值的左方波谷和右方波谷即为上下边界线
                    h_start = s1[i - 1]
                    h_end = s1[i]
                    break
    else:  # 图像右部不存在波谷
        max = 0
        for i in range(len(b) // 2, len(b) - 1):  # 从中值点开始，找到变化最大的像素强度位置，该位置则为图像下边界
            di = b[i] - b[i + 1]
            if di > max:
                max = di
                h_end = i + 1
        h_start = s1[-1]  # 最靠近中值的左方波谷为图像上边界
    print(h_start, h_end)


    cp = binary.copy()  # 绘制去除上下边界后的水平方向上的直方图
    c = [0 for x in range(0, h)]
    for j in range(0, h_start):
        for i in range(0, w):
            cp[j, i] = 255
    for j in range(h_start, h_end):
        for i in range(0, w):
            if cp[j, i] == 0:
                c[j] += 1
                cp[j, i] = 255
    for j in range(h_end, h):
        for i in range(0, w):
            cp[j, i] = 255
    for j in range(0, h):
        for i in range(0, c[j]):
            cp[j, i] = 0

    # 垂直投影，得到图像竖直方向上的直方图
    vproject = binary.copy()
    a = [0 for x in range(0, w)]
    # 记录每一列的波峰
    for j in range(0, w):  # 遍历每一列
        # 遍历每一行
        for i in range(0, h_start):
            vproject[i, j] = 255  # 将不属于范围内的点变为白色
        for i in range(h_start, h_end):
            if vproject[i, j] == 0:  # 如果该点为黑点
                a[j] += 1  # 该列的计数器加1计数
                vproject[i, j] = 255  # 记录完后将其变为白色
        for i in range(h_end, h):
            vproject[i, j] = 255  # 将不属于范围内的点变为白色
    for j in range(0, w):  # 遍历每一列
        for i in range((h - a[j]), h):  # 从该列应该变黑的最顶部的点开始向最底部涂黑
            vproject[i, j] = 0  # 涂黑

    # images = [img, binary, hproject, cp, vproject]  # 显示相关图像信息
    # for i in range(5):
    #     plt.subplot(3, 2, i + 1), plt.imshow(images[i], 'gray')
    #     plt.xticks([]), plt.yticks([])
    # plt.show()

    split_points = []
    i = 0
    while i < len(a) - 1:  # 找到水平方向上的符合分割条件的波谷的坐标信息
        if a[i] < 10:
            times = 1
            i = i + 1
            while a[i] < 10:
                times += 1
                i = i + 1
                if i >= len(a):
                    break
            split_points.append(i - times // 2 - 1)
        else:
            i = i + 1

    # # 去除车牌中心点
    # for i in range(len(split_points)-1):
    #     if split_points[i] > 100 and split_points[i]<130:
    #         if split_points[i+1] - split_points[i]<25:
    #             split_points.pop(i)
    #             break

    print(split_points)
    if len(split_points) == 0:
        print('***********************************************************************')
        split_points = [5, 50, 125, 175, 230, 285, 335, 395]
        src = binary.copy()
        re = []
        for i in range(len(split_points) - 1):
            re.append(src[h_start:h_end, split_points[i]:split_points[i + 1]])
        for i in range(len(re)):
            plt.subplot(1, len(re), i + 1), plt.imshow(re[i], 'gray')
            plt.xticks([]), plt.yticks([])
        plt.show()
        # with open('exp.txt',mode='a',encoding='utf_8') as f:
        #     f.write(imgname+'\n')
        # continue
        for i in range(len(re)):
            re[i] = cv2.resize(re[i], (32, 40))
            re[i] = cv2.bitwise_not(re[i])
            cv2.imwrite('../reg/cut_result/' + str(i) + '.jpg', re[i])

        return
    # 添加首尾端
    if split_points[0] > 10:
        split_points.insert(0, 5)

    te = split_points[-1]
    while 395 - te > 35:
        end = 395
        min = a[te+10]
        for i in range(te+11, 396):
            if a[i] < min:
                min = a[i]
                end = i
        if end-split_points[-1] < 35:
            te = end
            continue
        split_points.append(end)

    if split_points[-1] < 360:
        split_points.append(395)
    else:
        end = split_points[-1]
        if 400 - split_points[-2] > 15:
            min = a[split_points[-2]+11]
            for i in range(split_points[-2] + 11, split_points[-1]):
                if a[i] < min:
                    min = a[i]
                    end = i
            if end - split_points[-2] > 35:
                split_points.pop(-1)
                split_points.append(end)

    print(split_points)

    # 去除相聚过近的分割点
    while True:
        f = 0
        for i in range(0, len(split_points) - 1):
            diff = split_points[i + 1] - split_points[i]
            if diff < 35:
                split_points.pop(i)
                f = 1
                break
        if f == 0:
            break

    if split_points[0] - 5 > 35:
        split_points.insert(0, 5)

    print(split_points)


    # if flag == 0:  # 绿牌
    #     while len(split_points) != 9:
    #         if len(split_points) > 9:
    #             split_points.pop(-1)
    #         elif len(split_points) < 9:
    #             for i in range(0, len(split_points) - 1):
    #                 a = split_points[i + 1] - split_points[i]
    #                 if a > 85:
    #                     split_points.insert(i + 1, split_points[i] + a // 2)
    #                     break

    while len(split_points) != 8:
        # 去除汉字间间隔影响
        excp = 1
        if len(split_points) > 8:
            split_points.pop(-1)
        elif len(split_points) < 8:  # 添加分割点，将连在一起的符号分割开来
            excp = 0
            for i in range(0, len(split_points) - 1):
                diff = split_points[i+1] - split_points[i]
                if diff > 80:
                    excp = 1
                    cut = split_points[i] + diff // 2
                    min = a[split_points[i]+5]
                    for j in range(split_points[i]+6,split_points[i+1]-5):
                        if a[j] < min:
                            min = a[j]
                            cut = j
                    if split_points[i+1] - cut < 35 or cut - split_points[i] < 35:
                        cut = split_points[i] + diff // 2
                    split_points.insert(i+1,cut)
                    break
        if excp == 0:
            break

    if len(split_points) != 8:
        print("*******************************************************")
        split_points = [5, 50, 125, 175, 230, 280, 330, 395]
        src = binary.copy()
        re = []
        for i in range(len(split_points) - 1):
            re.append(src[h_start:h_end, split_points[i]:split_points[i + 1]])
        for i in range(len(re)):
            plt.subplot(1, len(re), i + 1), plt.imshow(re[i], 'gray')
            plt.xticks([]), plt.yticks([])
        plt.show()

        for i in range(len(re)):
            re[i] = cv2.resize(re[i], (32, 40))
            re[i] = cv2.bitwise_not(re[i])
            cv2.imwrite('../reg/cut_result/' + str(i) + '.jpg', re[i])

        # with open('exp.txt',mode='a',encoding='utf_8') as f:
        #     f.write(imgname+'\n')
        # continue
        return

    print(split_points)

    src = binary.copy()
    re = []
    for i in range(len(split_points) - 1):
        re.append(src[h_start:h_end, split_points[i]:split_points[i + 1]])

    # for i in range(len(re)):
    #     plt.subplot(1, len(re), i + 1), plt.imshow(re[i], 'gray')
    #     plt.xticks([]), plt.yticks([])
    # plt.show()

    for i in range(len(re)):
        re[i] = cv2.resize(re[i],(32,40))
        re[i] = cv2.bitwise_not(re[i])
        cv2.imwrite('../reg/cut_result/'+str(i)+'.jpg', re[i])
    # break

# cut_char('../yolov5/result/result.jpg')
# cut_char('../reg/PaddleOCR/test_data/000009.jpg')