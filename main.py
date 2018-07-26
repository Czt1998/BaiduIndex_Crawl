# coding utf-8
import os
import random
from BaiduIndex_Crawl import *
from get_data import *

def main():
    os.mkdir("./Data")
    for i in range(2010,2018):
        year_0 = i
        try:
            # 调用函数获取获取电影上映日期
            get_data(year_0)
            # 为存放数据创建文件夹
            os.mkdir("./Date/" + str(year_0))
            # 切片，获取电影上映日期（年、月、日）
            with open("./movie/" + str(year_0) + "_data.txt", "r") as r:
                lines = r.readlines()
                for line in lines:
                    try:
                        line = line.replace('\n', '')
                        movie_name = line.split(' ')[0]
                        movie_id = line.split(' ')[1]
                        year = line.split(' ')[2]
                        month = line.split(' ')[3]
                        day = line.split(' ')[4]
                        # 调用deal获取数据
                        try:
                            data = deal(movie_name, year, month, day)
                            print(data)
                        except:
                            print("login again." + '/n')
                            data = deal(movie_name, year, month, day)
                            while data == None:
                                account = random.choice(AccountList)
                                login_again(account)
                                data = deal(movie_name, year, month, day)
                        # 存放数据
                        with open("./Data/" + str(year) + "/" + str(movie_id) + ".txt", "a+") as w:
                            w.writelines(str(data))

                    # 若出现错误，则进行记录
                    except Exception as e:
                        with open("./Worng in second try.txt", "a+") as w:
                            line = line.replace('\n', '')
                            movie_name = line.split(' ')[0]
                            movie_id = line.split(' ')[1]
                            year = line.split(' ')[2]
                            month = line.split(' ')[3]
                            day = line.split(' ')[4]
                            w.writelines(
                                str(movie_name) + ' ' + str(movie_id) + ' ' + str(year) + ' ' + str(month) + ' ' + str(
                                    day) + '\n')
                            w.writelines(str(e) + '\n')
        # 若出现错误，则进行记录
        except Exception as e:
            with open("./Worng in first try.txt", "a+") as w:
                w.writelines("worng in " + str(year_0))
                w.writelines(str(e) + '\n')
if __name__ == '__main__':

    account = random.choice(AccountList)
    login(account)
    main()