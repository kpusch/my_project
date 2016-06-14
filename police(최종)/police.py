# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'police.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication



from xml.dom.minidom import parse, parseString # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree

##### global
loopFlag = 1
xmlFD = -1
BooksDoc = None

# smtp 정보


host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"


def read(): #파씽
    import urllib.request
    import xml.etree.ElementTree as etree
    global root
    #서울공공데이터사용
    key = '54584a59446e79333438764e655876'
    url = "http://openapi.seoul.go.kr:8088/%s/xml/SebcPoliceStationKor/1/270/" % key

    data = urllib.request.urlopen(url).read()

    filename = "sample2.xml"
    f = open(filename, "wb") #다른 사람들의 예제처럼 "w"만 해서 했더니 에러가 발생
    f.write(data)
    f.close()

    #파싱하기
    tree = etree.parse(filename)
    root = tree.getroot()


def LoadXMLFromFile():
    fileName = "police.xml"#str(input ("please input file name to load :"))  # 읽어올 파일경로를 입력 받습니다.
    global xmlFD
 
    try:
        xmlFD = open(fileName)   # xml 문서를 open합니다.
    except IOError:
        print ("invalid file name or path")
        return None
    else:
        try:
            dom = parse(xmlFD)   # XML 문서를 파싱합니다.
        except Exception:
            print ("읽어오기 실패!")
        else:
            #print ("읽어오기 완료!")
            return dom
    return None


def checkDocument():
    global BooksDoc
    if BooksDoc == None:
        print("비어있습니다 ! ")
        return False
    return True


def sendMain():
    global host, port
    html = ""
    title = str(input ('제목을 입력하세요:'))
    senderAddr = str(input ('보내는 사람 이메일 입력(gmail):'))
    recipientAddr = str(input ('받는 사람 이메일 입력  :'))
    msgtext = str(input ('write message :'))
    passwd = str(input ('보내는사람 계정의 비밀번호를 입력하세요:'))
    msgtext = str(input ('첨부할 데이터가 있습니까?(y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('검색할 키워드를 입력하세요:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
    
    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # 로긴을 합니다. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    # DOM 개체를 생성합니다.
    impl = getDOMImplementation()
    
    newdoc = impl.createDocument(None, "html", None)  # HTML 최상위 엘리먼트를 생성합니다.
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성
    body = newdoc.createElement('body')

    for bookitem in BookList:
        # Bold 엘리먼트를 생성합니다.
        b = newdoc.createElement('b')
        # 텍스트 노드를 만듭니다.
        nameText = newdoc.createTextNode("이름: " + bookitem[0])
        b.appendChild(nameText)

        body.appendChild(b)
    
        # <br> 부분을 생성합니다.
        br = newdoc.createElement('br')

        body.appendChild(br)

        # title 부분을 생성합니다.
        p = newdoc.createElement('p')
        # 텍스트 노드를 만듭니다.
        titleText= newdoc.createTextNode("구분 :" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  # <br> 부분을 부모 에릴먼트에 추가합니다.

        # <br> 부분을 생성합니다.
        ar = newdoc.createElement('br')

        # title 부분을 생성합니다.
        pr = newdoc.createElement('pr')
        # 텍스트 노드를 만듭니다.
        telText= newdoc.createTextNode("전화번호 :" + bookitem[2])
        pr.appendChild(telText)


        body.appendChild(pr)
        body.appendChild(ar) 


        # <br> 부분을 생성합니다.
        cr = newdoc.createElement('br')
        
        body.appendChild(cr)
        # title 부분을 생성합니다.
        qr = newdoc.createElement('qr')
        # 텍스트 노드를 만듭니다.
        adrText= newdoc.createTextNode("주소 :" + bookitem[3])
        qr.appendChild(adrText)

        body.appendChild(qr)
        body.appendChild(cr)


        dr = newdoc.createElement('br')
        
        body.appendChild(dr)
        
        vr = newdoc.createElement('vr')

        bar= newdoc.createTextNode("--------------------------")
        vr.appendChild(bar)

        body.appendChild(vr)
        body.appendChild(dr)
 

        

        
         
    # Body 엘리먼트를 최상위 엘리먼트에 추가시킵니다.
    top_element.appendChild(body)
    
    return newdoc.toxml()


def SearchBookTitle(keyword):
    global BooksDoc
    retlist = []
    if not checkDocument():
        return None
        
    try:
        tree = ElementTree.fromstring(str(BooksDoc.toxml()))
    except Exception:
        print ("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None
        
    # Book 엘리먼트 리스트를 가져 옵니다.
    bookElements = tree.getiterator("row") 
    for item in bookElements:
        strTitle = item.find("NAME_KOR")
        strWK = item.find("CATE2_NAME")
        strSA = item.find("TEL")
        strSUN = item.find("ADD_KOR_ROAD")
        if (strSUN.text.find(keyword) >=0 ):
            retlist.append((strTitle.text,strWK.text,strSA.text,strSUN.text))
    return retlist    

    

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(446, 416)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 421, 381))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(160, 20, 93, 28))
        self.pushButton.setObjectName("pushButton")
        
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(60, 60, 301, 291))
        self.listWidget.setObjectName("listWidget")
        
        self.tabWidget.addTab(self.tab, "")
        
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textBrowser = QtWidgets.QTextEdit(self.tab_2)
        self.textBrowser.setGeometry(QtCore.QRect(80, 10, 271, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 60, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listView_2 = QtWidgets.QListWidget(self.tab_2)
        self.listView_2.setGeometry(QtCore.QRect(80, 100, 271, 221))
        self.listView_2.setObjectName("listView_2")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 64, 15))
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 310, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit.setGeometry(QtCore.QRect(100, 20, 251, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_2.setGeometry(QtCore.QRect(100, 70, 251, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_3.setGeometry(QtCore.QRect(100, 120, 251, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_4.setGeometry(QtCore.QRect(100, 170, 251, 81))
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_5 = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_5.setGeometry(QtCore.QRect(100, 270, 251, 31))
        self.textEdit_5.setObjectName("textEdit_5")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(10, 20, 64, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 64, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 64, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(10, 200, 64, 15))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(10, 280, 64, 15))
        self.label_5.setObjectName("label_5")
        
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.pushButton.clicked.connect(self.allprint)
        self.pushButton_3.clicked.connect(self.searchprint)
        self.pushButton_2.clicked.connect(self.email)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Search(All)"))


        self.pushButton_3.setText(_translate("Form", "Search"))
        self.label_5.setText(_translate("Form", "동 입력"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Search(Dong)"))

        self.pushButton_2.setText(_translate("Form", "Send"))
        self.label.setText(_translate("Form", "ID(Gmail)"))
        self.label_2.setText(_translate("Form", "Password"))
        self.label_3.setText(_translate("Form", "Sent To"))
        self.label_4.setText(_translate("Form", "Mail Title"))
        self.label_5.setText(_translate("Form", "동 입력"))   
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Email"))

    def allprint(self, Form):

        global BooksDoc
        if not checkDocument():  # DOM이 None인지 검사합니다.
            return None
        
        booklist = BooksDoc.childNodes
        book = booklist[0].childNodes
        for item in book:
            if item.nodeName == "row":  # 엘리먼트를 중 book인 것을 골라 냅니다.
                subitems = item.childNodes  # book에 들어 있는 노드들을 가져옵니다.
                for atom in subitems:
                    if atom.nodeName in "NAME_KOR":
                        a = atom.firstChild.nodeValue  # 이름 목록을 출력 합니다.
                    if atom.nodeName in "CATE2_NAME":
                        b = atom.firstChild.nodeValue  # 서 목록을 출력 합니다.
                    if atom.nodeName in "TEL":
                        c = atom.firstChild.nodeValue  # 전화번호 목록을 출력 합니다.
                    if atom.nodeName in "ADD_KOR_ROAD":
                        d = atom.firstChild.nodeValue  # 주소 목록을 출력 합니다.                    
                self.listWidget.addItems((a,b,c,d,"-----------------------------------------------------------------"))

    def searchprint(self, Form):
        self.listView_2.clear()
        keyword = self.textBrowser.toPlainText()
        global BooksDoc
        retlist = []
        if not checkDocument():
            return None
        
        try:
            tree = ElementTree.fromstring(str(BooksDoc.toxml()))
        except Exception:
            print ("Element Tree parsing Error : maybe the xml document is not corrected.")
            return None
        
        # Book 엘리먼트 리스트를 가져 옵니다.
        bookElements = tree.getiterator("row") 
        for item in bookElements:
            strTitle = item.find("NAME_KOR")
            strWK = item.find("CATE2_NAME")
            strSA = item.find("TEL")
            strSUN = item.find("ADD_KOR_ROAD")
            if (strSUN.text.find(keyword) >=0 ):
                retlist.append((strTitle.text,strWK.text,strSA.text,strSUN.text))
          

        
        for res in retlist:
            self.listView_2.addItems((res[0],res[1],res[2],res[3],"-----------------------------------------------------------------"))
            #print(res)
        
    def email(self, Form):


        global host, port
        html = ""

        senderAddr = self.textEdit.toPlainText()
        passwd = self.textEdit_2.toPlainText()
        recipientAddr = self.textEdit_3.toPlainText()
        title = self.textEdit_4.toPlainText()
        #msgtext = str(input ('첨부할 데이터가 있습니까?(y/n):'))
        msgtext = 'y' 
        keyword = self.textEdit_5.toPlainText()
        html = MakeHtmlDoc(SearchBookTitle(keyword))
    
        import smtplib
        # MIMEMultipart의 MIME을 생성합니다.
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
    
        #Message container를 생성합니다.
        msg = MIMEMultipart('alternative')

        #set message
        msg['Subject'] = title
        msg['From'] = senderAddr
        msg['To'] = recipientAddr
    
        msgPart = MIMEText(msgtext, 'plain')
        bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
        # 메세지에 생성한 MIME 문서를 첨부합니다.
        msg.attach(msgPart)
        msg.attach(bookPart)
    
        print ("connect smtp server ... ")
        s = smtplib.SMTP(host,port)
        #s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(senderAddr, passwd)    # 로긴을 합니다. 
        s.sendmail(senderAddr , [recipientAddr], msg.as_string())
        s.close()
    
        print ("Mail sending complete!!!")
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.textEdit_3.clear()
        self.textEdit_4.clear()
        #sendMain()
        

if __name__ == '__main__':
    import sys
    read()
    BooksDoc = LoadXMLFromFile()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QDialog()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    
    sys.exit(app.exec_())

