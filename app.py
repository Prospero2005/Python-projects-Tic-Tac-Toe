import sys
import random
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox


class TicTacToe(QMainWindow):

    def __init__(self):
        super(TicTacToe, self).__init__()
        uic.loadUi('form.ui', self)
        self.rb_x.toggled.connect(self.check_xo_symbol)
        self.rb_o.toggled.connect(self.check_xo_symbol)
        for button in self.findChildren(QPushButton):
            button.clicked.connect(self.xo_click)
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Результат игры")
        self.init_vars()

    def check_xo_symbol(self):
        rb = self.sender()
        if rb.isChecked():
            self.user_symbol = rb.text()
            self.user_color = rb.toolTip()
        if not rb.isChecked():
            self.comp_symbol = rb.text()
            self.comp_color = rb.toolTip()
        self.lbl_status.setText(f"Пользователь играет '{self.user_symbol}'")

    def update_field(self, button, pos, symbol, color):
        button.setEnabled(False)
        button.setText(symbol)
        button.setStyleSheet(f"QPushButton {{ color: {color} }}")
        self.XO_dict[pos] = symbol
        self.free_fields.pop(self.free_fields.index(pos))

    def check_combo(self, dict, flag):
        xo_string = "".join(dict.values())
        combo1 = ["".join([xo_string[i] for i in range(j * 3, (j * 3) + 3)]) for j in range(3)]
        combo2 = ["".join([xo_string[i] for i in range(j, 8 + j, 3)]) for j in range(3)]
        combo3 = ["".join([xo_string[i] for i in [0 + j, 4, 8 - j]]) for j in range(0, 3, 2)]
        comp_win = (self.comp_symbol*3 in combo1) or (self.comp_symbol*3 in combo2) or (self.comp_symbol*3 in combo3)
        user_win = (self.user_symbol*3 in combo1) or (self.user_symbol*3 in combo2) or (self.user_symbol*3 in combo3)
        if flag:
            if user_win:
                self.msg.setText("Победа пользователя!")
                self.msg.exec()
                return True
            elif comp_win:
                self.msg.setText("Победа компьютера!")
                self.msg.exec()
                return True
            elif not comp_win and not user_win and xo_string.count("_") == 0:
                self.msg.setText("Ничья!")
                self.msg.exec()
                return True
            else:
                return False
        else:
            return comp_win or user_win


    def comp_choice(self):
        info = None
        for i in range(len(self.free_fields)):
            copy_dict = self.XO_dict.copy()
            copy_dict[self.free_fields[i]] = self.user_symbol
            if self.check_combo(copy_dict, False):
                info = self.free_fields[i]
                break
        if info == None:
            info = random.choice(self.free_fields)
        pos = f"{info[0]} {info[1]}"
        for button in self.findChildren(QPushButton):
            if button.text() != "Start":
                if button.toolTip() ==  pos:
                    self.update_field(button, info, self.comp_symbol, self.comp_color)
        self.gb_xo.setEnabled(True)
        if self.check_combo(self.XO_dict, True):
            self.init_vars()

    def xo_click(self):
        btn = self.sender()
        self.gb_xo.setEnabled(False)
        if btn.text() != "Start":
            coords = tuple(map(int, btn.toolTip().split(' ')))
            self.update_field(btn, coords, self.user_symbol, self.user_color)
            if self.check_combo(self.XO_dict, True):
                self.init_vars()
                return
            self.comp_choice()
        else:
            self.start_app()

    def start_app(self):
        for button in self.findChildren(QPushButton):
            if button.text() != "Start":
                button.setText("_")
        self.gb_main.setEnabled(False)
        self.gb_xo.setEnabled(True)
        if random.randint(0, 1):
            self.gb_xo.setEnabled(False)
            self.comp_choice()

    def init_vars(self):
        self.rb_x.setChecked(True)
        self.gb_main.setEnabled(True)
        self.gb_xo.setEnabled(False)
        for button in self.findChildren(QPushButton):
            if button.text() != "Start":
                button.setText("_")
                button.setEnabled(True)
                button.setStyleSheet(f"QPushButton {{ color: #000000 }}")
        self.user_symbol = self.rb_x.text()
        self.user_color = "#0000FF"
        self.comp_symbol = self.rb_o.text()
        self.comp_color = "#FF0000"
        self.XO_list = [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
        self.XO_dict = {k: "_" for k in self.XO_list}
        self.free_fields = [k for k, v in self.XO_dict.items() if v != "X" and v != "O"]

        self.lbl_status.setText(f"Пользователь играет '{self.user_symbol}'")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
