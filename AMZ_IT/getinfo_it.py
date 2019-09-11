import json
from queue import Queue

import pymysql


class GetInfo(object):
    '''
    对数据库操作的集合类
    '''

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='admin',
                                          db='amz_it',
                                          port=3307,
                                          charset='utf8')  # 注意是utf8不是utf-8

        self.cursor = self.connection.cursor()

        self.table = 'reg_info_1'

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # 获取reg_info表的方法
    def get_reg_info(self, title, num):

        sql = "SELECT {}  FROM {} WHERE id={}".format(title, self.table , num)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results[0][0]

        except:
            print("Error: unable to fetch data")

    def get_name(self, info_id):
        sql = 'SELECT name  FROM {} WHERE id={}'.format(self.table, info_id)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results[0][0]

        except:
            print("Error: unable to fetch data")

    def update_state(self, info_id):
        sql = 'UPDATE %s SET state = %d WHERE id = %d' % (self.table, 2, info_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print('更新状态失败')

    def update_info(self, state, login_wd, info_id):

        sql = "UPDATE %s SET state = %d,login_wd = '%s' WHERE id = %d "
        try:
            # 执行SQL语句
            self.cursor.execute(sql % (self.table, state, login_wd, info_id))
            self.connection.commit()
        except:
            print("更新数据失败")

    def update_phone_number(self, phone_number, info_id):
        sql = "UPDATE reg_info_1 SET phone_num = %d WHERE id = %d "
        try:
            # 执行SQL语句
            self.cursor.execute(sql % (phone_number, info_id))
            self.connection.commit()
        except:
            print("更新数据失败")

    def update_address(self, address_dict, info_id):
        sql = "UPDATE reg_info SET province = '%s',city = '%s',postcode = %d,address = '%s' WHERE id = %d "
        province = address_dict.get('province', '')
        city = address_dict.get('city', '')
        postcode = address_dict.get('postcode', 11012)
        address = address_dict.get('address', '')
        try:
            # 执行SQL语句
            self.cursor.execute(sql % (province, city, postcode, address, info_id))
            self.connection.commit()
        except:
            print("更新数据失败")

    def update_cookies(self, info_id):
        f = open('cookies.txt', 'r')
        s = ""
        for i in f.read():
            if i == "\\":
                i = "\\\\"
            s += i
        f.close()

        sql = "UPDATE %s SET cookies = '%s' WHERE id = %d "
        try:
            # 执行SQL语句
            self.cursor.execute(sql % (self.table, s, info_id))
            self.connection.commit()
        except:
            print("更新cookies数据失败")

    # 获取card_info表的方法
    def get_card_info(self, title, num):
        sql = "SELECT {}  FROM card_info WHERE id={}".format(title, num)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results[0][0]

        except:
            print("Error: unable to fetch data")

    # 获取表格最大id值
    def get_max_id(self):
        sql = "SELECT id  FROM {} WHERE id=(select max(id) from  {})".format(self.table, self.table)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results[0][0]

        except:
            print("Error: unable to fetch data")

    def get_fail(self):
        sql = 'SELECT id FROM {}  WHERE state != 1'.format(self.table)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            print(results)
            return results[0][0]

        except:
            print("Error: unable to fetch data")

    def get_no(self, state_code):
        q = Queue(maxsize=0)
        sql = "SELECT id  FROM {} WHERE state {}".format(self.table, state_code)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for i in results:
                q.put(i[0])
            return q

        except:
            print("Error: unable to fetch data")


#     def get_all_name(self, info_id):
#         sql = 'SELECT firstname,lastname FROM {} WHERE id = {}'.format(self.table, info_id)
#         try:
#             self.cursor.execute(sql)
#             results = self.cursor.fetchall()
#             return results[0][0] + " " + results[0][1]
#         except:
#             print('XXXXX')
#
#     def merge_name(self, info_id):
#         name = self.get_all_name(info_id)
#         sql = "UPDATE %s SET name = '%s' WHERE id = %d" % (self.table, name, info_id)
#         try:
#             self.cursor.execute(sql)
#             self.connection.commit()
#         except:
#             print('11')
#
# data_tool = GetInfo()
# print(data_tool.get_name(1).split(' ')[0])
# print(data_tool.get_name(1035).split(' ')[0])
# q = data_tool.get_no('= 0')
# size = q.empty()
# while not size:
#     data_tool.merge_name(q.get())
#




