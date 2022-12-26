from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from os import system
import sqlite3 as sql
from os.path import exists
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from instagrapi import Client


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
        wait = WebDriverWait(self.browser, 25)        
        username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        username.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        self.showTerminal("Hesaba girildi")

        el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_ac8f")))
        el.find_element_by_tag_name('button').click()
        self.showTerminal("Bildiriş bağlandı")

        clo = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_a9-z")))
        self.showTerminal("Notification bağlandı")
        clo.find_element_by_tag_name('button').click()

      
    def goComment(self, url):
        wait = WebDriverWait(self.browser, 25)        
        # self.browser.maximize_window()
        self.browser.get(url+"liked_by/")
        self.showTerminal("Commentə girildi")
        for i in range(500):
            self.browser.execute_script(f"window.scrollTo(0, {i*2});")
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        userClass = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "x78zum5")))
        users = userClass.find_elements_by_class_name("_abbj")
        system("rm userLists.txt")
        counter = 0
        self.showTerminal("İstifadəçilər yüklənir")
        

        for user in users:
            userLink = user.find_element_by_tag_name("a").get_attribute("href")
            clearUserList = userLink.replace("https://www.instagram.com/","").replace("/","").replace(" ","")
            self.showTerminal(f"{clearUserList}")
            self.writeUserList(clearUserList)
            counter+=1
        self.showTerminal(f"İstifadəçi sayı: {counter}")
        self.browser.close()

    def writeUserList(self, data):
        uList = open("userLists.txt","a",encoding="utf-8")
        uList.write(f"{data}\n")

class InstagramFollow:
    def __init__(self):
        self.client = Client()

    def connect(self, ACCOUNT_USERNAME, ACCOUNT_PASSWORD):
        self.client.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    def username2id(self, USER_ID):
        print(USER_ID)
        return self.client.user_id_from_username(USER_ID)

    def userFollow(self, user_id):
        print(user_id)
        if(self.client.user_follow(user_id)):
            return True
        else:
            return False

    

    def userUnfollow(self, user_id):
        print(user_id)
        if(self.client.user_unfollow(user_id)):
            return True
        else:
            return False



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

