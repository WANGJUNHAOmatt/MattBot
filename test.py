import datetime
import pickle


class Birthdays(object):

    def __init__(self):
        # 基本数据库，样例见本文件末尾
        self.birthday_database = {}
        Birthdays.load_database(self)

    # 添加一条生日到用户
    def add_birthday(self, user_id, date, name):
        if self.birthday_database.get(user_id) is None:
            self.birthday_database[user_id] = {}
        if self.birthday_database.get(user_id).get(date) is None:
            self.birthday_database.get(user_id)[date] = []
        self.birthday_database.get(user_id).get(date).append(name)

        # TODO 添加按照时间先后排序之后再保存

        print(f"添加成功！date={date}, name={name}")
        # 添加后直接保存到本地
        self.save_database()

    # 删除一个用户的生日
    def del_birthday(self, user_id, date, name):
        if self.birthday_database.get(user_id) is None:
            return "您未添加生日！"
        if self.birthday_database[user_id].get(date) is None:
            return "这一天没有生日呢！"
        if name not in self.birthday_database[user_id][date]:
            return "这一天"+name+"并没有生日记录呢！回复“生日列表”获取当前您好友的生日列表呢！"
        self.birthday_database[user_id][date].remove(name)
        if len(self.birthday_database[user_id][date]) == 0:
            self.birthday_database[user_id].pop(date)
        self.save_database()
        return "成功删除！"

    # 保存到本地
    def save_database(self):
        # pickle save
        with open('birthdays_database.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(self.birthday_database, f, pickle.HIGHEST_PROTOCOL)

    # 从本地读取
    def load_database(self):
        # pickle load
        with open('birthdays_database.pickle', 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            self.birthday_database = pickle.load(f)

    # 打印整个数据库
    def print_database(self):
        print(self.birthday_database)

    # 返回用户的好友生日列表
    def get_birthday_list(self, user_id):
        if self.birthday_database.get(user_id) is None:
            msg = "未添加好友生日，请联系qq813499516添加生日（通过命令直接添加生日正在开发中）"
            print(msg)
            return msg
        else:
            msg = ""
            for (key, value) in self.birthday_database.get(user_id).items():
                msg += str(key) + ' ' + str(value) + '\n'
                print(key, value)
            return msg

    # 获取接下来指定天数（默认14）的好友生日信息
    def get_next_birthdays(self, user_id, days=14):
        if self.birthday_database.get(user_id) is None:
            msg = "未添加好友生日，请联系qq813499516添加生日（通过命令直接添加生日正在开发中）"
            print(msg)
            return msg
        else:
            msg = ""
            for i in range(days):
                add_days = datetime.timedelta(days=i)
                if self.birthday_database.get(user_id).get(datetime.date.today()+add_days) is not None:
                    msg += str(datetime.date.today()+add_days) + ' ' + \
                           str(self.birthday_database[user_id][datetime.date.today()+add_days]) + '\n'
                    # print(datetime.date.today()+add_days,
                    #       self.birthday_database[user_id][datetime.date.today()+add_days])
            if len(msg) == 0:
                msg = "接下来的" + str(days) + "天，没有朋友过生日呢！"
            print(msg)
            return msg

    pass


if __name__ == '__main__':
    birthdays = Birthdays()
    # birthdays.print_database()
    birthdays.get_birthday_list(813499516)
    # print(len(birthdays.birthday_database[813499516][datetime.date(2020, 3, 9)]))
    birthdays.birthday_database[813499516].pop(datetime.date(2020, 3, 9))
    birthdays.save_database()
    # print(birthdays.del_birthday(813499516, datetime.date(2020, 1, 19), "王骏豪"))
    birthdays.get_birthday_list(813499516)
    # birthdays.add_birthday(813499516, datetime.date(datetime.date.today().year, 1, 19), "王骏豪")
    s = "1998-10-03"
    test = datetime.date.fromisoformat(s)
    print(test.day)
    # birthdays.get_next_birthdays(813499516)
    # birthdays.add_birthday(813499516, datetime.date(datetime.date.today().year, 3, 4), "王梓萌")
    # birthdays.print_database()


# birthday_database = {
#     # 子数据结构
#     # user_id(int): {
#     #     datetime.date: [name(str),...],
#     #     ...
#     # }
#
#     # 骏豪
#     813499516: {
#         datetime.date(today.year, 3, 9): ["温良"],
#         datetime.date(today.year, 3, 14): ["王永强"],
#         datetime.date(today.year, 3, 15): ["梁朝伟", "庞圣凡"],
#         datetime.date(today.year, 12, 12): ["马嘉城"],
#     },
#     # 郭俊言
#     2504465267: {
#         datetime.date(today.year, 3, 9): ["温良"],
#     }
# }