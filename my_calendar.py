import json
import sys
import os.path

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QCalendarWidget, QApplication



class MyCalendar(QCalendarWidget):

    def __init__(self):
        super(MyCalendar, self).__init__()
        self.selected_date = QCalendarWidget.selectedDate(self).toString('yyyy, M, d')
        self.clicked.connect(self.calendar_was_clicked)

    def calendar_was_clicked(self):
        self.selected_date = QCalendarWidget.selectedDate(self).toString('yyyy, M, d')
        return self.selected_date

    def paintCell(self, painter, rect, date):
        QCalendarWidget.paintCell(self, painter, rect, date)
        try:
            with open("info_result.json", 'r+') as file:
                result_dict = json.load(file)

            list_of_days = []
            list_of_color = []
            for key in result_dict:
                list_of_days.append(QDate.fromString(key, 'yyyy, M, d'))
                list_of_color.append(result_dict[key][1])
            # print(list_of_color)
            # print(list_of_days)

            list_of_color_rgb = []
            for color in list_of_color:
                if color == 'Красный':
                    list_of_color_rgb.append(QColor(255, 0, 0, 50))
                elif color == 'Оранжевый':
                    list_of_color_rgb.append(QColor(255, 102, 0, 50))
                elif color == 'Желтый':
                    list_of_color_rgb.append(QColor(255, 255, 0, 50))
                elif color == 'Зеленый':
                    list_of_color_rgb.append(QColor(0, 128, 1, 50))
                elif color == 'Синий':
                    list_of_color_rgb.append(QColor(0, 0, 255, 50))
            # print(list_of_color_rgb)

            for i in range(len(list_of_days)):
                if date == list_of_days[i]:
                    painter.setBrush(list_of_color_rgb[i])
                    painter.setPen(QColor(0, 0, 0, 0))
                    painter.drawRect(rect)

        except FileNotFoundError:
            QCalendarWidget.paintCell(self, painter, rect, date)
            print("Файл с итоговой информацией пуст или отсутствует")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyCalendar()
    w.resize(400, 400)
    w.show()
    app.exec()
