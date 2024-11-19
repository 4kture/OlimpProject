from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication([])

browser = QWebEngineView()
browser.setUrl(QUrl("http://127.0.0.1:5000/"))
browser.show()

app.exec_()