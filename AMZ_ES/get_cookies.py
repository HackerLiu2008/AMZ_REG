from selenium.webdriver.android import webdriver
import json
import time
from threading import Thread
import getinfo_uk
from makedata import make_data
import getproxy_uk
from selenium import webdriver
from othermethods import par_image, get_vircode
from vir_code import get_vir_code

import getproxy_uk


class NEWCOOKIES():
    def __init__(self, info_id):
        self.info_id = info_id
        self.data_tool = getinfo_uk.GetInfo()
        pass

    def login(self, y, x):
        chrome_options = getproxy_uk.getpro()
        dr = webdriver.Chrome(options=chrome_options)
        dr.set_page_load_timeout(70)
        dr.set_window_size(300, 300)
        dr.set_window_position(y=y, x=x)
        url = 'https://www.amazon.co.uk/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2F%3Fref_%3Dnav_signin&switch_account='
        dr.get(url)
        try:
            if 'Sign in' in dr.page_source:
                amil = dr.find_element_by_id('ap_email')
                amil_code = self.data_tool.get_reg_info('amil_num', self.info_id)
                amil.send_keys(amil_code)
                wd = dr.find_element_by_id('ap_password')
                # wd_code = self.data_tool.get_reg_info('login_wd', self.info_id)
                wd_code = amil_code[:5] + '123'
                wd.send_keys(wd_code)
                remember = dr.find_element_by_name('rememberMe')
                remember.click()
                login = dr.find_element_by_id('signInSubmit')
                login.click()
                firstname = self.data_tool.get_name(self.info_id).split(' ')[0]
                if firstname in dr.page_source:
                    self.save_cookies(dr, wd_code)
                info1 = 'Thank you'

                info2 = 'Verification needed'
                if info2 in dr.page_source:
                    sub = dr.find_element_by_id('continue')
                    sub.click()
                    amil_info = dr.find_element_by_name('code')
                    amil_wd = self.data_tool.get_reg_info('amil_wd', self.info_id)
                    vir_code = get_vir_code(amil_code, amil_wd)
                    amil_info.send_keys(vir_code)
                    sub = dr.find_element_by_class_name('a-button-input')
                    sub.click()
                    if firstname in dr.page_source:
                        self.save_cookies(dr, wd_code)

                if info1 in dr.page_source:
                    name = dr.find_element_by_name('dcq_question_subjective_1')
                    name_wd = self.data_tool.get_name(self.info_id)
                    name.send_keys(name_wd)
                    sub = dr.find_element_by_name('cvfDcqAction')
                    sub.click()
                    if firstname in dr.page_source:
                        self.save_cookies(dr, wd_code)
                return
        except:
            # self.data_tool.update_state(self.info_id)
            dr.quit()
            return

    def save_cookies(self, dr, wd_code):
        self.data_tool.update_info(1, wd_code, self.info_id)

        cookies = dr.get_cookies()
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        self.data_tool.update_cookies(self.info_id)
        print('id:{},获取cookies成功！'.format(self.info_id))
        dr.quit()


def run(q, y, x):
    size = q.empty()
    while not size:
        info_id = q.get()
        newcookies = NEWCOOKIES(info_id)
        newcookies.login(y, x)


if __name__ == '__main__':
    q = getinfo_uk.GetInfo().get_no("<> 1")

    threads = []

    loops = range(6)

    thread1 = Thread(target=run, args=(q, 0, 0))
    threads.append(thread1)
    thread2 = Thread(target=run, args=(q, 0, 500))
    threads.append(thread2)
    thread3 = Thread(target=run, args=(q, 300, 0))
    threads.append(thread3)
    thread4 = Thread(target=run, args=(q, 300, 500))
    threads.append(thread4)
    thread5 = Thread(target=run, args=(q, 600, 0))
    threads.append(thread5)
    thread6 = Thread(target=run, args=(q, 600, 500))
    threads.append(thread6)

    for i in loops:
        threads[i].start()
        time.sleep(2)

    for i in loops:
        threads[i].join()
