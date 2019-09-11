import json
import time
from threading import Thread
import getinfo
import getproxy
from makedata import make_data
from selenium import webdriver
from othermethods_us import par_image, get_vircode,get_user_agent
from vir_code import get_vir_code


class Amz(object):
    # 传入注册账号id
    def __init__(self, info_id):
        self.info_id = info_id
        self.data_tool = getinfo.GetInfo('yahoo_code')

        # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

    # 注册填入信息界面
    def register(self, y, x):
        # 获取代理
        chrome_options = getproxy.getpro('US')
        user_agent = get_user_agent()
        # chrome_options.add_argument('--incognito')
        chrome_options.add_argument('lang=en')
        chrome_options.add_argument('--user-agent="{}"'.format(user_agent))
        dr = webdriver.Chrome(chrome_options=chrome_options)
        # dr.get('http://geo.geosurf.io/')
        # time.sleep(20)
        dr.set_page_load_timeout(70)
        dr.set_window_position(y=y, x=x)
        dr.delete_all_cookies()
        url = 'https://www.amazon.com/ap/register?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_custrec_newcust'

        try:
            dr.get(url)
            # 'Il tuo nome'
            print(self.info_id)
            if 'Your name' in dr.page_source:

                user_name = self.data_tool.get_name(self.info_id)
                name = dr.find_element_by_id('ap_customer_name')
                time.sleep(1)
                name.send_keys(user_name.split(' ')[0])

                amil_num = self.data_tool.get_reg_info('yahoo_num', self.info_id)
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
                if 'Enter code' in dr.page_source:
                    self.amil_code(dr, amil_num, login_wd)
                elif "Enter the characters as they are given in the challenge." in dr.page_source:

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
            # self.register(y, x)
            return

    # 获取邮箱验证码，验证邮箱, 搜索商品，点击详情页面
    def amil_code(self, dr, amil_num, login_wd):
        # 翻页后获得验证码输入框并输入

        vir = dr.find_element_by_xpath('//*[@id="cvf-page-content"]/div/div/div[1]/form/div[2]/input')
        amil_wd = self.data_tool.get_reg_info('yahoo_wd', self.info_id)
        vir_code = get_vir_code(amil_num, amil_wd)
        if vir_code == 1 or vir_code == 0:
            self.data_tool.update_info(2, '邮箱验证失败!', self.info_id)
            dr.quit()
            return
        else:
            vir.send_keys(vir_code)
            verifiter = dr.find_element_by_xpath('//*[@id="a-autoid-0"]')
            verifiter.click()

            html = dr.page_source
            name = self.data_tool.get_name(self.info_id)
            # firstname = name.split(' ')[0]
            # 'Hallo, Connor'
            bonjour_name = 'Hello, ' + name
            print(bonjour_name)
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
                sub = dr.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div')
                sub.click()
                try:
                    detail_node = dr.find_element_by_xpath(
                        '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div[1]//h2/a')
                    detail_node.click()
                except:
                   print('获取商品详情页面失败')
                finally:
                    self.like_car(dr, amil_num)

            else:
                self.data_tool.update_info(2, "邮箱已使用!", self.info_id)
                time.sleep(1)
                dr.quit()
                return

    # 点击加入购物车
    def like_car(self, dr, amil_num):
        # WebDriverWait(dr, 60).until(EC.presence_of_element_located(
        #         (By.XPATH, '//*[@id="add-to-cart-button"]')))
        car = dr.find_element_by_xpath('//*[@id="add-to-cart-button"]')
        car.click()
        dr.quit()
        print('{}:注册溜号成功!'.format(amil_num))
        return


def run(q, y, x):
    size = q.empty()
    while not size:
        info_id = q.get()
        amz = Amz(info_id)
        amz.register(y, x)
        if q.empty():
            break


if __name__ == '__main__':
    q = getinfo.GetInfo('yahoo_code').get_one_state("<> 1")

    threads = []
    loops = range(10)

    for i in loops:
        thread = Thread(target=run, args=(q, 0, 0))
        threads.append(thread)

    for i in loops:
        threads[i].start()
        time.sleep(1)

    for i in loops:
        threads[i].join()
