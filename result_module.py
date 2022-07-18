import json
import smtplib
import sys
import os.path
from email.mime.text import MIMEText
from itertools import cycle

from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QWidget

import my_calendar


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def date_range():
    with open("info_date.json", 'r') as file_2:
        info_date = json.load(file_2)
    start_day = QDate.fromString(info_date, 'yyyy, M, d')
    end_day = QDate(start_day.year(), 12, 31)
    current_day = start_day
    while current_day <= end_day:
        yield current_day.toString('yyyy, M, d')
        current_day = current_day.addDays(1)


def calc_schedule():
    range_of_date = date_range()
    with open('info_days.json', 'r') as file:
        info_dict = json.load(file)
    info_from_dict = {}
    for i in info_dict:
        if info_dict[i][0] != "-":
            info_from_dict[i] = info_dict[i]
    result = dict(zip(range_of_date, cycle(info_from_dict.values())))
    with open('info_result.json', 'w+') as file_2:
        json.dump(result, file_2, ensure_ascii=False)
    print("Расчет сохранен")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(resource_path('result_widget.ui'))
        # print(self.ui.calendarWidget.__class__.__mro__)
        self.ui.calendarWidget.__class__ = my_calendar.MyCalendar
        # print(self.ui.calendarWidget.__class__.__mro__)
        self.ui.pushButton.adjustSize()
        self.ui.pushButton_3.adjustSize()
        self.start()

    def start(self):
        self.ui.show()
        try:
            with open('info_days.json', 'r+') as file:
                info_dict = json.load(file)
                if info_dict:
                    print("Загружаю настройки графика смен из файла")
                    self.load_info()
        except FileNotFoundError:
            print("Файл с информацией пуст или отсутствует")

        self.ui.setWindowTitle("Календарь сменного графика работы")
        self.ui.pushButton.clicked.connect(self.button_was_clicked)
        self.ui.pushButton_3.clicked.connect(self.send_mail)
        self.ui.calendarWidget.clicked.connect(self.set_label_text)
        self.ui.dateEdit_2.setDate(self.ui.calendarWidget.selectedDate())

    def button_was_clicked(self):
        info_dict = {}
        day1 = self.ui.comboBox_24.currentText()
        day2 = self.ui.comboBox_23.currentText()
        day3 = self.ui.comboBox_11.currentText()
        day4 = self.ui.comboBox_12.currentText()
        day5 = self.ui.comboBox_13.currentText()
        day6 = self.ui.comboBox_15.currentText()
        day7 = self.ui.comboBox_21.currentText()
        color1 = self.ui.comboBox_26.currentText()
        color2 = self.ui.comboBox_25.currentText()
        color3 = self.ui.comboBox_14.currentText()
        color4 = self.ui.comboBox_16.currentText()
        color5 = self.ui.comboBox_17.currentText()
        color6 = self.ui.comboBox_18.currentText()
        color7 = self.ui.comboBox_19.currentText()
        start_day = self.ui.dateEdit.date().toString('yyyy, M, d')

        info_dict.update(
            {"day1": (day1, color1), "day2": (day2, color2),
             "day3": (day3, color3), "day4": (day4, color4),
             "day5": (day5, color5), "day6": (day6, color6),
             "day7": (day7, color7)})

        with open('info_days.json', 'w+') as file:
            json.dump(info_dict, file, ensure_ascii=False)
        with open('info_date.json', 'w+') as file_2:
            json.dump(start_day, file_2, ensure_ascii=False)
        print("Настройки графика смен сохранены")
        calc_schedule()
        self.ui.calendarWidget.updateCells()

    def load_info(self):
        with open('info_days.json', 'r') as file:
            info_dict = json.load(file)
        # print("Начинаю загрузку смен")
        self.ui.comboBox_24.setCurrentText(info_dict["day1"][0])
        self.ui.comboBox_23.setCurrentText(info_dict["day2"][0])
        self.ui.comboBox_11.setCurrentText(info_dict["day3"][0])
        self.ui.comboBox_12.setCurrentText(info_dict["day4"][0])
        self.ui.comboBox_13.setCurrentText(info_dict["day5"][0])
        self.ui.comboBox_15.setCurrentText(info_dict["day6"][0])
        self.ui.comboBox_21.setCurrentText(info_dict["day7"][0])
        self.ui.comboBox_26.setCurrentText(info_dict["day1"][1])
        self.ui.comboBox_25.setCurrentText(info_dict["day2"][1])
        self.ui.comboBox_14.setCurrentText(info_dict["day3"][1])
        self.ui.comboBox_16.setCurrentText(info_dict["day4"][1])
        self.ui.comboBox_17.setCurrentText(info_dict["day5"][1])
        self.ui.comboBox_18.setCurrentText(info_dict["day6"][1])
        self.ui.comboBox_19.setCurrentText(info_dict["day7"][1])
        # print("Загрузка смен прошла успешно")
        with open('info_date.json', 'r') as file_2:
            info_date = json.load(file_2)
        # print("Начинаю загрузку даты")
        self.ui.dateEdit.setDate(QDate.fromString(info_date, 'yyyy, M, d'))
        # print("Загрузка даты прошла успешно")

    def set_label_text(self):
        self.ui.dateEdit_2.setDate(self.ui.calendarWidget.selectedDate())
        date = self.ui.calendarWidget.calendar_was_clicked()
        try:
            with open('info_result.json', 'r') as file:
                result_dict = json.load(file)
            format_date = QDate.fromString(date, 'yyyy, M, d').toString('dd.MM.yyyy')
            if date in result_dict:
                self.ui.label_5.setText(f"Выбрана дата {format_date} - {result_dict[date][0]}")
            else:
                self.ui.label_5.setText(f"Выбрана дата {format_date}")
        except FileNotFoundError:
            d = self.ui.calendarWidget.selectedDate().toString('dd.MM.yyyy')
            self.ui.label_5.setText(f"Выбрана дата {d}")

    def send_mail(self):
        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('*****', 'ххххх')
            recipient = self.ui.textEdit_2.toPlainText()
            mail_text = MIMEText(f"{self.ui.dateEdit_2.date().toString('dd.MM.yyyy')} {self.ui.textEdit.toPlainText()}",
                                 "", 'utf-8')

            mail.sendmail("*****", recipient, mail_text.as_string())
            mail.quit()
            print("Напоминание успешно отправлено")
        except:
            print("Напоминание не отправлено")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    app.exec()
