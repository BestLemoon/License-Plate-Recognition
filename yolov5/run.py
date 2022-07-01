
# 6.24 pyqt5界面设计和编码；完成与车牌分割、车牌识别部分(PaddleOCR)的交互；完成上一张，下一张和集中测试功能；
# 6.25 完成车牌检测(yolov5)的功能实现；车牌分割问题的bug修改；

import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from lsreg import Ui_Form
from reg.cut import cut_char
from tools.infer.predict_rec import recognition
from yolov5.detect_one_with_wrap import detect_with_wrap


class MyMainForm(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.count = 0  # 当前浏览图片的下标
        self.path = ''  # 查找图片路径
        self.FileButton.clicked.connect(lambda : self.choose_photo())
        self.front.clicked.connect(lambda : self.up())
        self.next.clicked.connect(lambda: self.down())
        self.pushButton.clicked.connect(lambda : self.con_test())

    def play(self):
        self.src_ph.setToolTip("%s" % self.path.split('/')[-1])
        self.src_ph.setStyleSheet("QPushButton{border-image: url(%s)}" % self.path)
### 此处放框好的图片img1
        points = detect_with_wrap(self.path, 'result/result.jpg', 'result/result_warp.jpg')
        self.check_button.setStyleSheet("QPushButton{border-image: url(%s)}" % 'result/result_warp.jpg')

### 此处放框好的图片在原图中的坐标
        self.label_11.setText("({},{})".format(int(points[0][0]),int(points[0][1])))
        self.label_12.setText("({},{})".format(int(points[1][0]),int(points[1][1])))
        self.label_13.setText("({},{})".format(int(points[2][0]),int(points[2][1])))
        self.label_14.setText("({},{})".format(int(points[3][0]),int(points[3][1])))

### 此处放分割好的图片check_img
        check_img = 'result/result.jpg' #修改分割后的图片地址
        self.get_ls.setStyleSheet("QPushButton{border-image: url(%s)}" % check_img)

        cut_char(check_img)
        self.pushButton_1.setStyleSheet("QPushButton{border-image: url(%s)}" % ('../reg/cut_result/' + '0.jpg'))
        self.pushButton_2.setStyleSheet("QPushButton{border-image: url(%s)}" % ('../reg/cut_result/' + '1.jpg'))
        self.pushButton_3.setStyleSheet("QPushButton{border-image: url(%s)}" % ('../reg/cut_result/' + '2.jpg'))
        self.pushButton_4.setStyleSheet("QPushButton{border-image: url(%s)}" % ('../reg/cut_result/' + '3.jpg'))
        self.pushButton_5.setStyleSheet("QPushButton{border-image: url(%s)}" % ('../reg/cut_result/' + '4.jpg'))
        self.pushButton_6.setStyleSheet("QPushButton{border-image: url(%s)}" % ('../reg/cut_result/' + '5.jpg'))
        self.pushButton_7.setStyleSheet("QPushButton{border-image: url(%s)}" % ('../reg/cut_result/' + '6.jpg'))

        result = recognition(check_img)
        s = 'wrong'
        if len(result) > 0:
            s = result[0]
        self.result.setText(s)
        QApplication.processEvents()
        return result[0]
        # time.sleep(2)

    def choose_photo(self):
        cwd = os.getcwd() + os.sep + 'img'  # 获取当前程序文件位置
        # recognition()
        path, filetype = QFileDialog.getOpenFileName(self, "选取照片", cwd, "All Files(*.*)")
        # file_name = QFileDialog.getOpenFileName(self, "Open File", "cwd", "jpg (*.jpg)")
        print(path)
        if path == "":
            return
        else:
            self.src_ph.setToolTip("%s" % path.split('/')[-1])
            self.path = 'img/' + path.split('/')[-1]
            self.count = int((path.split('/')[-1]).split('.')[0])
            print(self.count)
            print(self.path)
            self.play()



    def up(self):
        if self.count > 0:
            self.count -= 1
            # self.front.setToolTip('上一张')
            print('count:', self.count)
            self.path = ''
            self.path = "000000"+str(self.count)
            self.path = self.path[-6:]
            self.path = 'img/' + self.path + '.jpg'
            print('path:', self.path)
            self.play()

        else:
            self.pushButton_1.setToolTip("已经是第一张图片")
            QMessageBox.information(self,
                "提示",
                "已是第一张图片",
                QMessageBox.Yes | QMessageBox.No)
        # print(self.count)

    def down(self):
        # print('len:',len(os.listdir('img')))
        if self.count < len(os.listdir('img'))-1:
            self.count += 1
            # self.pushButton_2.setToolTip("下一页")
            print('count:', self.count)
            self.path = ''
            self.path = "000000" + str(self.count)
            self.path = self.path[-6:]
            self.path = 'img/' + self.path + '.jpg'
            print('path:', self.path)
            self.play()

        else:
            self.pushButton_2.setToolTip("已是最后一张图片")
            QMessageBox.information(self,
                "提示",
                "已是最后一张图片",
                QMessageBox.Yes | QMessageBox.No)
        # print(self.count)

    def con_test(self):
        list = os.listdir('img')
        reg_re = []
        ans = []
        for i in list:
            self.path = 'img/'+i
            # print(self.path)
            result = self.play()
            reg_re.append(result)
        with open('answer.txt','r',encoding='utf-8') as f:
            a = f.readlines()
        for i in a:
            ans.append(i.split()[0])
        # print(len(ans),ans)
        # print(len(reg_re),reg_re)
        ls = 0
        for i in range(len(ans)):
            simi = 0
            if len(ans[i]) == len(reg_re[i]):
                for j in range(len(ans[i])):
                    if ans[i][j] != reg_re[i][j]:
                        simi = 1
                        print('match_fail:', i)
                        break
            else:
                simi = 1
            if simi == 1:
                ls += 1
        acc = (len(ans)-ls)/(len(ans))
        QMessageBox.information(self, "准确度", "acc：%f" % acc)
        print(acc)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())