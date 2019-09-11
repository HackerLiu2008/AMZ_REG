import poplib

# 导入邮件相关
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import email.iterators
import re
from bs4 import BeautifulSoup
import os

mypath = os.path.abspath(__file__)


# 解析消息头中的字符串
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# 将邮件附件或内容保存至文件
# 即邮件中的附件数据写入附件文件
def savefile(filename, data, path):
    try:
        filepath = path + filename
        print('Save as: ' + filepath)
        f = open(filepath, 'wb')
    except:
        print(filepath + ' open failed')
        # f.close()
    else:
        f.write(data)
        f.close()


# 获取邮件的字符编码，首先在message中寻找编码，如果没有，就在header的Content-Type中寻找
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def print_info(msg):
    text = ''
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(addr)
                value = name + ' < ' + addr + ' > '
        # print(header + ':' + value)
        text = text + header + ':' + value
    for part in msg.walk():
        filename = part.get_filename()
        content_type = part.get_content_type()
        charset = guess_charset(part)
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            if filename != None or filename != '':
                # print('Accessory: ' + filename)
                text = text + 'Accessory: ' + filename
                savefile(filename, data, mypath)
        else:
            email_content_type = ''
            content = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            elif content_type == 'text/html':
                email_content_type = 'html'
            if charset:
                content = part.get_payload(decode=True).decode(charset)
            # print(email_content_type + ' ' + content)
            text = text + email_content_type + ' ' + content
    return text


# 开始操作邮箱

url = None


def get_vir_code(LoginEmail, OriginalEmailPassword):
    time.sleep(2)
    url = None
    openTime = 1
    maxOpenTime = 5
    pop3_server = 'pop.mail.yahoo.com'
    LoginEmail = LoginEmail
    OriginalEmailPassword = OriginalEmailPassword
    vir_code = ''
    while not vir_code:
        if openTime == maxOpenTime:
            server.quit()
            break
        openTime = openTime + 1

        try:
            server = poplib.POP3_SSL(pop3_server)
            server.user(LoginEmail)
            server.pass_(OriginalEmailPassword)
            resp, mails, objects = server.list()
            index = len(mails)
            # print('Mail total:', index)
            for i in range(index, 0, -1):
                # 取出某一个邮件的全部信息
                # print('Mail check No.:', i)
                try:

                    resp, lines, octets = server.retr(index)
                    # 邮件取出的信息是bytes，转换成Parser支持的str
                    lists = []
                    for e in lines:
                        lists.append(e.decode())
                    msg_content = '\r\n'.join(lists)
                    msg = Parser().parsestr(msg_content)
                    # print_info(msg)
                    text = print_info(msg)
                    # print(text)
                    vir_code = re.findall('<p class="otp">(\d{6})</p>', text)[0]
                    return vir_code

                except:
                    vir_code = 0
                    break

            if url != None:
                break
        except Exception as e:
            # print('Get email fail:', e)
            vir_code = 1
            return vir_code
            # server.quit()
            # time.sleep(3)
            # continue


# if __name__ == '__main__':
#     amil_code = input('请输入yahoo邮箱：')
#     pass_wd = input("请输入密码：")
#     num = get_vir_code(amil_code, pass_wd)
#     print(num)
#     time.sleep(6)
