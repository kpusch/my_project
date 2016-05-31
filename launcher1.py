# -*- coding: cp949 -*-
from subwaybook import *
from xml.dom.minidom import parse, parseString # minidom ����� �Ľ� �Լ��� ����Ʈ�մϴ�.
from xml.etree import ElementTree

##### global
loopFlag = 1
xmlFD = -1
BooksDoc = None

#### Menu  implementation
def printMenu():
    print("\nWelcome! station Manager Program (xml version)")
    print("========Menu==========")
    print("�ҷ�����:  l")
    print("��ü���: p")
    print("����:   q")
    print("���: b")
    print("�߰�: a")
    print("���� �˻�: e")
   # print("Make html: m")
    print("----------------------------------------")
    #print("Get station data from isbn: g")
    print("���� ������ : i")
    #print("sTart Web Service: t")
    print("========Menu==========")
    
def launcherFunction(menu):
    global BooksDoc
    if menu ==  'l':
        BooksDoc = LoadXMLFromFile()
    elif menu == 'q':
        QuitBookMgr()
    elif menu == 'p':
        PrintDOMtoXML()
    elif menu == 'b':
        PrintBookList(["station","WKDAY","SATDAY","SUNDAY",])
    elif menu == 'a':
        ISBN = str(input ('insert ISBN :'))
        station = str(input ('insert station :'))
        AddBook({'ISBN':ISBN, 'station':station})
    elif menu == 'e':
        keyword = str(input ('input keyword to search :'))
        printBookList(SearchBookTitle(keyword))
    elif menu == 'g': 
        isbn = str(input ('input isbn to get :'))
        #isbn = '0596513984'
        ret = getBookDataFromISBN(isbn)
        AddBook(ret)
    elif menu == 'm':
        keyword = str(input ('input keyword code to the html  :'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
        print("-----------------------")
        print(html)
        print("-----------------------")
    elif menu == 'i':
        sendMain()
    elif menu == "t":
        startWebService()
    else:
        print ("error : unknow menu key")

#### xml function implementation
def LoadXMLFromFile():
    fileName = str(input ("please input file name to load :"))  # �о�� ���ϰ�θ� �Է� �޽��ϴ�.
    global xmlFD
 
    try:
        xmlFD = open(fileName)   # xml ������ open�մϴ�.
    except IOError:
        print ("invalid file name or path")
        return None
    else:
        try:
            dom = parse(xmlFD)   # XML ������ �Ľ��մϴ�.
        except Exception:
            print ("loading fail!!!")
        else:
            print ("XML Document loading complete")
            return dom
    return None

def BooksFree():
    if checkDocument():
        BooksDoc.unlink()   # minidom ��ü �����մϴ�.

def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    BooksFree()
    
def PrintDOMtoXML():
    if checkDocument():
        print(BooksDoc.toxml())

def PrintBookList(tags):
    global BooksDoc
    if not checkDocument():  # DOM�� None���� �˻��մϴ�.
        return None
        
    booklist = BooksDoc.childNodes
    book = booklist[0].childNodes
    for item in book:
        if item.nodeName == "book":  # ������Ʈ�� �� book�� ���� ��� ���ϴ�.
            subitems = item.childNodes  # book�� ��� �ִ� ������ �����ɴϴ�.
            for atom in subitems:
                if atom.nodeName in "station":
                    print("station=",atom.firstChild.nodeValue)  # å ����� ��� �մϴ�.
                if atom.nodeName in "WKDAY":
                    print("WKDAY=",atom.firstChild.nodeValue)  # ���� ����� ��� �մϴ�.
                if atom.nodeName in "SATDAY":
                    print("SATERDAY=",atom.firstChild.nodeValue)  # ����� ����� ��� �մϴ�.
                if atom.nodeName in "SUNDAY":
                    print("SUNDAY=",atom.firstChild.nodeValue)  # �ָ� ����� ��� �մϴ�.                    


def AddBook(bookdata):
    global BooksDoc
    if not checkDocument() :
        return None
     
    # Book ������Ʈ�� ����ϴ�.
    newBook = BooksDoc.createElement('book')
    newBook.setAttribute('ISBN',bookdata['ISBN'])
    # Title ������Ʈ�� ����ϴ�.
    titleEle = BooksDoc.createElement('station')
    # �ؽ�Ʈ ������Ʈ�� ����ϴ�.
    titleNode = BooksDoc.createTextNode(bookdata['station'])
    # �ؽ�Ʈ ���� Title ������Ʈ�� ���� ��ŵ�ϴ�.
    try:
        titleEle.appendChild(titleNode)
    except Exception:
        print ("append child fail- please,check the parent element & node!!!")
        return None
    else:
        titleEle.appendChild(titleNode)

    # Title�� book ������Ʈ�� ���� ��ŵ�ϴ�.
    try:
        newBook.appendChild(titleEle)
        booklist = BooksDoc.firstChild
    except Exception:
        print ("append child fail- please,check the parent element & node!!!")
        return None
    else:
        if booklist != None:
            booklist.appendChild(newBook)

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
        
    # Book ������Ʈ ����Ʈ�� ���� �ɴϴ�.
    bookElements = tree.getiterator("book") 
    for item in bookElements:
        strTitle = item.find("station")
        strWK = item.find("WKDAY")
        strSA = item.find("SATDAY")
        strSUN = item.find("SUNDAY")
        if (strTitle.text.find(keyword) >=0 ):
            retlist.append((item.attrib["ISBN"], strTitle.text,strWK.text,strSA.text,strSUN.text))
    print("\t ISBN\t����\t����\t�����\t�ָ�")
    return retlist    

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    # DOM ��ü�� �����մϴ�.
    impl = getDOMImplementation()
    
    newdoc = impl.createDocument(None, "html", None)  # HTML �ֻ��� ������Ʈ�� �����մϴ�.
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body ������Ʈ ����
    body = newdoc.createElement('body')

    for bookitem in BookList:
        # Bold ������Ʈ�� �����մϴ�.
        b = newdoc.createElement('b')
        # �ؽ�Ʈ ��带 ����ϴ�.
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)
    
        # <br> �κ��� �����մϴ�.
        br = newdoc.createElement('br')

        body.appendChild(br)

        # title �κ��� �����մϴ�.
        p = newdoc.createElement('p')
        # �ؽ�Ʈ ��带 ����ϴ�.
        titleText= newdoc.createTextNode("station:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  # <br> �κ��� �θ� ������Ʈ�� �߰��մϴ�.
         
    # Body ������Ʈ�� �ֻ��� ������Ʈ�� �߰���ŵ�ϴ�.
    top_element.appendChild(body)
    
    return newdoc.toxml()
    
def printBookList(blist):
    for res in blist:
        print (res)
    
def checkDocument():
    global BooksDoc
    if BooksDoc == None:
        print("Error : Document is empty")
        return False
    return True


###############��������#############
def sendMain():
    global host, port
    html = ""
    title = str(input ('Title :'))
    senderAddr = str(input ('sender email address :'))
    recipientAddr = str(input ('recipient email address :'))
    msgtext = str(input ('write message :'))
    passwd = str(input (' input your password of gmail account :'))
    msgtext = str(input ('Do you want to include book data (y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
    
    import mysmtplib
    # MIMEMultipart�� MIME�� �����մϴ�.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container�� �����մϴ�.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain','utf-8')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # �޼����� ������ MIME ������ ÷���մϴ�.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP("smtp.gmail.com",587)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr,passwd)    # �α��� �մϴ�. 
    s.sendmail(senderAddr,recipientAddr,msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        from urllib.parse import urlparse
        import sys
      
        parts = urlparse(self.path)
        keyword, value = parts.query.split('=',1)

        if keyword == "title" :
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword�� �ش��ϴ� å�� �˻��ؼ� HTML�� ��ȯ�մϴ�.
            ##��� �κ��� �ۼ�.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  ����( body ) �κ��� ��� �մϴ�.
        else:
            self.send_error(400,' bad requst : please check the your url') # �� ���� ��û��� ������ �����Ѵ�.

##### run #####
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('select menu :'))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")
