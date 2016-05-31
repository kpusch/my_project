# -*- coding: cp949 -*-
from subwaybook import *
from xml.dom.minidom import parse, parseString # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree

##### global
loopFlag = 1
xmlFD = -1
BooksDoc = None

#### Menu  implementation
def printMenu():
    print("\nWelcome! station Manager Program (xml version)")
    print("========Menu==========")
    print("불러오기:  l")
    print("전체출력: p")
    print("종료:   q")
    print("출력: b")
    print("추가: a")
    print("역명 검색: e")
   # print("Make html: m")
    print("----------------------------------------")
    #print("Get station data from isbn: g")
    print("메일 보내기 : i")
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
    fileName = str(input ("please input file name to load :"))  # 읽어올 파일경로를 입력 받습니다.
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
            print ("loading fail!!!")
        else:
            print ("XML Document loading complete")
            return dom
    return None

def BooksFree():
    if checkDocument():
        BooksDoc.unlink()   # minidom 객체 해제합니다.

def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    BooksFree()
    
def PrintDOMtoXML():
    if checkDocument():
        print(BooksDoc.toxml())

def PrintBookList(tags):
    global BooksDoc
    if not checkDocument():  # DOM이 None인지 검사합니다.
        return None
        
    booklist = BooksDoc.childNodes
    book = booklist[0].childNodes
    for item in book:
        if item.nodeName == "book":  # 엘리먼트를 중 book인 것을 골라 냅니다.
            subitems = item.childNodes  # book에 들어 있는 노드들을 가져옵니다.
            for atom in subitems:
                if atom.nodeName in "station":
                    print("station=",atom.firstChild.nodeValue)  # 책 목록을 출력 합니다.
                if atom.nodeName in "WKDAY":
                    print("WKDAY=",atom.firstChild.nodeValue)  # 평일 목록을 출력 합니다.
                if atom.nodeName in "SATDAY":
                    print("SATERDAY=",atom.firstChild.nodeValue)  # 토요일 목록을 출력 합니다.
                if atom.nodeName in "SUNDAY":
                    print("SUNDAY=",atom.firstChild.nodeValue)  # 주말 목록을 출력 합니다.                    


def AddBook(bookdata):
    global BooksDoc
    if not checkDocument() :
        return None
     
    # Book 엘리먼트를 만듭니다.
    newBook = BooksDoc.createElement('book')
    newBook.setAttribute('ISBN',bookdata['ISBN'])
    # Title 엘리먼트를 만듭니다.
    titleEle = BooksDoc.createElement('station')
    # 텍스트 에릴먼트를 만듭니다.
    titleNode = BooksDoc.createTextNode(bookdata['station'])
    # 텍스트 노드와 Title 엘리먼트를 연결 시킵니다.
    try:
        titleEle.appendChild(titleNode)
    except Exception:
        print ("append child fail- please,check the parent element & node!!!")
        return None
    else:
        titleEle.appendChild(titleNode)

    # Title를 book 엘리먼트와 연결 시킵니다.
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
        
    # Book 엘리먼트 리스트를 가져 옵니다.
    bookElements = tree.getiterator("book") 
    for item in bookElements:
        strTitle = item.find("station")
        strWK = item.find("WKDAY")
        strSA = item.find("SATDAY")
        strSUN = item.find("SUNDAY")
        if (strTitle.text.find(keyword) >=0 ):
            retlist.append((item.attrib["ISBN"], strTitle.text,strWK.text,strSA.text,strSUN.text))
    print("\t ISBN\t역명\t평일\t토요일\t주말")
    return retlist    

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
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)
    
        # <br> 부분을 생성합니다.
        br = newdoc.createElement('br')

        body.appendChild(br)

        # title 부분을 생성합니다.
        p = newdoc.createElement('p')
        # 텍스트 노드를 만듭니다.
        titleText= newdoc.createTextNode("station:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  # <br> 부분을 부모 에릴먼트에 추가합니다.
         
    # Body 엘리먼트를 최상위 엘리먼트에 추가시킵니다.
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


###############메일전송#############
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
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain','utf-8')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP("smtp.gmail.com",587)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr,passwd)    # 로긴을 합니다. 
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
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
            ##헤더 부분을 작성.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  본분( body ) 부분을 출력 합니다.
        else:
            self.send_error(400,' bad requst : please check the your url') # 잘 못된 요청라는 에러를 응답한다.

##### run #####
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('select menu :'))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")
