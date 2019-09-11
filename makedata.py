import random


# 制造随机信息的集成类
class MakeData(object):

    def __init__(self):
        self.name_str = 'qwertyuioplkjhgfdsazxcvbnm'
        self.phone_number = '0123456789'
        self.front_phone_number = ['06', '07']

    # 制造随机姓名 str类型
    def get_name(self):
        front_name = ''.join(random.sample(self.name_str, random.randint(5, 9))).title()
        later_name = ''.join(random.sample(self.name_str, random.randint(6, 11)))
        name = front_name + ' ' + later_name
        return name

    # 制造随机电话 int类型
    def get_phone_number(self):
        later_phone_number = ''.join(random.sample(self.phone_number, random.randint(7, 9)))
        front_phone_number = self.front_phone_number[random.randint(0, 1)]
        phone_number = front_phone_number + later_phone_number
        return int(phone_number)

    # 制造地址字典
    def get_address(self):
        dict1 = {'province': 'haute garonne', 'city': 'castelnaud estretefonds', 'postcode': 31620,
                 "address": '{} rue du capech'.format(random.randint(0, 99))}
        dict2 = {'province': 'lorraine', 'city': 'thionville', 'postcode': 57100,
                 "address": '{} rue pepin le bref'.format(random.randint(0, 99))}
        dict3 = {'province': 'MARNE', 'city': 'CORMONTREUIL', 'postcode': 51350,
                 "address": '{} RUE RES COMPAGNONS'.format(random.randint(0, 99))}
        dict4 = {'province': 'Isere', 'city': 'Maubec', 'postcode': 95110,
                 "address": '{}.A Chemin de Cesarges'.format(random.randint(100, 999))}
        dict5 = {'province': "val d'ois", 'city': 'SANNOIS', 'postcode': 38300,
                 "address": '{} allee racine'.format(random.randint(1, 999))}
        dict6 = {'province': 'paca', 'city': 'tourrettes', 'postcode': 83440,
                 "address": '{} chemin des colles'.format(random.randint(100, 999))}
        dict7 = {'province': 'Grand Est', 'city': 'Vosges', 'postcode': 88000,
                 "address": '{} Rue de Brunove'.format(random.randint(100, 999))}
        dict8 = {'province': 'Grand Est', 'city': 'Moselle', 'postcode': 57460,
                 "address": '{} Rue Sainte-Croix'.format(random.randint(0, 99))}

        address_list = [dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8]
        address_dict = address_list[random.randint(0, 7)]
        return address_dict

    def get_kw(self):
        kw = ["Clothes", "Socks", "Headphones", "Umbrella", "Mouse", "Hat"]
        key_word = kw[random.randint(0, 5)]
        return key_word

    def get_kw_jp(self):
        kw = ['スカート', 'Bluetoothヘッドセット']
        key_word = kw[random.randint(0, 1)]
        return key_word


make_data = MakeData()
