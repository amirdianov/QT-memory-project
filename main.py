








if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec())


class ClickableLabel(QLabel):
    def mousePressEvent(self, e):
        print(1)