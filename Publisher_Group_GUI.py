#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 23:31
# @Author  : WuYan
# @FileName: Publisher_Group_GUI.py
# @Software: PyCharm
# @EMail   : wuyansec@qq.com


import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
import os
import GeoServer_Publisher
import ast,requests
import re

# 其中有些投影坐标系有偏移，不能直接使用，需要加偏后使用？
PROJECT = ["3857 WGS84/Pseudo-Mercator","4508 CGCS2000_GK_CM_111E ","2327 Xian_1980_GK_Zone_13 ","2328 Xian_1980_GK_Zone_14","2329 Xian_1980_GK_Zone_15 ","2330 Xian_1980_GK_Zone_16 ","2331 Xian_1980_GK_Zone_17 ","2332 Xian_1980_GK_Zone_18 ","2333 Xian_1980_GK_Zone_19 ","2334 Xian_1980_GK_Zone_20 ","2335 Xian_1980_GK_Zone_21 ","2336 Xian_1980_GK_Zone_22","2337 Xian_1980_GK_Zone_23 ","2338 Xian_1980_GK_CM_75E ","2339 Xian_1980_GK_CM_81E ","2340 Xian_1980_GK_CM_87E ","2341 Xian_1980_GK_CM_93E ","2342 Xian_1980_GK_CM_99E ","2343 Xian_1980_GK_CM_105E ","2344 Xian_1980_GK_CM_111E","2345 Xian_1980_GK_CM_117E ","2346 Xian_1980_GK_CM_123E ","2347 Xian_1980_GK_CM_129E ","2348 Xian_1980_GK_CM_135E ","2349 Xian_1980_3_Degree_GK_Zone_25 ","2350 Xian_1980_3_Degree_GK_Zone_26 ","2351 Xian_1980_3_Degree_GK_Zone_27 ","2352 Xian_1980_3_Degree_GK_Zone_28 ","2353 Xian_1980_3_Degree_GK_Zone_29 ","2354 Xian_1980_3_Degree_GK_Zone_30 ","2355 Xian_1980_3_Degree_GK_Zone_31 ","2356 Xian_1980_3_Degree_GK_Zone_32 ","2357 Xian_1980_3_Degree_GK_Zone_33 ","2358 Xian_1980_3_Degree_GK_Zone_34","2359 Xian_1980_3_Degree_GK_Zone_35 ","2360 Xian_1980_3_Degree_GK_Zone_36 ","2361 Xian_1980_3_Degree_GK_Zone_37 ","2362 Xian_1980_3_Degree_GK_Zone_38 ","2363 Xian_1980_3_Degree_GK_Zone_39 ","2364 Xian_1980_3_Degree_GK_Zone_40","2365 Xian_1980_3_Degree_GK_Zone_41 ","2366 Xian_1980_3_Degree_GK_Zone_42 ","2367 Xian_1980_3_Degree_GK_Zone_43 ","2368 Xian_1980_3_Degree_GK_Zone_44 ","2369 Xian_1980_3_Degree_GK_Zone_45 ","2370 Xian_1980_3_Degree_GK_CM_75E","2371 Xian_1980_3_Degree_GK_CM_78E ","2372 Xian_1980_3_Degree_GK_CM_81E ","2373 Xian_1980_3_Degree_GK_CM_84E ","2374 Xian_1980_3_Degree_GK_CM_87E ","2375 Xian_1980_3_Degree_GK_CM_90E ","2376 Xian_1980_3_Degree_GK_CM_93E ","2377Xian_1980_3_Degree_GK_CM_96E ","2378 Xian_1980_3_Degree_GK_CM_99E ","2379 Xian_1980_3_Degree_GK_CM_102E ","2380 Xian_1980_3_Degree_GK_CM_105E ","2381 Xian_1980_3_Degree_GK_CM_108E ","2382 Xian_1980_3_Degree_GK_CM_111E ","2383 Xian_1980_3_Degree_GK_CM_114E","2384 Xian_1980_3_Degree_GK_CM_117E ","2385 Xian_1980_3_Degree_GK_CM_120E ","2386 Xian_1980_3_Degree_GK_CM_123E ","2387 Xian_1980_3_Degree_GK_CM_126E ","2388 Xian_1980_3_Degree_GK_CM_129E ","2389 Xian_1980_3_Degree_GK_CM_132E","2390 Xian_1980_3_Degree_GK_CM_135E ","2401 Beijing_1954_3_Degree_GK_Zone_25 ","2402 Beijing_1954_3_Degree_GK_Zone_26 ","2403 Beijing_1954_3_Degree_GK_Zone_27 ","2404 Beijing_1954_3_Degree_GK_Zone_28 ","2405 Beijing_1954_3_Degree_GK_Zone_29","2406 Beijing_1954_3_Degree_GK_Zone_30 ","2407 Beijing_1954_3_Degree_GK_Zone_31 ","2408 Beijing_1954_3_Degree_GK_Zone_32 ","2409 Beijing_1954_3_Degree_GK_Zone_33 ","2410 Beijing_1954_3_Degree_GK_Zone_34 ","2411 Beijing_1954_3_Degree_GK_Zone_35","2412 Beijing_1954_3_Degree_GK_Zone_36 ","2413 Beijing_1954_3_Degree_GK_Zone_37 ","2414 Beijing_1954_3_Degree_GK_Zone_38 ","2415 Beijing_1954_3_Degree_GK_Zone_39 ","2416 Beijing_1954_3_Degree_GK_Zone_40 ","2417 Beijing_1954_3_Degree_GK_Zone_41","2418 Beijing_1954_3_Degree_GK_Zone_42 ","2419 Beijing_1954_3_Degree_GK_Zone_43 ","2420 Beijing_1954_3_Degree_GK_Zone_44 ","2421 Beijing_1954_3_Degree_GK_Zone_45 ","2422 Beijing_1954_3_Degree_GK_CM_75E ","2423 Beijing_1954_3_Degree_GK_CM_78E ","2424 Beijing_1954_3_Degree_GK_CM_81E ","2425 Beijing_1954_3_Degree_GK_CM_84E ","2426 Beijing_1954_3_Degree_GK_CM_87E ","2427 Beijing_1954_3_Degree_GK_CM_90E ","2428 Beijing_1954_3_Degree_GK_CM_93E ","2429 Beijing_1954_3_Degree_GK_CM_96E ","2430 Beijing_1954_3_Degree_GK_CM_99E ","2431 Beijing_1954_3_Degree_GK_CM_102E ","2432 Beijing_1954_3_Degree_GK_CM_105E ","2433 Beijing_1954_3_Degree_GK_CM_108E ","2434 Beijing_1954_3_Degree_GK_CM_111E","2435 Beijing_1954_3_Degree_GK_CM_114E ","2436 Beijing_1954_3_Degree_GK_CM_117E ","2437 Beijing_1954_3_Degree_GK_CM_120E ","2438 Beijing_1954_3_Degree_GK_CM_123E ","2439 Beijing_1954_3_Degree_GK_CM_126E ","2440 Beijing_1954_3_Degree_GK_CM_129E","2441 Beijing_1954_3_Degree_GK_CM_132E ","2442 Beijing_1954_3_Degree_GK_CM_135E ","3395 WGS_1984_World_Mercator ","4491 CGCS2000_GK_Zone_13 ","4492 CGCS2000_GK_Zone_14 ","4493 CGCS2000_GK_Zone_15 ","4494 CGCS2000_GK_Zone_16","4495 CGCS2000_GK_Zone_17 ","4496 CGCS2000_GK_Zone_18 ","4497 CGCS2000_GK_Zone_19 ","4498 CGCS2000_GK_Zone_20 ","4499 CGCS2000_GK_Zone_21 ","4500 CGCS2000_GK_Zone_22 ","4501 CGCS2000_GK_Zone_23 ","4502 CGCS2000_GK_CM_75E ","4503 CGCS2000_GK_CM_81E ","4504 CGCS2000_GK_CM_87E ","4505 CGCS2000_GK_CM_93E ","4506 CGCS2000_GK_CM_99E ","4507 CGCS2000_GK_CM_105E ","4509 CGCS2000_GK_CM_117E ","4510 CGCS2000_GK_CM_123E ","4511 CGCS2000_GK_CM_129E","4512 CGCS2000_GK_CM_135E ","4513 CGCS2000_3_Degree_GK_Zone_25 ","4514 CGCS2000_3_Degree_GK_Zone_26 ","4515 CGCS2000_3_Degree_GK_Zone_27 ","4516 CGCS2000_3_Degree_GK_Zone_28 ","4517 CGCS2000_3_Degree_GK_Zone_29 ","4518 CGCS2000_3_Degree_GK_Zone_30 ","4519 CGCS2000_3_Degree_GK_Zone_31 ","4520 CGCS2000_3_Degree_GK_Zone_32 ","4521 CGCS2000_3_Degree_GK_Zone_33 ","4522 CGCS2000_3_Degree_GK_Zone_34 ","4523 CGCS2000_3_Degree_GK_Zone_35 ","4524 CGCS2000_3_Degree_GK_Zone_36","4525 CGCS2000_3_Degree_GK_Zone_37 ","4526 CGCS2000_3_Degree_GK_Zone_38 ","4527 CGCS2000_3_Degree_GK_Zone_39 ","4528 CGCS2000_3_Degree_GK_Zone_40 ","4529 CGCS2000_3_Degree_GK_Zone_41 ","4530 CGCS2000_3_Degree_GK_Zone_42 ","4531 CGCS2000_3_Degree_GK_Zone_43 ","4532 CGCS2000_3_Degree_GK_Zone_44 ","4533 CGCS2000_3_Degree_GK_Zone_45 ","4534 CGCS2000_3_Degree_GK_CM_75E ","4535 CGCS2000_3_Degree_GK_CM_78E ","4536 CGCS2000_3_Degree_GK_CM_81E ","4537 CGCS2000_3_Degree_GK_CM_84E","4538 CGCS2000_3_Degree_GK_CM_87E ","4539 CGCS2000_3_Degree_GK_CM_90E ","4540 CGCS2000_3_Degree_GK_CM_93E ","4541 CGCS2000_3_Degree_GK_CM_96E ","4542 CGCS2000_3_Degree_GK_CM_99E ","4543 CGCS2000_3_Degree_GK_CM_102E ","4544 CGCS2000_3_Degree_GK_CM_105E ","4545 CGCS2000_3_Degree_GK_CM_108E ","4546 CGCS2000_3_Degree_GK_CM_111E ","4547 CGCS2000_3_Degree_GK_CM_114E ","4548 CGCS2000_3_Degree_GK_CM_117E ","4549 CGCS2000_3_Degree_GK_CM_120E ","4550 CGCS2000_3_Degree_GK_CM_123E","4551 CGCS2000_3_Degree_GK_CM_126E ","4552 CGCS2000_3_Degree_GK_CM_129E ","4553 CGCS2000_3_Degree_GK_CM_132E ","4554 CGCS2000_3_Degree_GK_CM_135E ","4568 New_Beijing_Gauss_Kruger_Zone_13 ","4569 New_Beijing_Gauss_Kruger_Zone_14","4570 New_Beijing_Gauss_Kruger_Zone_15 ","4571 New_Beijing_Gauss_Kruger_Zone_16 ","4572 New_Beijing_Gauss_Kruger_Zone_17 ","4573 New_Beijing_Gauss_Kruger_Zone_18 ","4574 New_Beijing_Gauss_Kruger_Zone_19 ","4575 New_Beijing_Gauss_Kruger_Zone_20","4576 New_Beijing_Gauss_Kruger_Zone_21 ","4577 New_Beijing_Gauss_Kruger_Zone_22 ","4578 New_Beijing_Gauss_Kruger_Zone_23 ","4579 New_Beijing_Gauss_Kruger_CM_75E ","4580 New_Beijing_Gauss_Kruger_CM_81E ","4581 New_Beijing_Gauss_Kruger_CM_87E","4582 New_Beijing_Gauss_Kruger_CM_93E ","4583 New_Beijing_Gauss_Kruger_CM_99E ","4584 New_Beijing_Gauss_Kruger_CM_105E ","4585 New_Beijing_Gauss_Kruger_CM_111E ","4586 New_Beijing_Gauss_Kruger_CM_117E ","4587 New_Beijing_Gauss_Kruger_CM_123E","4588 New_Beijing_Gauss_Kruger_CM_129E ","4589 New_Beijing_Gauss_Kruger_CM_135E ","4652 New_Beijing_3_Degree_Gauss_Kruger_Zone_25 ","4653 New_Beijing_3_Degree_Gauss_Kruger_Zone_26 ","4654 New_Beijing_3_Degree_Gauss_Kruger_Zone_27","4655 New_Beijing_3_Degree_Gauss_Kruger_Zone_28 ","4656 New_Beijing_3_Degree_Gauss_Kruger_Zone_29 ","4766 New_Beijing_3_Degree_Gauss_Kruger_Zone_30 ","4767 New_Beijing_3_Degree_Gauss_Kruger_Zone_31 ","4768 New_Beijing_3_Degree_Gauss_Kruger_Zone_32","4769 New_Beijing_3_Degree_Gauss_Kruger_Zone_33 ","4770 New_Beijing_3_Degree_Gauss_Kruger_Zone_34 ","4771 New_Beijing_3_Degree_Gauss_Kruger_Zone_35 ","4772 New_Beijing_3_Degree_Gauss_Kruger_Zone_36 ","4773 New_Beijing_3_Degree_Gauss_Kruger_Zone_37","4774 New_Beijing_3_Degree_Gauss_Kruger_Zone_38 ","4775 New_Beijing_3_Degree_Gauss_Kruger_Zone_39 ","4776 New_Beijing_3_Degree_Gauss_Kruger_Zone_40 ","4777 New_Beijing_3_Degree_Gauss_Kruger_Zone_41 ","4778 New_Beijing_3_Degree_Gauss_Kruger_Zone_42 ","4779 New_Beijing_3_Degree_Gauss_Kruger_Zone_43 ","4780 New_Beijing_3_Degree_Gauss_Kruger_Zone_44 ","4781 New_Beijing_3_Degree_Gauss_Kruger_Zone_45 ","4782 New_Beijing_3_Degree_Gauss_Kruger_CM_75E","4783 New_Beijing_3_Degree_Gauss_Kruger_CM_78E ","4784 New_Beijing_3_Degree_Gauss_Kruger_CM_81E ","4785 New_Beijing_3_Degree_Gauss_Kruger_CM_84E ","4786 New_Beijing_3_Degree_Gauss_Kruger_CM_87E ","4787 New_Beijing_3_Degree_Gauss_Kruger_CM_90E","4788 New_Beijing_3_Degree_Gauss_Kruger_CM_93E ","4789 New_Beijing_3_Degree_Gauss_Kruger_CM_96E ","4790 New_Beijing_3_Degree_Gauss_Kruger_CM_99E ","4791 New_Beijing_3_Degree_Gauss_Kruger_CM_102E ","4792 New_Beijing_3_Degree_Gauss_Kruger_CM_105E","4793 New_Beijing_3_Degree_Gauss_Kruger_CM_108E ","4794 New_Beijing_3_Degree_Gauss_Kruger_CM_111E ","4795 New_Beijing_3_Degree_Gauss_Kruger_CM_114E ","4796 New_Beijing_3_Degree_Gauss_Kruger_CM_117E ","4797 New_Beijing_3_Degree_Gauss_Kruger_CM_120E","4798 New_Beijing_3_Degree_Gauss_Kruger_CM_123E ","4799 New_Beijing_3_Degree_Gauss_Kruger_CM_126E ","4800 New_Beijing_3_Degree_Gauss_Kruger_CM_129E ","4822 New_Beijing_3_Degree_Gauss_Kruger_CM_135E"]
PROJECT_WKID = ["3857","4508","2327","2328","2329","2330","2331","2332","2333","2334","2335","2336","2337","2338","2339","2340","2341","2342","2343","2344","2345","2346","2347","2348","2349","2350","2351","2352","2353","2354","2355","2356","2357","2358","2359","2360","2361","2362","2363","2364","2365","2366","2367","2368","2369","2370","2371","2372","2373","2374","2375","2376","2377","2378","2379","2380","2381","2382","2383","2384","2385","2386","2387","2388","2389","2390","2401","2402","2403","2404","2405","2406","2407","2408","2409","2410","2411","2412","2413","2414","2415","2416","2417","2418","2419","2420","2421","2422","2423","2424","2425","2426","2427","2428","2429","2430","2431","2432","2433","2434","2435","2436","2437","2438","2439","2440","2441","2442","3395","4491","4492","4493","4494","4495","4496","4497","4498","4499","4500","4501","4502","4503","4504","4505","4506","4507","4509","4510","4511","4512","4513","4514","4515","4516","4517","4518","4519","4520","4521","4522","4523","4524","4525","4526","4527","4528","4529","4530","4531","4532","4533","4534","4535","4536","4537","4538","4539","4540","4541","4542","4543","4544","4545","4546","4547","4548","4549","4550","4551","4552","4553","4554","4568","4569","4570","4571","4572","4573","4574","4575","4576","4577","4578","4579","4580","4581","4582","4583","4584","4585","4586","4587","4588","4589","4652","4653","4654","4655","4656","4766","4767","4768","4769","4770","4771","4772","4773","4774","4775","4776","4777","4778","4779","4780","4781","4782","4783","4784","4785","4786","4787","4788","4789","4790","4791","4792","4793","4794","4795","4796","4797","4798","4799","4800","4822"]

# 图层/图层组合法性检查：数字和字母组合，不允许纯数字
NUM_LETTER = re.compile("^(?!\d+$)[\da-zA-Z_]+$")
FIRST_LETTER = re.compile("^[a-zA-Z]")           #只能以字母开头

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(934, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 140, 72, 15))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 410, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 111, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(140, 80, 151, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 140, 151, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 200, 151, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 260, 151, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 200, 72, 15))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 260, 91, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 30, 211, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 410, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(540, 60, 121, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(520, 30, 211, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(510, 110, 121, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(640, 110, 141, 21))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(640, 160, 141, 21))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(510, 160, 131, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(520, 210, 101, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(640, 210, 141, 21))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(20, 330, 101, 16))
        self.label_13.setObjectName("label_13")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 330, 93, 28))
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(320, 330, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(260, 330, 41, 16))
        self.label_14.setObjectName("label_14")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(150, 490, 701, 191))
        self.textBrowser.setObjectName("textBrowser")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(40, 580, 72, 15))
        self.label_15.setObjectName("label_15")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(540, 260, 72, 15))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(640, 60, 141, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(640, 260, 141, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(390, 410, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 934, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuabout = QtWidgets.QMenu(self.menuBar)
        self.menuabout.setObjectName("menuabout")
        MainWindow.setMenuBar(self.menuBar)
        self.about = QAction(MainWindow)
        self.about.setObjectName("about")
        self.about.setShortcut("Ctrl+A")  # 设置快捷键
        self.menuabout.addAction(self.about)
        self.menuBar.addAction(self.menuabout.menuAction())

        # 禁止最大化按钮
        MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.lineEdit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GeoTIFF批量发布工具"))
        self.label.setText(_translate("MainWindow", "账号:"))
        self.pushButton.setText(_translate("MainWindow", "发布图层"))
        self.label_4.setText(_translate("MainWindow", "Geoserver地址:"))
        self.label_5.setText(_translate("MainWindow", "密码:"))
        self.label_6.setText(_translate("MainWindow", "workspace:"))
        self.label_7.setText(_translate("MainWindow", "GeoServer基本参数:"))
        self.pushButton_2.setText(_translate("MainWindow", "取消任务"))
        self.label_8.setText(_translate("MainWindow", "WKID: "))
        self.label_9.setText(_translate("MainWindow", "切片格式:"))
        self.label_10.setText(_translate("MainWindow", "切片金字塔层数:"))
        self.label_11.setText(_translate("MainWindow", "metersPerUnit:"))
        self.label_12.setText(_translate("MainWindow", "threadCount:"))
        self.label_13.setText(_translate("MainWindow", "geotiff文件:"))
        self.pushButton_3.setText(_translate("MainWindow", "选择文件"))
        self.pushButton_4.setText(_translate("MainWindow", "选择文件夹"))
        self.label_14.setText(_translate("MainWindow", "或者"))
        self.label_15.setText(_translate("MainWindow", "详细日志:"))
        self.label_2.setText(_translate("MainWindow", "Size:"))
        self.pushButton_5.setText(_translate("MainWindow", "发布图层组"))
        self.menuabout.setTitle(_translate("MainWindow", "about"))
        self.about.setText(_translate("MainWindow", "About"))


class Window(QMainWindow, Ui_MainWindow):
    servername = "http://localhost:8080"
    username = "admin"
    password = "geoserver"
    workspace = "cite"
    wkid = PROJECT_WKID[0]
    levels = 7
    metersPerUnit = 1
    threadCount = 1
    size = "256"
    # 待发布的Tiff文件列表
    filelists = []
    groupname = "defaultgroup"

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setupUi(self)

        # 设置按钮颜色
        self.pushButton.setStyleSheet("background-color: red")
        self.pushButton_2.setStyleSheet("background-color: red")
        self.pushButton_5.setStyleSheet("background-color: red")
        # 设置默认值
        self.lineEdit.setText(str(self.servername))
        self.lineEdit_2.setText(str(self.username))
        self.lineEdit_3.setText(str(self.password))
        self.lineEdit_4.setText(str(self.workspace))
        self.comboBox.addItems(PROJECT)
        self.comboBox_2.addItems(["256*256","512*512"])
        self.lineEdit_6.setText(str(self.levels))
        # self.lineEdit_6.setValidator(QIntValidator(1,50))
        self.lineEdit_7.setText(str(self.metersPerUnit))
        self.lineEdit_7.setEnabled(False)
        self.lineEdit_8.setText(str(self.threadCount))
        # self.lineEdit_8.setValidator(QIntValidator(1,100))
        # 设置监听事件
        self.lineEdit.textEdited.connect(lambda: self.onServerNameChanged())
        self.lineEdit_2.textEdited.connect(lambda: self.onUserNameChanged())
        self.lineEdit_3.textEdited.connect(lambda: self.onPasswordChanged())
        self.lineEdit_4.textEdited.connect(lambda: self.onWorkspaceChanged())
        self.lineEdit_6.editingFinished.connect(lambda: self.onLevelsChanged())
        self.lineEdit_8.editingFinished.connect(lambda: self.onThreadCountChanged())
        self.pushButton.clicked.connect(lambda: self.onPublishLayers())
        self.pushButton_2.clicked.connect(lambda: self.onCancel())
        self.pushButton_3.clicked.connect(lambda: self.onChoseFiles())
        self.pushButton_4.clicked.connect(lambda: self.onChoseDir())
        self.comboBox.currentIndexChanged.connect(lambda : self.onWKIDChanged())
        self.comboBox_2.currentIndexChanged.connect(lambda : self.onSizeChanged())
        self.pushButton_5.clicked.connect(lambda : self.onPublishGroup())
        # 查询缓存状态计时器
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.HasCacheFinished())
        # about 开发者信息
        self.about.setStatusTip('created by wuyan on 2020.10.2')
        self.about.triggered.connect(lambda: self.onAbout())
        # statustip提示
        self.comboBox.setStatusTip('Coordinate Reference System (Projection Coordinate System Only)!')
        self.comboBox_2.setStatusTip('the width and height of each tile!')
        self.lineEdit_8.setStatusTip('the thread used to tile maps!')
        self.lineEdit_7.setStatusTip('under PCS the param metersPerUnit can be only 1!')


    def onServerNameChanged(self):
        self.servername = self.lineEdit.text()
        GeoServer_Publisher.SERVER_NAME = self.servername

    def onUserNameChanged(self):
        self.username = self.lineEdit_2.text()
        GeoServer_Publisher.USERNAME = self.username

    def onPasswordChanged(self):
        self.password = self.lineEdit_3.text()
        GeoServer_Publisher.PASSWORD = self.password

    def onWorkspaceChanged(self):
        self.workspace = self.lineEdit_4.text()

    def onWKIDChanged(self):
        self.wkid = str(PROJECT_WKID[self.comboBox.currentIndex()])
        #QMessageBox.information(None,"tip","你选择的坐标系必须与GeoTIFF的坐标系一致!",QMessageBox.Yes)

    def onSizeChanged(self):
        self.size = "256" if self.comboBox_2.currentIndex() == 0 else "512"

    def onLevelsChanged(self):
        try:
            self.levels = int(self.lineEdit_6.text())
            if self.levels <= 0:
                raise Exception
        except Exception:
            QMessageBox.warning(None, 'warning', 'levels must be a positive number!', QMessageBox.Yes)
            self.lineEdit_6.setText("7")
            self.levels = 7

            return

    def onThreadCountChanged(self):
        try:
            self.threadCount = int(self.lineEdit_8.text())
            if self.threadCount <= 0:
                raise Exception
        except Exception:
            QMessageBox.warning(None, 'warning', 'threatCount must be a number!', QMessageBox.Yes)
            self.lineEdit_8.setText("1")
            self.threadCount = 1
            return

    def onPublishLayers(self):
        # 发布服务
        if len(self.filelists) <= 0:
            QMessageBox.warning(None, 'warning', '请先选择需要发布的TIFF文件或文件夹!', QMessageBox.Yes)
            return
        else:
            self.textBrowser.append("processing uploade tasks !")
            step = 1
            for file in self.filelists:
                (filepath, tempfilename) = os.path.split(file)
                (filename, extension) = os.path.splitext(tempfilename)
                # 服务名称：使用文件名称
                layername = filename.replace('-', '_').replace('—', '_').replace('+', '_')
                # 发布服务
                try:
                    # 发布到GeoServer
                    self.PublishProcess(file, layername)
                    # 查询服务状态
                    self.timer.start(2000)
                except Exception as e:
                    QMessageBox.warning(None, "error", str(e), QMessageBox.Yes)
                    return

                # 暂停一下
                time.sleep(1)

        #QMessageBox.information(None, "info", "服务上传成功，正在生成切片！可在详细日志处查看切片缓存状态。", QMessageBox.Yes)

    def onCancel(self):
        QMessageBox.information(None, "info", "你需要手动在Geoserver管理界面中关闭正在运行的task!", QMessageBox.Yes)

    def onChoseDir(self):
        dir_choose = QFileDialog.getExistingDirectory(None, "选取文件夹", os.getcwd())  # 起始
        if dir_choose == "":
            return

        self.filelists.clear()
        for file in os.listdir(dir_choose):
            if file.endswith(".tif"):
                self.filelists.append(dir_choose + "/" + file)

        if len(self.filelists) <= 0:
            self.textBrowser.append("warning: no tiff file in selected dir " + dir_choose)
            return
        self.textBrowser.append("selected files:" + str(self.filelists))

    def onChoseFiles(self):
        files, status = QtWidgets.QFileDialog.getOpenFileNames(None, "选取文件", os.getcwd(), "TiFF Files(*.tif)")
        if status == "":
            return

        self.filelists.clear()
        for file in files:
            self.filelists.append(file)

        self.textBrowser.append("selected files:" + str(self.filelists))

    def onAbout(self):
        QMessageBox.information(None, "info", "Created by WuYan on Sat Sep 26 19:48:34 2020. \nVersion:  1.0.0 \nENV:  Python  3.8 \nTOOL:  PyQt  5.15.1 \nSERVER:  GeoServer  2.17.2 \nGeoServer Rest API (GeoServer 2.18.x User Manual)", QMessageBox.Yes)

        # 发布缓存切片

    def onPublishGroup(self):
        # 文件检查
        if len(self.filelists) <= 0:
            QMessageBox.warning(None, 'warning', '请先选择需要发布的TIFF文件或文件夹!', QMessageBox.Yes)
            return

        # 输入图层组名称并进行合法性检查
        gpname, ok3 = QInputDialog.getText(self, "请输入layergroup参数", "layergroup名称:", QLineEdit.Normal, "layergrop1")
        self.groupname = gpname
        if not ok3:
            return

        # publish layergroup
        try:
            # 发布服务并缓存
            self.PublishGroupProcess()
            # 查询服务状态
            self.timer.start(2000)
        except Exception as e:
            QMessageBox.warning(None, "error", str(e), QMessageBox.Yes)
            return

        return

    # 发布单个图层
    def PublishProcess(self, filepath, layername):
        # 0.验证地址及账号密码是否正确
        if not GeoServer_Publisher.VerifyInfo():
            msg = "error: connect to geoserver faild: -url " + self.servername + "  -u " + self.username + "   -p " + self.password
            self.textBrowser.append("<font color='red'>" + msg + "<font>")
            raise Exception("账号密码或地址错误!")
            return

        # 1.创建Geoserver工作区
        GeoServer_Publisher.CreateWorkSpace(self.workspace)
        self.textBrowser.append("create or update workspace: " + self.workspace + " success!")
        QApplication.processEvents()

        # 2.发布TIFF图层
        try:
            GeoServer_Publisher.CreateCoverage(self.workspace, layername, filepath)
        except Exception:
            msg = "error: GeoTIFF "+filepath+" 格式错误，请检查后重试！<br>tip: GeoTiff文件目录下应同时含有.tif .ovr .tfw .aux!"
            self.textBrowser.append("<font color='red'>" + msg + "<font>")
            QApplication.processEvents()
            raise Exception("geotiff格式错误!")
            return
        self.textBrowser.append("create coverage: " + self.workspace + ":" + layername + " success!")
        QApplication.processEvents()

        # 3.创建图层的切片方案
        gridname = self.workspace + "_" +layername + "_cache"
        GeoServer_Publisher.CreateGridSet_WKID4508(gridname, self.workspace, layername, self.levels, self.wkid, self.size)
        self.textBrowser.append("create gridset " + gridname + "success!")
        QApplication.processEvents()

        # 4.修改图层的切片方案
        GeoServer_Publisher.EditCacheLayer_GridSets(self.workspace, layername, gridname)
        self.textBrowser.append("The cache layer was successfully updated!")
        QApplication.processEvents()

        # 5.开始切片
        GeoServer_Publisher.CreateSeedsTask(self.workspace, layername, self.levels, self.threadCount)
        self.textBrowser.append("begin to process cache tasks! ")
        QApplication.processEvents()

    # 发布图层组
    def PublishGroupProcess(self):
        # 0.验证地址及账号密码是否正确
        if not GeoServer_Publisher.VerifyInfo():
            msg = "error: connect to geoserver faild: -url " + self.servername + "  -u " + self.username + "   -p " + self.password
            self.textBrowser.append("<font color='red'>" + msg + "<font>")
            raise Exception("账号密码或地址错误!")
            return

        # 1.创建Geoserver工作区
        GeoServer_Publisher.CreateWorkSpace(self.workspace)
        self.textBrowser.append("create or update workspace: " + self.workspace + " success!")
        QApplication.processEvents()

        # 2.发布TIFF图层
        layers = []
        layername = ""
        for file in self.filelists:
            try:
                (filepath, tempfilename) = os.path.split(file)
                (filename, extension) = os.path.splitext(tempfilename)
                # 服务名称：使用文件名称
                layername = filename.replace('-', '_').replace('—', '_').replace('+', '_')
                GeoServer_Publisher.CreateCoverage(self.workspace, layername, file)
                layers.append(self.workspace + ":" + layername)
            except Exception:
                msg = "error: GeoTIFF " + filepath + " 格式错误，请检查后重试！<br>tip: GeoTiff文件目录下应同时含有.tif .ovr .tfw .aux!"
                self.textBrowser.append("<font color='red'>" + msg + "<font>")
                QApplication.processEvents()
                raise Exception("geotiff格式错误!")
                return
            self.textBrowser.append("create coverage: " + self.workspace + ":" + layername + " success!")
            QApplication.processEvents()

        # 3.发布Layergroup
        GeoServer_Publisher.PublishLayerGroup_S(self.groupname,layers)

        # 4.创建图层的切片方案 使用图层组的最后一个图层创建
        gridname = "group" + "_" + self.groupname + "_cache"
        GeoServer_Publisher.CreateGridSet_WKID4508(gridname, self.workspace, layername, self.levels, self.wkid,
                                                   self.size)
        self.textBrowser.append("create gridset " + gridname + "success!")
        QApplication.processEvents()

        # 5.修改图层的切片方案
        GeoServer_Publisher.EditCacheLayer_GridSets("", self.groupname, gridname)
        self.textBrowser.append("The cache layer was successfully updated!")
        QApplication.processEvents()

        # 6.开始切片
        GeoServer_Publisher.CreateSeedsTask("", self.groupname, self.levels, self.threadCount)
        self.textBrowser.append("begin to process cache tasks! ")
        QApplication.processEvents()

        return

    def HasCacheFinished(self):
        # sent request to operate geoserver
        folderURL = "/geoserver/gwc/rest/seed.json"
        response = requests.get(self.servername + folderURL, auth=(self.username, self.password))

        # 返回结果
        if (response.status_code != 200):
            self.textBrowser.append("error:" + str(response))
        else:
            try:
                res = ast.literal_eval(response.text)
                # 返回的数组结构：[tiles processed, total of tiles to process, total of remaining tiles, Task ID, Task status]
                status = ["PENDING", "RUNNING", "DONE"]

                if len(res["long-array-array"]) == 0:
                    self.textBrowser.append("*******************************************")
                    self.textBrowser.append("     all cache jobs has been finished!     ")
                    self.textBrowser.append("*******************************************")
                    self.timer.stop()
                    QMessageBox.information(None, "info", "所有切片生成成功!", QMessageBox.Yes)
                    return

                self.textBrowser.append(str(res["long-array-array"]))

                for task in res["long-array-array"]:
                    sts = "ABORTED" if task[4] == -1 else status[task[4]]
                    self.textBrowser.append(
                        "task " + str(task[3]) + " is " + sts + ": tatal " + str(task[1]) + " / finished " + str(
                            task[0]) + " / remaining " + str(task[2]))
                    if (task[4] == 2):
                        self.textBrowser.append("cache for task " + str(task[3]) + " finished!")
            except Exception as e:
                self.textBrowser.append("error in query seeds status: " + str(response))
                self.timer.stop()

    def layer_name_fomart(Name):
        re.match("^[A-Za-z0-9_]*$", Name)
        if NUM_LETTER.search(Name):
            if FIRST_LETTER.search(Name):
                return True
        return False

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())