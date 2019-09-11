# 其他方法的集合
import re
import requests
from hashlib import md5


def get_ip_info(html):
    temp_list = re.findall('pre-wrap;">{"ip":"(.*?)","country":"(.*?)","city":.*?</pre></body></html>',
                           html)
    temp = temp_list[0]
    ip_num = temp[0]
    country = temp[1]
    return ip_num, country


def par_image(image_url):
    image_url = image_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    res = requests.get(image_url, headers=headers)

    with open('pic_code.jpg', 'wb') as f:
        f.write(res.content)








class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('pic_code.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


def get_vircode():
    rc = RClient('lakepaul', 'sumaitong', '112306', 'c8b806dfffd04a7aaafbb025e09df699')
    im = open('pic_code.jpg', 'rb').read()
    result_dict = rc.rk_create(im, 3060)
    vir_code = result_dict.get('Result')
    return vir_code

