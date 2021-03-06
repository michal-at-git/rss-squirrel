#!/usr/bin/python
# coding: utf-8

import sys;
reload(sys);
sys.setdefaultencoding("utf-8")


from PyQt4.QtGui import *
from PyQt4.QtCore import *

class AddFeedDialog(QDialog):
  def __init__(self, parent=None):
    super(AddFeedDialog, self).__init__(parent);
  

    self.name = QLineEdit();
    self.address = QLineEdit();
    self.send = QPushButton("Add");
    self.cancel = QPushButton("Cancel");
    
    mainLayout = QVBoxLayout();
    line1 = QHBoxLayout();
    line2 = QHBoxLayout();
    line3 = QHBoxLayout();
    
    nameLabel = QLabel("Name: ");
    addressLabel = QLabel("Address: ");
    
    
    mainLayout.addLayout(line1);
    mainLayout.addLayout(line2);
    mainLayout.addLayout(line3);
    
    line1.addWidget(nameLabel);
    line1.addWidget(self.name);
    line2.addWidget(addressLabel);
    line2.addWidget(self.address);
    
    line3.addWidget(self.send);
    line3.addWidget(self.cancel);
    
    self.setWindowIcon(QIcon('GUI/ikonka.png'));
    self.setLayout(mainLayout);
    self.setWindowTitle(u"Add new RSS feed");
    self.setGeometry(400, 180, 350,80);
    self.setMaximumWidth(500);
    self.setMaximumHeight(100);
