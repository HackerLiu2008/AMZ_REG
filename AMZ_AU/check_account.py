import json
import random
import time
from threading import Thread
from selenium.webdriver.common.keys import Keys
import getinfo
import getproxy
from makedata import make_data
from selenium import webdriver

from othermethods_it import par_image, get_vircode


class Amz(object):
    # 传入注册账号id
    def __init__(self, info_id):
        self.info_id = info_id
        self.data_tool = getinfo.GetInfo('reged_au')
        # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

    # 注册填入信息界面
    def log_valid(self, y, x):

        # 获取代理
        chrome_options = getproxy.getpro('AU')
        user = self.data_tool.get_user(self.info_id)
        print(user)
        chrome_options.add_argument('user-agent={}'.format(user))
        dr = webdriver.Chrome(chrome_options=chrome_options)
        try:
            print(self.info_id)
            dr.set_page_load_timeout(70)
            # dr.set_window_size(300, 300)
            dr.set_window_position(y=y, x=x)
            dr.get(
                'https://www.amazon.com.au/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=auflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com.au%2F%3Fref_%3Dnav_signin&switch_account=')
            cookies = self.data_tool.get_cookies(self.info_id)
            with open("cookies.txt", "w") as fp:
                # json.dump(cookies, fp)
                fp.write(cookies)
            with open("cookies.txt", "r") as fp:
                cookies = json.load(fp)
                for cookie in cookies:
                    # cookie.pop('domain')  # 如果报domain无效的错误
                    dr.add_cookie(cookie)
            url_pay = "https://www.amazon.com.au/cpe/managepaymentmethods?ref_=ya_d_c_pmt_mpo"
            dr.get(url_pay)
            if 'Password' in dr.page_source:
                # time.sleep(50)
                login_wd = self.data_tool.get_info('login_wd', self.info_id)
                dr.find_element_by_id("ap_password").send_keys(login_wd)
                dr.find_element_by_xpath(
                    '//*[@id="authportal-main-section"]/div[2]/div/div/form/div/div/div/div[4]/div/div/label/div/label/span').click()
                dr.find_element_by_id('signInSubmit').click()
                if 'they are shown in the image below' in dr.page_source:
                    img_url = dr.find_element_by_id('auth-captcha-image').get_attribute('src')
                    par_image(img_url)
                    image_code = get_vircode()
                    dr.find_element_by_id("ap_password").send_keys(login_wd)
                    print(image_code)
                    dr.find_element_by_id("auth-captcha-guess").send_keys(image_code)
                    dr.find_element_by_id('signInSubmit').click()
                    if "Your Amazon Wallet" in dr.page_source:
                        self.sneak_away(dr)

                if "Your Amazon Wallet" in dr.page_source:
                    self.sneak_away(dr)
            else:
                self.sneak_away(dr)
            # 也有可以不用验证，直接进去的

        except:
            print('###################')
        dr.quit()
        return

    def sneak_away(self, dr):
        input_kw = dr.find_element_by_id("twotabsearchtextbox")
        k = make_data.get_kw()
        input_kw.send_keys(k)
        input_kw.send_keys(Keys.ENTER)

        try:
            dr.find_element_by_xpath(
                '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div[{}]//h5/a'.format(random.randint(1, 3))).click()
            self.like_car(dr)
        except:
            print('点击商品详情失败!')

        return

    def like_car(self, dr):
        # WebDriverWait(dr, 60).until(EC.presence_of_element_located(
        #         (By.XPATH, '//*[@id="add-to-cart-button"]')))
        car = dr.find_element_by_xpath('//*[@id="add-to-cart-button"]')
        car.click()
        print('{}:注册溜号成功!'.format(self.info_id))
        cookies = dr.get_cookies()
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        self.data_tool.update_cookies(self.info_id)
        self.data_tool.update_two(1, self.info_id)

        return


def run(q, y, x):
    size = q.empty()
    while not size:
        info_id = q.get()
        amz = Amz(info_id)
        amz.log_valid(y, x)
        if q.empty():
            break


if __name__ == '__main__':
    q = getinfo.GetInfo('reged_au').get_no(" 0")

    threads = []
    loops = range(20)

    for i in loops:
        thread = Thread(target=run, args=(q, 0, 0))
        threads.append(thread)

    for i in loops:
        threads[i].start()
        time.sleep(1)

    for i in loops:
        threads[i].join()
