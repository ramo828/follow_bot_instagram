from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from main_gui import Ui_home
import sys
from get_link_users import Instagram, Data
class Pencere(QMainWindow, Ui_home):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Follow Bot")
        self.setupUi(self)
        self.data = Data()
        self.load_data()
        self.driver_button.clicked.connect(self.click_driver)
        self.start_button.clicked.connect(self.start)
        self.show_password.clicked.connect(self.show_password_button)
        self.save_button.clicked.connect(self.save_data)
        self.show_password_flag = False
        self.driver_path = ""


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
        username = self.login.text()
        password =  self.password.text()
        instagram = Instagram(username=username, password= password)
        instagram.signIn()
        instagram.goComment(self.comment_link.text())


app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec())