from mymapapi import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
 
W = 400
H = 500
dMenu = 110
m = 10 #отступ
map_w, map_h = W -2 * m, H - dMenu - 2 * m


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setGeometry(100, 100, W, H)
        self.setWindowTitle('Карта')

        self.file_map = "one.png" #имя файла с картой
        self.mas = 8 #текущий масштаб
        self.type_map = "map"
        self.mode = False #карта еще не отображена
        self.lat = "55.7507" # координаты центра карты
        self.lon = "55.7507"
        self.map_label = None
         
        self.label = QLabel(self)
        self.label.setText("Введите координаты центра карты или название объекта:")
        self.label.move(m, 10)
 
        self.lat_input = QLineEdit(self)
        self.lat_input.resize(80,25)
        self.lat_input.move(m, 30)
        self.lat_input.setText("55.7507")
        self.lon_input = QLineEdit(self)
        self.lon_input.resize(80,25)
        self.lon_input.move(100, 30)
        self.lon_input.setText("37.6256")
        #выпадающий список
        self.combo = QComboBox(self)
        self.combo.resize(90, 25)
        self.combo.addItems(["схема", "спутник", 'гибрид'])
        self.combo.move(W // 2 - 10, 30)
        self.combo.activated[str].connect(self.onActivated)
    
        self.btn = QPushButton('Отобразить', self)
        self.btn.resize(W // 4, 25)
        self.btn.move(W // 4 * 3 - 10, 30)
        self.btn.clicked.connect(self.show_map_file)
        #строка поиска
        self.search_input = QLineEdit(self)
        self.search_input.resize(W // 4 * 3 - 20,25)
        self.search_input.move(m, 60)
        self.search_input.textChanged[str].connect(self.onChanged)
        self.search_btn = QPushButton('Искать', self)
        self.search_btn.resize(W // 5 - 30, 25)
        self.search_btn.move(W // 4 * 3 - 10, 60)
        self.search_btn.clicked.connect(self.search_address)
        self.search_btn.setDisabled(True)
        self.btnc = QPushButton('x', self)
        self.btnc.resize(25, 25)
        self.btnc.move(W - 40, 60)
        self.btnc.clicked.connect(self.search_clear)
        self.btnc.setDisabled(True)        
        
        self.pixmap = QPixmap(self.file_map)
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setGeometry(m , m + dMenu, map_w, map_h)
        self.lbl.move(m, m + dMenu)
       
        self.btnp = QPushButton('+', self)
        self.btnp.resize(25, 25)
        self.btnp.move(m, m + dMenu)
        self.btnp.clicked.connect(self.mas_plus)
        self.btnp.setDisabled(True)

        self.btnm = QPushButton('-', self)
        self.btnm.resize(25, 25)
        self.btnm.move(m + 25, m + dMenu)
        self.btnm.clicked.connect(self.mas_minus)
        self.btnm.setDisabled(True)
        
        self.label_address = QLabel(self)
        self.label_address.setText(" "*200)
        self.label_address.move(m, 95)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.mas_plus()
        if event.key() == Qt.Key_PageDown:
            self.mas_minus()       
        if event.key() == Qt.Key_Up:
            dy = 180 / 2 ** (self.mas) * (map_h / 256)
            lat = float(self.lat_input.text())
            if lat < (90 - dy):
                lat += dy    
            self.lat_input.setText(str(lat)) 
            self.show_map_file()
        if event.key() == Qt.Key_Down:
            dy = 180 / 2 ** (self.mas) * (map_h / 256)
            lat = float(self.lat_input.text())
            if lat > (-90 + dy):
                lat -= dy
            self.lat_input.setText(str(lat)) 
            self.show_map_file()  
            
        if event.key() == Qt.Key_Left:
            dx = 360 / 2 ** (self.mas - 8) * (map_h / 256)
            lat = float(self.lat_input.text())
            if lat < (90 - dy):
                lat += dx
            self.lat_input.setText(str(lat)) 
            self.show_map_file()
        if event.key() == Qt.Key_Right:
            dx = 360 / 2 **(self.mas - 8) * (map_h / 256)
            lat = float(self.lat_input.text())
            if lat > (-90 + dy):
                lat -= dx
            self.lat_input.setText(str(lat)) 
            self.show_map_file()          
        

    def onChanged(self, text):
        if text:
            self.search_btn.setDisabled(False)
            self.btnc.setDisabled(False)

    def onActivated(self, text):
        d = {"спутник":"sat", "схема":"map", 'гибрид':'sat,skl'}
        if text in d:
            self.type_map = d[text]
        self.show_map_file()
 
    def search_address(self):
        address = self.search_input.text()
        lon, lat, address = get_coordinates(address)
        self.lon_input.setText(str(lon))
        self.lat_input.setText(str(lat))
        self.label_address.setText(str(address))
        self.map_label = 'flag'
        self.show_map_file()

    def show_map_file(self):
        # Показать карту
        self.btnp.setDisabled(False)
        self.btnm.setDisabled(False)
        lon = self.lon_input.text()
        lat = self.lat_input.text()
        
        map_locations = "ll=" + ",".join([lon,lat])# + "&spn=1.0,1.0"
                
        map_param = "z={0}&size={1},{2}".format(str(self.mas),
                                                str(map_w),
                                                str(map_h))
        if self.map_label != None:
            map_param += '&pt={0},{1},{2}'.format(lon, lat, self.map_label)
        f_name = get_file_map(map_locations, self.type_map, map_param)
        if f_name:
            self.file_map = f_name
        
        self.pixmap.load(self.file_map)
        self.lbl.setPixmap(self.pixmap)
        
    def mas_minus(self):
        if self.mas > 0:
            self.mas = self.mas - 1
        self.show_map_file()

    def mas_plus(self):
        if self.mas < 17:
            self.mas = self.mas + 1
        self.show_map_file()
        
    def search_clear(self):
        self.search_input.setText('')
        self.label_address.setText(" "*200)
        self.map_label = None
        self.search_btn.setDisabled(True)
        self.btnc.setDisabled(True)        
        self.show_map_file()

    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
