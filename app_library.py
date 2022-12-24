from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from os import system
import sqlite3 as sql
from os.path import exists
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot


class Instagram(QObject):
    terminalSignal = Signal(str)
    def init_browser(self, driver_path="chromedriver"):
        self.followers = []
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages':'en,en_US'})
        # self.browserProfile.add_argument("--headless")
        self.browser = webdriver.Chrome(driver_path, options=self.browserProfile)

    def setAccount(self, username, password):
        self.username = username
        self.password = password

    def showTerminal(self, msg):
        print(f"Terminal class showTerminal {msg}")
        self.terminalSignal.emit(msg)
        
    def signIn(self):
        self.showTerminal("Browser açıldı")
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        if(self.browser.find_element_by_name('username') and self.browser.find_element_by_name('password')):
            usernameInput = self.browser.find_element_by_name('username')
            passwordInput = self.browser.find_element_by_name('password')
            usernameInput.send_keys(self.username)
            passwordInput.send_keys(self.password)
            passwordInput.send_keys(Keys.ENTER)
        else:
            self.showTerminal("Xəta baş verdi")
            self.browser.close()

        time.sleep(5)
        if self.browser.find_element_by_class_name('_ac8f'):
            self.showTerminal("Hesaba girildi")
            el = self.browser.find_element_by_class_name('_ac8f')
            el.find_element_by_tag_name('button').click()
        else:
            self.showTerminal("Xəta baş verdi")
            self.browser.close()

        time.sleep(5)
        if self.browser.find_element_by_class_name('_a9-z'):
            self.showTerminal("Bildiriş bağlandı")
            clo = self.browser.find_element_by_class_name('_a9-z')
            clo.find_element_by_tag_name('button').click()
        else:
            self.showTerminal("Xəta baş verdi")
            self.browser.close()

    def goComment(self, url):
        # self.browser.maximize_window()
        self.browser.get(url+"liked_by/")
        time.sleep(5)
        self.showTerminal("Commentə girildi")
        for i in range(10000):
            self.browser.execute_script(f"window.scrollTo(0, {i});")
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)
        users = self.browser.find_element_by_class_name("x78zum5").find_elements_by_class_name("_abbj")
        system("rm userLists.txt")
        counter = 0
        self.showTerminal("İstifadəçilər yüklənir")
        
        time.sleep(5)

        for user in users:
            userLink = user.find_element_by_tag_name("a").get_attribute("href")
            clearUserList = userLink.replace("https://www.instagram.com/","").replace("/","").replace(" ","")
            self.showTerminal(f"{clearUserList}")
            self.writeUserList(clearUserList)
            counter+=1
        self.showTerminal(f"İstifadəçi sayı: {counter}")
        self.browser.close()

    def writeUserList(self, data):
        uList = open("userLists.txt","a")
        uList.write(f"{data}\n")

class InstagramFollow:
    def __init__(self):
        pass


class Data:
    def __init__(self):
        self.codec = "utf-8"
        file_exists = exists("base.sqlite")
        self.sql = sql.connect("base.sqlite")
        self.cursor = self.sql.cursor()
        self.cursor.execute(
        """
        CREATE TABLE if NOT EXISTS settings (
        login TEXT,
        password TEXT, 
        driver_path TEXT, 
        comment_link TEXT, 
        start_time INT,
        sleep_time INT,
        follow_limit INT)
        """)

        if(file_exists):
            self.default_data("","","","",0,0,0)

    def default_data(self, *args):
        addValue = "INSERT INTO settings VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(args[0],args[1],args[2],args[3],args[4],args[5],args[6])
        self.cursor.execute(addValue)
        self.sql.commit()

    def load_data(self,index = 0):
        sql = "SELECT * FROM settings"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data[0][index]

    def save_data(self,*args):
        addValue = "UPDATE settings SET login = '{0}',password = '{1}', driver_path = '{2}', comment_link = '{3}', start_time = '{4}',sleep_time = '{5}',follow_limit = '{6}'".format(args[0],args[1],args[2],args[3],args[4],args[5],args[6])
        self.cursor.execute(addValue)
        self.sql.commit()
