import json
import time
from threading import Thread

import getinfo
from makedata import make_data
import getproxy
from selenium import webdriver
from othermethods import par_image, get_vircode
from vir_code import get_vir_code


class Amz(object):
    # 传入注册账号id
    def __init__(self, info_id):
        self.info_id = info_id
        self.data_tool = getinfo.GetInfo('reged_us')
        # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

    # 注册填入信息界面
    def register(self, y, x):
        # 获取代理
        chrome_options = getproxy.getpro('US')
        chrome_options.add_argument("lang=en")
        user_agent = self.data_tool.get_user(self.info_id)
        chrome_options.add_argument('user-agent="{}"'.format(user_agent))
        dr = webdriver.Chrome(options=chrome_options)
        dr.set_page_load_timeout(70)
        dr.set_window_position(y=y, x=x)
        url = 'https://www.amazon.com/ap/register?showRememberMe=true&showRmrMe=1&openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&accountStatusPolicy=P1&pageId=webcs-yourorder&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Forder-history%3Fie%3DUTF8%26ref_%3Dnav_orders_first&prevRID=EKJ6E85CPEVGBB96B3SJ&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'
        try:
            dr.get(url)

            # 判断是否请求到注册页面

            if 'Your name' in dr.page_source:

                user_name = self.data_tool.get_name(self.info_id)
                name = dr.find_element_by_id('ap_customer_name')
                time.sleep(1)
                name.send_keys(user_name)

                amil_num = self.data_tool.get_reg_info('amil_num', self.info_id)
                email = dr.find_element_by_id('ap_email')
                email.send_keys(amil_num)

                login_wd = amil_num[:5] + '123'
                password = dr.find_element_by_id('ap_password')
                password.send_keys(login_wd)

                password_check = dr.find_element_by_id('ap_password_check')
                password_check.send_keys(login_wd)

                # 点击提交
                sub = dr.find_element_by_id('continue')
                sub.click()

                time.sleep(10)
                if 'Enter code' in dr.page_source:
                    self.amil_code(dr, amil_num, login_wd)
                elif "given in the challenge." in dr.page_source:

                    password = dr.find_element_by_id('ap_password')
                    password.send_keys(login_wd)
                    time.sleep(1)
                    password_check = dr.find_element_by_id('ap_password_check')
                    password_check.send_keys(login_wd)

                    image_src = dr.find_element_by_id('auth-captcha-image').get_attribute('src')
                    par_image(image_src)
                    image_code = get_vircode()
                    print(image_code)
                    captcha = dr.find_element_by_id('auth-captcha-guess')
                    captcha.send_keys(image_code)

                    sub = dr.find_element_by_id('continue')
                    sub.click()

                    self.amil_code(dr, amil_num, login_wd)

                else:
                    self.data_tool.update_info(2, login_wd, self.info_id)
                    dr.quit()
                    return

            # 没有请求到注册页面（网络超时）
            else:
                self.data_tool.update_info(2, '请求失败', self.info_id)
                dr.quit()
                return

        except:
            dr.quit()
            self.register(y, x)

    # 获取邮箱验证码，验证邮箱, 搜索商品，点击详情页面
    def amil_code(self, dr, amil_num, login_wd):
        # 翻页后获得验证码输入框并输入

        vir = dr.find_element_by_xpath('//*[@id="cvf-page-content"]/div/div/div[1]/form/div[2]/input')
        amil_wd = self.data_tool.get_reg_info('amil_wd', self.info_id)
        vir_code = get_vir_code(amil_num, amil_wd)
        if vir_code == 1:
            self.data_tool.update_info(2, '邮箱验证失败!', self.info_id)
            dr.quit()
            return
        else:
            vir.send_keys(vir_code)
            verifiter = dr.find_element_by_xpath('//*[@id="a-autoid-0"]')
            verifiter.click()

            html = dr.page_source
            name = self.data_tool.get_name(self.info_id)
            firstname = name.split(' ')[0]
            bonjour_name = 'Hello, ' + firstname
            if bonjour_name in html:

                # 更新用户状态码
                self.data_tool.update_info(1, login_wd, self.info_id)

                cookies = dr.get_cookies()
                with open("cookies.txt", "w") as fp:
                    json.dump(cookies, fp)
                self.data_tool.update_cookies(self.info_id)
                time.sleep(1)

                input_kw = dr.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
                key_word = make_data.get_kw()
                input_kw.send_keys(key_word)
                sub = dr.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]')
                sub.click()
                # wait.until(EC.presence_of_element_located((By.ID, 'a-page')))
                num = 0

                try:
                    detail_node = dr.find_element_by_xpath(
                        '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div[1]//h5/a')
                    detail_node.click()
                except:
                   print('获取商品详情页面失败')
                finally:
                    self.like_car(dr)



            else:
                self.data_tool.update_info(2, "邮箱已使用!", self.info_id)
                time.sleep(1)
                dr.quit()
                return

    # 点击加入购物车
    def like_car(self, dr):

        car = dr.find_element_by_xpath('//*[@id="add-to-cart-button"]')
        car.click()
        time.sleep(3)
        dr.quit()
        print('注册溜号成功!')
        return


def run(q, y, x):
    size = q.empty()
    while not size:
        info_id = q.get()
        print(info_id)
        amz = Amz(info_id)
        amz.register(y, x)
        if q.empty():
            break


if __name__ == '__main__':
    q = getinfo.GetInfo('reged_us').get_one_state("0")

    threads = []
    loops = range(1)

    for i in loops:
        thread = Thread(target=run, args=(q, 0, 0))
        threads.append(thread)

    for i in loops:
        threads[i].start()
        time.sleep(1)

    for i in loops:
        threads[i].join()
