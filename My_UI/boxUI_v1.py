import sys
from PyQt5 import QtWidgets, QtCore
import time
import serial


serial_port = serial.Serial("COM4", 9600)

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Управление микроконтроллером")
        self.setGeometry(50, 50, 550, 400)
        self.outputs = []
        self.output_labels = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"]
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)
        self.sent_strings = []
        self.recieved_strings = []
        for i in range(4):
            for j in range(4):
                output_var = QtWidgets.QComboBox()
                output_var.addItems(["0", "1", "2", "3", "4", "5", "6", "7", "GND", "10MOm"])
                output_var.setCurrentText("0")
                self.outputs.append(output_var)
                label = QtWidgets.QLabel(self.output_labels[i*4+j])
                grid_layout.addWidget(label, i, j*2, 1, 1)
                grid_layout.addWidget(output_var, i, j*2+1, 1, 1)
        gnd_button = QtWidgets.QPushButton("GND")
        gnd_button.clicked.connect(self.send_gnd)
        grid_layout.addWidget(gnd_button, 4, 0, 1, 1)
        mom_button = QtWidgets.QPushButton("MOm")
        mom_button.clicked.connect(self.send_resistor)
        grid_layout.addWidget(mom_button, 4, 1, 1, 1)
        send_button = QtWidgets.QPushButton("Отправить")
        send_button.clicked.connect(self.send_string)
        grid_layout.addWidget(send_button, 5, 0, 1, 4)
        self.sent_label = QtWidgets.QLabel()
        grid_layout.addWidget(self.sent_label, 6, 0, 1, 2)
        self.response_label = QtWidgets.QLabel()
        grid_layout.addWidget(self.response_label, 6, 4, 1, 2)
        
        
        serial_port.write("init\n".encode())

        switch_button = QtWidgets.QPushButton("Переключиться на другое окно")
        switch_button.clicked.connect(self.switch_window)
        grid_layout.addWidget(switch_button, 7, 0, 1, 4)

    def __del__(self):
        serial_port.close()
        
    def read_all():
        serial_port.read_all()

    def close_port(self):
        serial_port.close()


    def send_string(self):
        selected_outputs = []
        for output in self.outputs:
            selected_outputs.append(output.currentText())
        selected_outputs = [output if output != "GND" else '9' for output in selected_outputs]
        selected_outputs = [output if output != "10MOm" else '8' for output in selected_outputs]
        
        string=""
        for out in selected_outputs:
            string += out
        string = string[:]
        
        self.send_resistor()
        time.sleep(1)
        print(string,end="\n")
        self.sent_strings.append(string)
        if len(self.sent_strings) > 3:
            self.sent_strings = self.sent_strings[-3:]
        self.sent_label.setText("\n".join(self.sent_strings))
        string += "\n"
        serial_port.write(("+" +string).encode())
        self.read_str()
        
         
        # time.sleep(1)
        #self.serial_port.flush()  # Очистка буфера порта
        # self.serial_port.write("\n".encode())
        # self.sent_label.setText(string)
        # response1 = self.serial_port.readline().decode()
        # self.response_label.setText(response1)
        
        
    def read_str(self):
        # time.sleep(1)
        
        # self.recieved_strings.append("Заглущка")
        # if len(self.recieved_strings) > 3:
        #     self.recieved_strings = self.recieved_strings[-3:]
        # self.response_label.setText("\n".join(self.recieved_strings))
        time.sleep(1)
        
        while True:
            if serial_port.in_waiting > 0: 
               # print('here1')# Проверяем, доступны ли данные для чтения
                ans =serial_port.readline().decode().strip()  # Читаем данные из порта
                print("Прочитано из порта:", ans)
                self.recieved_strings.append(ans)
                if len(self.recieved_strings) > 3:
                    self.recieved_strings = self.recieved_strings[-3:]
                self.response_label.setText("\n".join(self.recieved_strings))
                break
            else:
               # print("waiting")
                time.sleep(1)
                
       

    def send_gnd(self):
        serial_port.write("GND\n".encode())
        # response = self.serial_port.readline().decode()
        # self.response_label.setText(response)
        # self.sent_label.setText("GND")
        print("GND sent")
        
        self.sent_strings.append("GND sent")
        if len(self.sent_strings) > 3:
            self.sent_strings = self.sent_strings[-3:]
        self.sent_label.setText("\n".join(self.sent_strings)) 
        
        self.read_str()
        
    def send_resistor(self):
        serial_port.write("MOm\n".encode())
        # response = self.serial_port.readline().decode()
        # self.response_label.setText(response)
        # self.sent_label.setText("MOm")
        print("MOm sent")
        
        self.sent_strings.append("MOm sent")
        if len(self.sent_strings) > 3:
            self.sent_strings = self.sent_strings[-3:]
        self.sent_label.setText("\n".join(self.sent_strings)) 
        
        self.read_str()

    def switch_window(self):
        self.new_window = NewWindow()
        self.new_window.return_signal.connect(self.return_to_main_window)
        self.new_window.return_button.clicked.connect(self.return_to_main_window)
        self.new_window.show()
        self.hide()

    def return_to_main_window(self):
        self.new_window.close()
        self.show()

class NewWindow(QtWidgets.QWidget):
    return_signal = QtCore.pyqtSignal()
    def __init__(self):
        super(NewWindow, self).__init__()
        
        grid = QtWidgets.QGridLayout(self)
        self.setLayout(grid)
        self.setGeometry(50, 50, 500, 500)

        # Создание 16 блоков
        self.blocks = []
        self.output_label = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"]
        for i in range(4):
            for j in range(4):
                block = QtWidgets.QWidget()
                block_layout = QtWidgets.QGridLayout()
                block.setLayout(block_layout)
                self.blocks.append([])
                # Создание 9 маленьких кнопок в каждом блоке
                o = 1
                for k in range(3):
                    for l in range(3):
                        if k==1 and l == 1:
                            text = self.output_label[i*4+j] + " GND"
                        elif o == 8:
                            text = "10MOm"
                        else:
                            text = f"{o}"
                            o+=1
                            
                        small_button = QtWidgets.QPushButton(text)
                        small_button.setCheckable(True)
                        self.blocks[i*4 +j].append(small_button)
                        block_layout.addWidget(small_button, k, l)

                grid.addWidget(block, i, j)
                
                
                
        self.return_button = QtWidgets.QPushButton("Вернуться на предыдущее окно")
        grid.addWidget(self.return_button,8, 0, 1, 4) # номер строки, номер столбца, количетсво занимаемых строк, колво столбцоы
        
        send_button = QtWidgets.QPushButton("Отправить")
        send_button.clicked.connect(self.send_string)
        grid.addWidget(send_button, 5, 0, 1, 4)
        
        self.gnd_button = QtWidgets.QPushButton("GND")
        self.gnd_button.clicked.connect(self.send_gnd)
        grid.addWidget(self.gnd_button,4,0,1,1)

        self.mom_button = QtWidgets.QPushButton("10MOm")
        self.mom_button.clicked.connect(self.send_resistor)
        grid.addWidget(self.mom_button,4,1,1,1)
        
        self.sent_strings = []
        self.sent_label = QtWidgets.QLabel()
        grid.addWidget(self.sent_label, 4, 2, 1,1)
        
        self.recieved_strings = []
        self.response_label = QtWidgets.QLabel()
        grid.addWidget(self.response_label, 4, 3, 1, 1)
       
    def send_gnd(self):
        serial_port.write("GND\n".encode())
        # response = self.serial_port.readline().decode()
        # self.response_label.setText(response)
        # self.sent_label.setText("GND")
        print("GND sent")
        self.sent_strings.append("GND sent")
        if len(self.sent_strings) > 3:
            self.sent_strings = self.sent_strings[-3:]
        self.sent_label.setText("\n".join(self.sent_strings)) 
        self.read_str()
        
    def send_resistor(self):
        serial_port.write("MOm\n".encode())
        # response = self.serial_port.readline().decode()
        # self.response_label.setText(response)
        # self.sent_label.setText("MOm")
        print("MOm sent")
        self.sent_strings.append("MOm sent")
        if len(self.sent_strings) > 3:
            self.sent_strings = self.sent_strings[-3:]
        self.sent_label.setText("\n".join(self.sent_strings)) 
        
        self.read_str()   
                        
    def read_str(self):
        # time.sleep(1)
        # self.recieved_strings.append("Заглущка")
        # if len(self.recieved_strings) > 3:
        #     self.recieved_strings = self.recieved_strings[-3:]
        # self.response_label.setText("\n".join(self.recieved_strings))
        
        time.sleep(1)
        while True:
            if serial_port.in_waiting > 0:
               # print('here2')# Проверяем, доступны ли данные для чтения
                ans = serial_port.readline().decode().strip()  # Читаем данные из порта
                print("Прочитано из порта:", ans)
                self.recieved_strings.append(ans)
                if len(self.recieved_strings) > 3:
                    self.recieved_strings = self.recieved_strings[-3:]
                self.response_label.setText("\n".join(self.recieved_strings))
                break
            else:
                #print("waiting")
                time.sleep(1)
       

    
    def send_string(self):
        
        self.send_resistor()
        string = "MULTY*"
        
        for block in self.blocks:
            arr = []
            for button in block:
                if button.isChecked():
                    arr.append("1")
                else:
                    arr.append("0")
            gnd = arr.pop(4)
            arr.append(gnd)
            string += "".join(arr)
        print(string)
        
        serial_port.flush()  # Очистка буфера порта
        string +='\n'
        serial_port.write(string.encode())
        self.sent_strings.append("Multy sent")
        if len(self.sent_strings) > 3:
            self.sent_strings = self.sent_strings[-3:]
        self.sent_label.setText("\n".join(self.sent_strings))
        self.read_str()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())