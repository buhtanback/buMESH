from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QTimer, QTime, pyqtSignal
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer
import sqlite3
import datetime

#choBD = sqlite3.connect('choinka_data.db')

app = QtWidgets.QApplication([])
ui = uic.loadUi("keeMASH.ui")
ui.setWindowTitle("keeMASH")

serial = QSerialPort()
serial.setBaudRate (115200)
portList = []
ports = QSerialPortInfo().availablePorts()

for port in ports:
    portList.append(port.portName())
ui.comboBox.addItems(portList)

#def clear_cho_table():
    #cursor = choBD.cursor()
    #cursor.execute("DELETE FROM humidity")

    #choBD.commit()
    #cursor.close()

#def get_cho():
    #cursor = choBD.cursor()
    #cursor.execute("SELECT * FROM humidity ORDER BY date DESC LIMIT 8")
    #results = cursor.fetchall()
    #cursor.close()
    #return results

#def update_choT():

    #first_measurements = get_cho()
    #display_text = ""
    #for date, humidity in first_measurements:
        #display_text += f"{date} choinka {humidity}\n"

    #ui.choT.setText(display_text)

#def add_choinka_db(x):
    #choBD = sqlite3.connect('choinka_data.db')
    #c = choBD.cursor()
    #c.execute("INSERT INTO humidity (date, humidity_level) VALUES (?, ?)",
     #         (datetime.datetime.now().strftime("%m-%d %H:%M"), x))
    #choBD.commit()
    #choBD.close()

def onOpen():
    try:
        serial.setPortName(ui.comboBox.currentText())
        if serial.open(QIODevice.ReadWrite):
            print(f"Порт {serial.portName()} відкрито")
            ui.openB.setStyleSheet("background-color: green; color: white;")  # Оновити індикатор підключення
        else:
            print(f"Не вдалося відкрити порт {serial.portName()}: {serial.errorString()}")
            ui.openB.setStyleSheet("background-color: red; color: white;")  # Відображення помилки
    except Exception as e:
        print(f"Виникла помилка при відкритті порту: {e}")




def feedback():
    commands = [("garland_echo", 1300), ("red_led_echo", 1300), ("sens_echo", 1300), ("choinka", 1300), ("bedside_echo", 1300), ("echo_turb", 1300)]
    for i, (command, delay) in enumerate(commands):
        QTimer.singleShot(sum(item[1] for item in commands[:i+1]), lambda cmd=command: sendi(cmd))
    print("feeeeeeeeeeee")

def onClose():
    serial.close()
    #clear_cho_table()

def sendi(datic):
    if serial.isOpen():
        bytes_written = serial.write(datic.encode('utf-8'))
        if bytes_written == -1:
            print("Помилка запису даних у серійний порт")
    else:
        print("Серіальний порт не відкритий")


def set_col_ind (x, u, y):
    getattr(ui, x).setCurrentIndex(u)
    getattr(ui, x).setStyleSheet(f"background-color: {y}; color: white;")

def turboBox_change(index):
    sendi(f'14{index}')
def modBoxR_change(index):
    sendi(f'01_mode_{index}')
def colorBox_change(index):
    sendi(f'18{index}')
def watLBox_change(index):
    if index <= 9:
        sendi(f'19{index}')
    else: sendi(f'19M')
def briBoxR_change(index):
    if index <= 9:
        sendi(f'02_bri_{index}')
    else: sendi(f'02_bri_M')
def mod_change_fid(x):
    if x[:2] == '01':
        set_col_ind("modBoxR", int(x[-1]), "grey")

def mod_colorBox_fid(x):
    if x[:2] == '21':
        set_col_ind("colorBox", int(x[-1]), "grey")

def bri_change_fid(x):
    match x:
        case "020": set_col_ind("briBoxR", 0, "grey")
        case "0226": set_col_ind("briBoxR", 1, "grey")
        case "0251": set_col_ind("briBoxR", 2, "grey")
        case "0277": set_col_ind("briBoxR", 3, "grey")
        case "02102": set_col_ind("briBoxR", 4, "grey")
        case "02128": set_col_ind("briBoxR", 5, "grey")
        case "02153": set_col_ind("briBoxR", 6, "grey")
        case "02179": set_col_ind ("briBoxR", 7, "grey")
        case "02204": set_col_ind ("briBoxR", 8, "grey")
        case "02230": set_col_ind ("briBoxR", 9, "grey")
        case "02255": set_col_ind ("briBoxR", 10, "grey")

def watLBox_change_fid(x):
    match x:
        case "200": set_col_ind("watLBox", 0, "grey")
        case "2026": set_col_ind("watLBox", 1, "grey")
        case "2051": set_col_ind("watLBox", 2, "grey")
        case "2077": set_col_ind("watLBox", 3, "grey")
        case "20102": set_col_ind("watLBox", 4, "grey")
        case "20128": set_col_ind("watLBox", 5, "grey")
        case "20153": set_col_ind("watLBox", 6, "grey")
        case "20179": set_col_ind ("watLBox", 7, "grey")
        case "20204": set_col_ind ("watLBox", 8, "grey")
        case "20230": set_col_ind ("watLBox", 9, "grey")
        case "20255": set_col_ind ("watLBox", 10, "grey")

def reti():                                # тут можуть бути баги
    txt = "05" + ui.spedE.text()
    ui.spedE.clear()
    sendi(txt)
def send2mash():                                # тут можуть бути баги
    sendi(ui.sendL.text())
    ui.sendL.clear()


def onRead():
    try:
        rx = serial.readLine()
        rxs = str(rx, "utf-8").strip()
        data = rxs.split(",")
        if len(data) == 0:
            print("Отримано порожні дані")
            return

        print(data)

        watLBox_change_fid(data[0])
        mod_colorBox_fid(data[0])
        mod_change_fid(data[0])
        bri_change_fid(data[0])

    except Exception as e:
        print(f"Виникла помилка при читанні даних: {e}")

    if data[0] == 'hello':
        ui.openB.setStyleSheet("background-color: green; color: white;")
        feedback()

    if data[0] == 'pimpa':
        ui.pumpB.setStyleSheet("background-color: green; color: white;")
    #if data[0] == 'turbo1':
        #ui.turbo1B.setStyleSheet("background-color: black; color: white;")

    if data[0] == 'garland_on':
        ui.pushB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'garland_off':
        ui.pushB.setStyleSheet("background-color: black; color: white;")

    if data[0] == 'redled_on':
        ui.redB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'redled_off':
        ui.redB.setStyleSheet("background-color: black; color: white;")

    if data[0] == 'bedside_on':
        ui.bedLB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'bedside_off':
        ui.bedLB.setStyleSheet("background-color: black; color: white;")

    if data[0][:2] == '03':
        spF = data[0][2:]
        ui.lcdSp.display(spF)


    if data[0][:2] == '05':
        temp = data[0][2:]
        ui.lcdTemp.display(temp)
        ui.tempB.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '06':
        humi = data[0][2:]
        ui.lcdHumi.display(humi)
        ui.humiB.setStyleSheet("background-color: green; color: white;")



    if data[0][:2] == '22':  # Відображення CO2
        co2 = data[0][2:]
        if co2.isdigit():  # Перевірка, чи є значення числом
            ui.lcdCO2.setDigitCount(6)  # Встановлення кількості цифр
            ui.lcdCO2.display(int(co2))  # Використання lcdCO2
            ui.CO2.setStyleSheet("background-color: green; color: white;")  # Встановлення стилю кнопки CO2

    if data[0][:2] == '07':
        pressure = data[0][2:]
        pressure_value = float(pressure)  # Перетворення на дробове число
        ui.lcdpressure.setDigitCount(6)
        ui.lcdpressure.display(pressure_value)  # Використання значення тиску як аргумент
        ui.pressure.setStyleSheet("background-color: green; color: white;")  # Встановлення стилю кнопки


    if data[0][:2] == '28':
        soil = data[0][2:]
        if soil.isdigit():
            ui.lcdSoil.setDigitCount(6)
            ui.lcdSoil.display(int(soil))
            ui.soil.setStyleSheet("background-color: green; color: white;")




    watLBox_change_fid(data[0])
    mod_colorBox_fid(data[0])

    mod_change_fid(data[0])
    bri_change_fid(data[0])
#///////////////////////////////////////////////
def checkEvent_1():
    if ui.checkEvent_1.isChecked():
        print("Чекбокс встановлено")
    else:
        print("Чекбокс скасовано")
def checkEvent_2():
    if ui.checkEvent_2.isChecked():
        print("Чекбокс встановлено")
    else:
        print("Чекбокс скасовано")
def readT1():
    time = ui.timeEvent_1.time()
    #print("Час1:", time.toString("hh:mm:ss"))
def readT2():
    time = ui.timeEvent_2.time()
    #print("Час2:", time.toString("hh:mm:ss"))
def saveT1():
    saved_text = ui.lineEvent_1.text()
    sendi( saved_text)
    readT1()
def saveT2():
    saved_text = ui.lineEvent_2.text()
    sendi( saved_text)
    readT2()


#/////////////////////////////////////////////////////

class TimerWidget(QtWidgets.QWidget):
    timer1_timeout = QtCore.pyqtSignal()
    timer2_timeout = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.timer1_timeout.emit)

        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.timer2_timeout.emit)

        ui.timeEvent_1.timeChanged.connect(self.set_timer1)
        ui.timeEvent_2.timeChanged.connect(self.set_timer2)

        self.timer1_timeout.connect(saveT1)
        self.timer2_timeout.connect(saveT2)

        ui.checkEvent_1.stateChanged.connect(self.toggle_timer1)
        ui.checkEvent_2.stateChanged.connect(self.toggle_timer2)

    def set_timer1(self):
        if ui.checkEvent_1.isChecked():
            time = ui.timeEvent_1.time()
            self.timer1.setSingleShot(True)
            self.timer1.setInterval(QTime.currentTime().msecsTo(time))
            self.timer1.start()

    def set_timer2(self):
        if ui.checkEvent_2.isChecked():
            time = ui.timeEvent_2.time()
            self.timer2.setSingleShot(True)
            self.timer2.setInterval(QTime.currentTime().msecsTo(time))
            self.timer2.start()

    def toggle_timer1(self, state):
        if state == QtCore.Qt.Checked:
            self.set_timer1()
        else:
            self.timer1.stop()

    def toggle_timer2(self, state):
        if state == QtCore.Qt.Checked:
            self.set_timer2()
        else:
            self.timer2.stop()


timer_widget = TimerWidget()

###############
ui.colorBox.activated.connect(colorBox_change)
ui.watLBox.activated.connect(watLBox_change)

ui.modBoxR.activated.connect(modBoxR_change)
ui.briBoxR.activated.connect(briBoxR_change)

ui.turboBox.activated.connect(turboBox_change)

serial.readyRead.connect(onRead)

ui.upB.clicked.connect(feedback)

ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.bedLB.clicked.connect(lambda: sendi("bedside"))
ui.pushB.clicked.connect(lambda: sendi("garland"))
ui.redB.clicked.connect(lambda: sendi("power"))


ui.tempB.clicked.connect(lambda: sendi("temp_echo"))
ui.humiB.clicked.connect(lambda: sendi("humi_echo"))


ui.pumpB.clicked.connect(lambda: sendi("pomp"))
ui.flowB.clicked.connect(lambda: sendi("flow"))
ui.ionB.clicked.connect(lambda: sendi("ion"))
ui.huB.clicked.connect(lambda: sendi("huOn"))

#ui.choB.clicked.connect(lambda: sendi("choinka"))

ui.jajoB.clicked.connect(lambda: sendi("jajo"))

ui.speedBU.clicked.connect(lambda: sendi("redl_sp+"))
ui.speedBD.clicked.connect(lambda: sendi("redl_sp-"))

ui.spedE.returnPressed.connect(reti)
ui.sendL.returnPressed.connect(send2mash)

ui.show()
app.exec()