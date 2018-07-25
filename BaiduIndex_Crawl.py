# coding utf-8
import time
import sys
import pytesseract
import re
import os
import shutil
from PIL import Image
from imp import reload
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
reload(sys)
driver = webdriver.Chrome()

path=os.getcwd()

def login(name, passwd):
    """
    模拟登录百度帐号
    :param name: 帐号名称
    :param passwd: 帐号密码
    :return: void
    """

    # 进入百度指数
    url = 'http://index.baidu.com/?from=pinzhuan#/'
    driver.maximize_window()
    driver.get(url)
    print('开始登录')
    time.sleep(3)

    # 定位“登录”按钮
    login_tag = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div[4]/span/span")
    login_tag.click()
    time.sleep(3)

    # 定位帐号输入框，输入帐号
    name_field = driver.find_element_by_xpath("//*[@id='TANGRAM__PSP_4__userName']")
    name_field.send_keys(name)
    time.sleep(3)

    # 定位密码输入框，输入密码
    passwd_field = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__password"]')
    passwd_field.send_keys(passwd)
    time.sleep(3)

    # 出现验证码的处理方法
    # yanzheng = driver.find_element_by_xpath("//*[@id='TANGRAM__PSP_4__verifyCodeImg']")
    # pic = yanzheng.get_attribute("src")
    # print(pic)
    # driver1.get(pic)
    # driver.save_screenshot('./pic.png')
    # rangle = (934, 470, 1026, 512)
    # img = Image.open('./pic.png')
    # jpg = img.crop(rangle)
    # jpg.save('./picc.png')
    # im = Image.open('./picc.png')
    # text = pytesseract.image_to_string(im)
    # print(text)
    # yanzheng = driver.find_element_by_xpath("//*[@id='TANGRAM__PSP_4__verifyCode']")
    # yanzheng.send_keys(text)

    # 点击“登录”按钮
    login_button = driver.find_element_by_id('TANGRAM__PSP_4__submit')
    login_button.click()
    time.sleep(3)

def deal(name,year,month,day):
    """
    获取我们所要数据
    :param name: 将要查询的电影名
    :param year: 电影上映年份
    :param month: 电影上映月份
    :param day: 电影上映日期
    :return: 电影上映前后一个月的百度指数数据
    """

    # 登录之后第一做的是except的操作，第二及以后的操作都是try中的操作
    # 输入我们要查询的电影名称
    try:
        driver.find_element_by_xpath("//*[@id='schword']").clear()
        driver.find_element_by_xpath("//*[@id='schword']").send_keys(name)
        driver.find_element_by_xpath("//*[@id='schsubmit']").click()
    except:
        driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").clear()
        driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").send_keys(name)
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div[2]/div/div[1]/div/div[2]/div/span/span").click()
    time.sleep(3)

    # 计算电影上映前一个月与后一个月的日期
    #fyear，fmonth为上映前一个月的日期信息，ayear，amonth为上映后一个月的日期信息
    fyear,fmonth,ayear,amonth=CalculateDate(year,month)

    # 点击网页上日期”自定义“
    # 选择网页上的开始日期
    driver.maximize_window()
    driver.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
    driver.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
    driver.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(fyear) + "']").click()
    driver.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
    driver.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(fmonth) + "']").click()
    # 选择网页上的截止日期
    driver.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
    driver.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(ayear) + "']").click()
    driver.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
    driver.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(amonth) + "']").click()
    driver.find_element_by_xpath("//input[@value='确定']").click()
    time.sleep(1)

    # 月份-日字典
    Monthdict = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
            '11': 30, '12': 31, '1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30}
    # 闰年处理
    if int(year) == 2012 or int(year) == 2016:
        Monthdict['02'] = 29
    return CollectIndex(Monthdict,fyear,fmonth,day,name)

def CalculateDate(year, month):
    """
    计算电影上映前后一个月的日期
    :param year: 电影上映年份
    :param month: 电影上映月份
    :return: 前后一个月日期信息
    """

    # 由于百度指数上的数据最早到2011年1月，最晚到2018年7月，因此要对特定日期进行处理
    if year == '2010':
        fyear = 2011
        fmonth = '02'
    else:
        fyear = year
        if int(month) == 1 and year != '2011':
            fmonth = '12'
            fyear = str(int(year) - 1)
        else:
            fmonth = str(int(month) - 1)
        if int(month)  == 1 and year == '2011':
            fmonth = '1'
            fyear = '2011'
    if len(fmonth) < 2:
        fmonth = '0' + fmonth
    if year == '2010':
        ayear = 2011
        amonth = '04'
    else:
        ayear = year
        if int(month) + 1 == 13:
            amonth = '01'
            ayear = str(int(year) + 1)
        else:
            amonth = str(int(month) + 1)
    if year == '2011' and month == '1':
        ayear = 2011
        amonth = str(int(month) + 1)
    if year == '2018' and month == '7':
        fmonth = str(int(month) - 2)
        amonth = str(int(month))
    if len(amonth) < 2:
        amonth = '0' + amonth
    return fyear, fmonth, ayear, amonth

def CollectIndex(Monthdict, fyear, fmonth, day, name):
    """
    定位我们所要的数据，并进行获取
    :param Monthdict: 日期字典
    :param name: 电影名
    :return: 所要数据
    """

    # 初始化输出String
    OutputString = str(name) + '\n' + '['

    # x_0,y_0为鼠标坐标
    x_0 = 1
    y_0 = 1
    # 根据起始具体日子计算鼠标的初始位置
    # 一日=13.51 例如,上映日期为7.20日 则x起始坐标为1+13.51*19
    if str(fyear) != '2011':
        ran = Monthdict[fmonth] + int(day) - 32
        if ran < 0:
            ran = 0.5
        x_0 = x_0 + 13.51 * ran
    else:
        day = 1

    # xoyelement为鼠标起始坐标
    xoyelement = driver.find_elements_by_css_selector("#trend rect")[2]
    #鼠标从起始坐标移动到(x_0,y_0)
    ActionChains(driver).move_to_element_with_offset(xoyelement, x_0, y_0).perform()

    for i in range(61):
        # 计算当前得到指数的时间
        if int(fmonth) < 10:
            fmonth = '0' + str(int(fmonth))
        if int(day) >= Monthdict[str(fmonth)] + 1:
            day = 1
            fmonth = int(fmonth) + 1
            if fmonth == 13:
                fyear = int(fyear) + 1
                fmonth = 1
        day = int(day) + 1
        time.sleep(0.5)
        # 获取数据
        code = GetTheCode(fyear, fmonth, day, name, path, xoyelement, x_0, y_0)

        # ViewBox不出现的循环
        cot = 0
        jud = True
        # print code
        while (code == None):
            cot += 1
            code = GetTheCode(fyear, fmonth, day, name, path, xoyelement, x_0, y_0)
            if cot >= 6:
                jud = False
                break
        if jud:
            anwserCode = code.group()
            print(anwserCode)
        else:
            anwserCode = str(-1)
            if int(day) < 10:
                day = '0' + str(int(day))
            if int(fmonth) < 10:
                fmonth = '0' + str(int(fmonth))
        OutputString += str(fyear) + '-' + str(fmonth) + '-' + str(int(day) - 1) + ':' + str(anwserCode) + ','
        x_0 = x_0 + 13.51
    OutputString += ']\n'
    print(OutputString)
    return OutputString

def GetTheCode(fyear,fmonth,day,name,path,xoyelement,x_0, y_0):
    """
    定位viewbox，获取数据
    :param path: 文件存放路径
    :return: 一天的百度指数数据
    """
    # 移动鼠标操作
    ActionChains(driver).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
    #鼠标重复操作直到ViewBox出现
    cot1=0
    while (ExistBox(driver)==False):
        cot1+=1
        ActionChains(driver).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
        if ExistBox(driver)==True:
            break
        if cot1>=6:
            return None
    time.sleep(0.5)

    # 创建存放图片的文件夹
    Create_folder()
    # 进行定位截图获取数据
    imgelement = driver.find_element_by_xpath('//div[@id="viewbox"]')
    locations = imgelement.location
    printString = str(fyear) + "-" + str(fmonth) + "-" + str(day)
    # 找到图片位置
    l = len(name)
    if l > 8:
        l = 8
    rangle = (int(int(locations['x'])) + l * 10 + 38, int(int(locations['y'])) + 28,
              int(int(locations['x'])) + l * 10 + 38 + 75,
              int(int(locations['y'])) + 56)
    #保存截图
    driver.save_screenshot(str(path) + "/raw/" + printString + ".png")
    img = Image.open(str(path) + "/raw/" + printString + ".png")
    if locations['x'] != 0.0:
         #按Rangle截取图片
        jpg = img.crop(rangle)
        imgpath = str(path) + "/crop/" + printString + ".jpg"
        jpg.save(imgpath)
        jpgzoom = Image.open(str(imgpath))
        #放大图片
        (x, y) = jpgzoom.size
        x_s = 60 * 10
        y_s = 20 * 10
        out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(path + "/zoom/" + printString, 'jpeg', quality=95)
        image = Image.open(path + "/zoom/" + printString )
        #识别图片
        code = pytesseract.image_to_string(image)
        regex = "\d+"
        pattern = re.compile(regex)

        # 为提高准确度进行判断修改
        dealcode = code.replace("S", '5').replace(" ", "").replace(",", "").replace("E", "8").replace(".", ""). \
            replace("'", "").replace(u"‘", "").replace("B", "8").replace("\"", "").replace("I", "1").replace(
            "i", "").replace("-", ""). \
            replace("$", "8").replace(u"’", "").strip()
        match = pattern.search(dealcode)
        # 删除文件夹及内部内容，准备下次操作
        Delete_folder()
        return match
    else:
        Delete_folder()
        return None

def ExistBox(driver):
    """
    判断是否找到viewbox
    """

    try:
        driver.find_element_by_xpath('//div[@id="viewbox"]')
        return True
    except:
        return False

def Create_folder():
    os.mkdir("./crop")
    os.mkdir("./raw")
    os.mkdir("./zoom")

def Delete_folder():
    shutil.rmtree("./crop")
    shutil.rmtree("./raw")
    shutil.rmtree("./zoom")
