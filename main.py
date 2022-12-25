from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtGui import QTextCursor
from main_gui import Ui_home
import sys
import datetime
from app_library import Instagram, Data, InstagramFollow
import threading as td
from time import sleep

class Pencere(QMainWindow, Ui_home):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Follow Bot")
        self.setupUi(self)
        self.data = Data()
        self.instagram = Instagram()
        self.follower = InstagramFollow()
        self.load_data()
        self.driver_button.clicked.connect(self.click_driver)
        self.start_button.clicked.connect(self.start)
        self.show_password.clicked.connect(self.show_password_button)
        self.save_button.clicked.connect(self.save_data)
        self.follow_button.clicked.connect(self.startFollower)
        self.show_password_flag = False
        self.driver_path = ""
        self.instagram.terminalSignal.connect(self.setTerminal)

        # self.setTerminal("Hello World")
       


    def setTerminal(self, message):
        an = datetime.datetime.now()
        saat = datetime.datetime.strftime(an, '%X') # Saat
        cursor1 = QTextCursor(self.terminal.textCursor())
        cursor1.movePosition(cursor1.MoveOperation.Down)
        self.terminal.setTextCursor(cursor1)
        self.terminal.insertPlainText(f" >> {saat} {message}\n")

        print("OK")

    def show_password_button(self):
        if(self.show_password_flag):
            self.password.setEchoMode(self.password.echoMode().Password)
            self.show_password.setText("Göster")
            self.show_password_flag = False
        else:
            self.password.setEchoMode(self.password.echoMode().Normal)
            self.show_password.setText("Gizle")
            self.show_password_flag = True

    def save_data(self):
        login = self.login.text()
        password = self.password.text()
        driver_path = self.driver.text()
        comment_link = self.comment_link.text()
        start_time = self.start_time.text()
        sleep_time = self.sleep_time.text()
        follow_limit = self.follow_number.text()
        self.data.save_data(
            login,
            password,
            driver_path,
            comment_link,
            int(start_time),
            int(sleep_time),
            int(follow_limit))

    def load_data(self):
        login = self.data.load_data(0)
        password = self.data.load_data(1)
        driver_path = self.data.load_data(2)
        comment_link = self.data.load_data(3)
        start_time = self.data.load_data(4)
        sleep_time = self.data.load_data(5)
        follow_number = self.data.load_data(6)
        self.login.setText(login)
        self.password.setText(password)
        self.driver.setText(driver_path)
        self.comment_link.setText(comment_link)
        self.start_time.setText(str(start_time))
        self.sleep_time.setText(str(sleep_time))
        self.follow_number.setText(str(follow_number))




    def click_driver(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        # dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.driver_path = filenames[0]
            self.driver.setText(self.driver_path)
            print(self.driver_path)
   
    def start(self):
        self.terminal.clear()
        self.thread = td.Thread(target=self.runDriver, daemon=True)
        self.thread.start()
    def startFollower(self):
        self.thread = td.Thread(target=self.runFollower, daemon=True)
        self.thread.start()
    def runDriver(self):
        username = self.login.text()
        password =  self.password.text()
        self.instagram.setAccount(username=username, password=password)
        self.instagram.init_browser(self.driver.text())
        self.instagram.signIn()
        self.instagram.goComment(self.comment_link.text())

    def runFollower(self):
        username = self.login.text()
        password =  self.password.text()
        self.follower.connect(username, password)
        f = open("userLists.txt","r", encoding="utf-8")
        userData = f.readlines()
        sleep(int(self.start_time.text()))
        for i in range(int(self.follow_number.text())):
            sleep(int(self.sleep_time.text()))
            length  = len(userData[i])
            id = self.follower.username2id(userData[i][:length-1])
            print(id)
            if(self.follower.userFollow(id)):
                self.setTerminal(f"{i} - {userData[i]} follow atıldı")
            else:
                self.setTerminal("Xəta baş verdi")

        self.setTerminal("Follow atma tamamlandı")


app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec())