# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\toolkit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1256, 859)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_2.setUsesScrollButtons(True)
        self.tabWidget_2.setTabBarAutoHide(False)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.operation_tab = QtWidgets.QWidget()
        self.operation_tab.setObjectName("operation_tab")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.operation_tab)
        self.horizontalLayout_17.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_17.setSpacing(3)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.left3 = QtWidgets.QVBoxLayout()
        self.left3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.left3.setSpacing(3)
        self.left3.setObjectName("left3")
        self.groupBox = QtWidgets.QGroupBox(self.operation_tab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.OrderTable = QtWidgets.QTableWidget(self.groupBox)
        self.OrderTable.setObjectName("OrderTable")
        self.OrderTable.setColumnCount(2)
        self.OrderTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.OrderTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.OrderTable.setHorizontalHeaderItem(1, item)
        self.OrderTable.horizontalHeader().setVisible(False)
        self.OrderTable.horizontalHeader().setCascadingSectionResizes(True)
        self.OrderTable.horizontalHeader().setDefaultSectionSize(120)
        self.OrderTable.horizontalHeader().setStretchLastSection(True)
        self.OrderTable.verticalHeader().setVisible(False)
        self.OrderTable.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_5.addWidget(self.OrderTable)
        self.load_order_btn = QtWidgets.QPushButton(self.groupBox)
        self.load_order_btn.setFlat(False)
        self.load_order_btn.setObjectName("load_order_btn")
        self.verticalLayout_5.addWidget(self.load_order_btn)
        self.left3.addWidget(self.groupBox)
        self.horizontalLayout_8.addLayout(self.left3)
        self.Left_2 = QtWidgets.QVBoxLayout()
        self.Left_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.Left_2.setSpacing(3)
        self.Left_2.setObjectName("Left_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.operation_tab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.ToolsTable = QtWidgets.QTableWidget(self.groupBox_3)
        self.ToolsTable.setObjectName("ToolsTable")
        self.ToolsTable.setColumnCount(2)
        self.ToolsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ToolsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ToolsTable.setHorizontalHeaderItem(1, item)
        self.ToolsTable.horizontalHeader().setCascadingSectionResizes(True)
        self.ToolsTable.horizontalHeader().setDefaultSectionSize(120)
        self.ToolsTable.horizontalHeader().setHighlightSections(False)
        self.ToolsTable.horizontalHeader().setStretchLastSection(False)
        self.ToolsTable.verticalHeader().setVisible(False)
        self.ToolsTable.verticalHeader().setHighlightSections(False)
        self.verticalLayout_7.addWidget(self.ToolsTable)
        self.Left_2.addWidget(self.groupBox_3)
        self.horizontalLayout_8.addLayout(self.Left_2)
        self.Right_2 = QtWidgets.QVBoxLayout()
        self.Right_2.setSpacing(3)
        self.Right_2.setObjectName("Right_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.HomeDeviceConnStatusLayout = QtWidgets.QHBoxLayout()
        self.HomeDeviceConnStatusLayout.setObjectName("HomeDeviceConnStatusLayout")
        self.HomeDeviceConnStatusWidget = QtWidgets.QWidget(self.operation_tab)
        self.HomeDeviceConnStatusWidget.setObjectName("HomeDeviceConnStatusWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.HomeDeviceConnStatusWidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.HomeDeviceConnStatusLabel = QtWidgets.QLabel(self.HomeDeviceConnStatusWidget)
        self.HomeDeviceConnStatusLabel.setObjectName("HomeDeviceConnStatusLabel")
        self.horizontalLayout_6.addWidget(self.HomeDeviceConnStatusLabel)
        self.HomeDeviceConnStatusButton = QtWidgets.QPushButton(self.HomeDeviceConnStatusWidget)
        self.HomeDeviceConnStatusButton.setObjectName("HomeDeviceConnStatusButton")
        self.horizontalLayout_6.addWidget(self.HomeDeviceConnStatusButton)
        self.HomeDeviceConnStatusLayout.addWidget(self.HomeDeviceConnStatusWidget)
        self.horizontalLayout_5.addLayout(self.HomeDeviceConnStatusLayout)
        self.timeLabel = QtWidgets.QLabel(self.operation_tab)
        self.timeLabel.setStyleSheet("font: 20pt \"Arial\";")
        self.timeLabel.setScaledContents(False)
        self.timeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout_5.addWidget(self.timeLabel)
        self.Right_2.addLayout(self.horizontalLayout_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.operation_tab)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.OrderCodeLabel = QtWidgets.QLabel(self.groupBox_4)
        self.OrderCodeLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.OrderCodeLabel.setObjectName("OrderCodeLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.OrderCodeLabel)
        self.OrderCodeEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.OrderCodeEdit.setObjectName("OrderCodeEdit")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.OrderCodeEdit)
        self.horizontalLayout_7.addLayout(self.formLayout_3)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.TargetTorqueLabel = QtWidgets.QLabel(self.groupBox_4)
        self.TargetTorqueLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.TargetTorqueLabel.setObjectName("TargetTorqueLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.TargetTorqueLabel)
        self.TargetTorqueEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.TargetTorqueEdit.setObjectName("TargetTorqueEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.TargetTorqueEdit)
        self.horizontalLayout_7.addLayout(self.formLayout_2)
        self.Right_2.addWidget(self.groupBox_4)
        self.groupBox_6 = QtWidgets.QGroupBox(self.operation_tab)
        self.groupBox_6.setFlat(True)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_6.setObjectName("formLayout_6")
        self.FirstCheckCardLabel = QtWidgets.QLabel(self.groupBox_6)
        self.FirstCheckCardLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.FirstCheckCardLabel.setObjectName("FirstCheckCardLabel")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.FirstCheckCardLabel)
        self.FirstCheckCardEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.FirstCheckCardEdit.setObjectName("FirstCheckCardEdit")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.FirstCheckCardEdit)
        self.RecheckCardLabel = QtWidgets.QLabel(self.groupBox_6)
        self.RecheckCardLabel.setScaledContents(False)
        self.RecheckCardLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.RecheckCardLabel.setObjectName("RecheckCardLabel")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.RecheckCardLabel)
        self.RecheckCardEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.RecheckCardEdit.setObjectName("RecheckCardEdit")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.RecheckCardEdit)
        self.horizontalLayout_10.addLayout(self.formLayout_6)
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setObjectName("formLayout_7")
        self.FirstCheckNameLabel = QtWidgets.QLabel(self.groupBox_6)
        self.FirstCheckNameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.FirstCheckNameLabel.setObjectName("FirstCheckNameLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.FirstCheckNameLabel)
        self.FirstCheckNameEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.FirstCheckNameEdit.setObjectName("FirstCheckNameEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.FirstCheckNameEdit)
        self.RecheckNameLabel = QtWidgets.QLabel(self.groupBox_6)
        self.RecheckNameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.RecheckNameLabel.setObjectName("RecheckNameLabel")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.RecheckNameLabel)
        self.RecheckNameEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.RecheckNameEdit.setObjectName("RecheckNameEdit")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.RecheckNameEdit)
        self.horizontalLayout_10.addLayout(self.formLayout_7)
        self.Right_2.addWidget(self.groupBox_6)
        self.groupBox_5 = QtWidgets.QGroupBox(self.operation_tab)
        self.groupBox_5.setFlat(True)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_5.setObjectName("formLayout_5")
        self.InspectionCodeLabel = QtWidgets.QLabel(self.groupBox_5)
        self.InspectionCodeLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.InspectionCodeLabel.setObjectName("InspectionCodeLabel")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.InspectionCodeLabel)
        self.InspectionCodeEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.InspectionCodeEdit.setObjectName("InspectionCodeEdit")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.InspectionCodeEdit)
        self.ProductCodeLabel = QtWidgets.QLabel(self.groupBox_5)
        self.ProductCodeLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ProductCodeLabel.setObjectName("ProductCodeLabel")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ProductCodeLabel)
        self.ProductCodeEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.ProductCodeEdit.setObjectName("ProductCodeEdit")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ProductCodeEdit)
        self.RFIDLabel = QtWidgets.QLabel(self.groupBox_5)
        self.RFIDLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.RFIDLabel.setObjectName("RFIDLabel")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.RFIDLabel)
        self.RFIDEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.RFIDEdit.setObjectName("RFIDEdit")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.RFIDEdit)
        self.horizontalLayout_9.addLayout(self.formLayout_5)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.ClassificationCodeLabel = QtWidgets.QLabel(self.groupBox_5)
        self.ClassificationCodeLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ClassificationCodeLabel.setObjectName("ClassificationCodeLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ClassificationCodeLabel)
        self.ClassificationCodeEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.ClassificationCodeEdit.setObjectName("ClassificationCodeEdit")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ClassificationCodeEdit)
        self.NameLabel = QtWidgets.QLabel(self.groupBox_5)
        self.NameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.NameLabel.setObjectName("NameLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.NameLabel)
        self.NameEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.NameEdit.setObjectName("NameEdit")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.NameEdit)
        self.SpecsLabel = QtWidgets.QLabel(self.groupBox_5)
        self.SpecsLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.SpecsLabel.setObjectName("SpecsLabel")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.SpecsLabel)
        self.SpecsEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.SpecsEdit.setObjectName("SpecsEdit")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.SpecsEdit)
        self.horizontalLayout_9.addLayout(self.formLayout_4)
        self.Right_2.addWidget(self.groupBox_5)
        self.groupBox_7 = QtWidgets.QGroupBox(self.operation_tab)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setFlat(True)
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setObjectName("formLayout_8")
        self.FirstCheckResultLabel = QtWidgets.QLabel(self.groupBox_7)
        self.FirstCheckResultLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.FirstCheckResultLabel.setObjectName("FirstCheckResultLabel")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.FirstCheckResultLabel)
        self.FirstCheckResultButton = QtWidgets.QPushButton(self.groupBox_7)
        self.FirstCheckResultButton.setObjectName("FirstCheckResultButton")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.FirstCheckResultButton)
        self.horizontalLayout_11.addLayout(self.formLayout_8)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.RecheckResultLabel = QtWidgets.QLabel(self.groupBox_7)
        self.RecheckResultLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.RecheckResultLabel.setObjectName("RecheckResultLabel")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.RecheckResultLabel)
        self.RecheckResultButton = QtWidgets.QPushButton(self.groupBox_7)
        self.RecheckResultButton.setObjectName("RecheckResultButton")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.RecheckResultButton)
        self.horizontalLayout_11.addLayout(self.formLayout_9)
        self.Right_2.addWidget(self.groupBox_7)
        self.ResultTable = QtWidgets.QTableWidget(self.operation_tab)
        self.ResultTable.setObjectName("ResultTable")
        self.ResultTable.setColumnCount(3)
        self.ResultTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ResultTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ResultTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ResultTable.setHorizontalHeaderItem(2, item)
        self.ResultTable.horizontalHeader().setCascadingSectionResizes(True)
        self.ResultTable.horizontalHeader().setDefaultSectionSize(200)
        self.ResultTable.horizontalHeader().setStretchLastSection(True)
        self.Right_2.addWidget(self.ResultTable)
        self.submit_btn = QtWidgets.QPushButton(self.operation_tab)
        self.submit_btn.setObjectName("submit_btn")
        self.Right_2.addWidget(self.submit_btn)
        self.textLog_2 = QtWidgets.QTextBrowser(self.operation_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLog_2.sizePolicy().hasHeightForWidth())
        self.textLog_2.setSizePolicy(sizePolicy)
        self.textLog_2.setObjectName("textLog_2")
        self.Right_2.addWidget(self.textLog_2)
        self.Right_2.setStretch(5, 2)
        self.Right_2.setStretch(7, 1)
        self.horizontalLayout_8.addLayout(self.Right_2)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 3)
        self.horizontalLayout_17.addLayout(self.horizontalLayout_8)
        self.tabWidget_2.addTab(self.operation_tab, "")
        self.setting_tab = QtWidgets.QWidget()
        self.setting_tab.setObjectName("setting_tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.setting_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_9 = QtWidgets.QGroupBox(self.setting_tab)
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setObjectName("formLayout_10")
        self.OrderUrlLabel = QtWidgets.QLabel(self.groupBox_9)
        self.OrderUrlLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.OrderUrlLabel.setObjectName("OrderUrlLabel")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.OrderUrlLabel)
        self.OrderUrlEdit = QtWidgets.QLineEdit(self.groupBox_9)
        self.OrderUrlEdit.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.OrderUrlEdit.setInputMask("")
        self.OrderUrlEdit.setClearButtonEnabled(True)
        self.OrderUrlEdit.setObjectName("OrderUrlEdit")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.OrderUrlEdit)
        self.MOMUrlLabel = QtWidgets.QLabel(self.groupBox_9)
        self.MOMUrlLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.MOMUrlLabel.setObjectName("MOMUrlLabel")
        self.formLayout_10.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.MOMUrlLabel)
        self.MOMUrlEdit = QtWidgets.QLineEdit(self.groupBox_9)
        self.MOMUrlEdit.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.MOMUrlEdit.setClearButtonEnabled(True)
        self.MOMUrlEdit.setObjectName("MOMUrlEdit")
        self.formLayout_10.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.MOMUrlEdit)
        self.verticalLayout_4.addLayout(self.formLayout_10)
        self.verticalLayout.addWidget(self.groupBox_9)
        self.groupBox_10 = QtWidgets.QGroupBox(self.setting_tab)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_6.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.ToolsConfigTable = QtWidgets.QTableWidget(self.groupBox_10)
        self.ToolsConfigTable.setObjectName("ToolsConfigTable")
        self.ToolsConfigTable.setColumnCount(0)
        self.ToolsConfigTable.setRowCount(0)
        self.verticalLayout_6.addWidget(self.ToolsConfigTable)
        self.ToolsConfigAddButton = QtWidgets.QPushButton(self.groupBox_10)
        self.ToolsConfigAddButton.setObjectName("ToolsConfigAddButton")
        self.verticalLayout_6.addWidget(self.ToolsConfigAddButton)
        self.verticalLayout.addWidget(self.groupBox_10)
        self.groupBox_2 = QtWidgets.QGroupBox(self.setting_tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_11 = QtWidgets.QFormLayout()
        self.formLayout_11.setObjectName("formLayout_11")
        self.deviceIPLabel = QtWidgets.QLabel(self.groupBox_2)
        self.deviceIPLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.deviceIPLabel.setObjectName("deviceIPLabel")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.deviceIPLabel)
        self.DeviceIPEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.DeviceIPEdit.setClearButtonEnabled(True)
        self.DeviceIPEdit.setObjectName("DeviceIPEdit")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.DeviceIPEdit)
        self.DevicePortLabel = QtWidgets.QLabel(self.groupBox_2)
        self.DevicePortLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.DevicePortLabel.setObjectName("DevicePortLabel")
        self.formLayout_11.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.DevicePortLabel)
        self.DevicePortEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.DevicePortEdit.setClearButtonEnabled(True)
        self.DevicePortEdit.setObjectName("DevicePortEdit")
        self.formLayout_11.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.DevicePortEdit)
        self.DeviceConnStatusLabel = QtWidgets.QLabel(self.groupBox_2)
        self.DeviceConnStatusLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.DeviceConnStatusLabel.setObjectName("DeviceConnStatusLabel")
        self.formLayout_11.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.DeviceConnStatusLabel)
        self.DeviceConnStatusButton = QtWidgets.QPushButton(self.groupBox_2)
        self.DeviceConnStatusButton.setObjectName("DeviceConnStatusButton")
        self.formLayout_11.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.DeviceConnStatusButton)
        self.verticalLayout_2.addLayout(self.formLayout_11)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.DeviceConnectButton = QtWidgets.QPushButton(self.groupBox_2)
        self.DeviceConnectButton.setObjectName("DeviceConnectButton")
        self.horizontalLayout_4.addWidget(self.DeviceConnectButton)
        self.DeviceDisconnectButton = QtWidgets.QPushButton(self.groupBox_2)
        self.DeviceDisconnectButton.setObjectName("DeviceDisconnectButton")
        self.horizontalLayout_4.addWidget(self.DeviceDisconnectButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_8 = QtWidgets.QGroupBox(self.setting_tab)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_8)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.groupBox_8)
        self.verticalLayout.setStretch(3, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.tabWidget_2.addTab(self.setting_tab, "")
        self.horizontalLayout.addWidget(self.tabWidget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "唐山转向架动检车间标定程序"))
        self.groupBox.setTitle(_translate("MainWindow", " 当日订单"))
        item = self.OrderTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "订单号"))
        item = self.OrderTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "已选择"))
        self.load_order_btn.setText(_translate("MainWindow", "同步当日订单"))
        self.groupBox_3.setTitle(_translate("MainWindow", "选择工具"))
        item = self.ToolsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "工具序列号"))
        item = self.ToolsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "已选择"))
        self.HomeDeviceConnStatusLabel.setText(_translate("MainWindow", " 标定设备连接状态"))
        self.HomeDeviceConnStatusButton.setText(_translate("MainWindow", "已连接"))
        self.timeLabel.setText(_translate("MainWindow", "00-00-00 00:00:00"))
        self.OrderCodeLabel.setText(_translate("MainWindow", "订单号    "))
        self.TargetTorqueLabel.setText(_translate("MainWindow", "标准扭矩值"))
        self.groupBox_6.setTitle(_translate("MainWindow", "人员信息"))
        self.FirstCheckCardLabel.setText(_translate("MainWindow", "初检人卡号"))
        self.RecheckCardLabel.setText(_translate("MainWindow", "复检人卡号"))
        self.FirstCheckNameLabel.setText(_translate("MainWindow", "初检人姓名"))
        self.RecheckNameLabel.setText(_translate("MainWindow", "复检人姓名"))
        self.groupBox_5.setTitle(_translate("MainWindow", " 工具信息"))
        self.InspectionCodeLabel.setText(_translate("MainWindow", "定检编号  "))
        self.ProductCodeLabel.setText(_translate("MainWindow", "物料号"))
        self.RFIDLabel.setText(_translate("MainWindow", "工具RFID"))
        self.ClassificationCodeLabel.setText(_translate("MainWindow", "分类号    "))
        self.NameLabel.setText(_translate("MainWindow", "名称"))
        self.SpecsLabel.setText(_translate("MainWindow", "规格"))
        self.FirstCheckResultLabel.setText(_translate("MainWindow", "初检结果  "))
        self.FirstCheckResultButton.setText(_translate("MainWindow", "成功"))
        self.RecheckResultLabel.setText(_translate("MainWindow", "复检结果  "))
        self.RecheckResultButton.setText(_translate("MainWindow", "成功"))
        item = self.ResultTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "时间"))
        item = self.ResultTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "扭矩值"))
        item = self.ResultTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "角度值"))
        self.submit_btn.setText(_translate("MainWindow", "提交"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.operation_tab), _translate("MainWindow", "标定"))
        self.groupBox_9.setTitle(_translate("MainWindow", "连接"))
        self.OrderUrlLabel.setText(_translate("MainWindow", "获取订单地址"))
        self.MOMUrlLabel.setText(_translate("MainWindow", "MOM上送地址"))
        self.groupBox_10.setTitle(_translate("MainWindow", "工具"))
        self.ToolsConfigAddButton.setText(_translate("MainWindow", "添加工具"))
        self.groupBox_2.setTitle(_translate("MainWindow", " 标定设备"))
        self.deviceIPLabel.setText(_translate("MainWindow", "ip"))
        self.DevicePortLabel.setText(_translate("MainWindow", "端口"))
        self.DeviceConnStatusLabel.setText(_translate("MainWindow", "连接状态"))
        self.DeviceConnStatusButton.setText(_translate("MainWindow", "    已连接"))
        self.DeviceConnectButton.setText(_translate("MainWindow", " 连接"))
        self.DeviceDisconnectButton.setText(_translate("MainWindow", " 断开"))
        self.groupBox_8.setTitle(_translate("MainWindow", "日志"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.setting_tab), _translate("MainWindow", "设置"))
