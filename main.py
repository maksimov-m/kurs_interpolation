#подключаем нужные библиотеки
import csv
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#наш класс с окном и функциями
class window:
    #в этой функции мы создаем наше окно и размещаем в нем наши виджеты
    def __init__(self, width, height, title="Algoritm"):
        #наше окно и размер
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        #массивы начальных координат
        self.x = []
        self.y = []
        #полотно с графиком
        frameUp = Frame(self.root, relief=SUNKEN, height=10)
        frameUp.pack(side=TOP, fill=X)
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='white')
        self.ax = fig.add_subplot(111)
        self.canvasAgg = FigureCanvasTkAgg(fig, master=self.root)
        self.canvasAgg.draw()
        canvas = self.canvasAgg.get_tk_widget()
        canvas.pack(fill=BOTH, expand=1)

        #текстовое окно, куда выводятся координаты
        self.tx = Text(self.root, width=40, height=6, font='14')
        self.scr = Scrollbar(self.root, command=self.tx.yview)
        self.tx.configure(yscrollcommand=self.scr.set)
        self.tx.pack()
        self.scr.pack()

        #кнопки для счтения и рассчета
        self.btn_res = Button(self.root, text="Read file", command=self.read)
        self.btn_res.pack()

        self.btn_res = Button(self.root, text="Draw", command=self.draw)
        self.btn_res.pack()


    #рисуем наш график по точкам и полученным результатам
    def draw(self):
        #полчаем наш многочлен
        new_pol = self.create_Newton_polynomial(self.x, self.y)
        y_res = []
        for i in self.x:
            y_res.append(new_pol(i))
        #записали данные в файл
        self.write(self.x, y_res)

        self.ax.clear()  # очистить графическую область
        self.ax.plot(self.x, self.y, 'ro')
        self.ax.plot(self.x, y_res, 'b')
        self.ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
        self.canvasAgg.draw()  # перерисовать "составной" холст


    def divided_differences(self, x_values, y_values, k): #k - значение, в котором вычислить
        result = 0
        for j in range(k + 1): #находим произведение по формуле
            mul = 1
            for i in range(k+1):
                if i != j:
                    mul *= x_values[j] - x_values[i] #вычисляем наше произведение от i до k
            result += y_values[j]/mul #вычисляем разделенную разность k-го порядка
        return result

    def create_Newton_polynomial(self, x_values, y_values):#функция вернет интерполиционный полином ньютона
        div_diff = [] #список разделенных разностей
        for i in range(1, len(x_values)):#количество разделенных разностей от 1 до количества точек
            div_diff.append(self.divided_differences(x_values, y_values, i)) #храним разделенный разности
        def newton_polynomial(x): #вложенная функция, которая вернет полином ньютона
            result = y_values[0] #это игрек нулевое
            for k in range(1, len(y_values)):#вычисляем умножение по формуле
                mul = 1
                for j in range(k):
                    mul *= (x-x_values[j])
                result += div_diff[k-1]*mul #умножаем разделенную разность на произведение
            return result
        print(div_diff)
        return newton_polynomial #возвращаем наш полином

    # запись результата в файл
    def write(self, x, y_res):

        w_y_res = []

        for x2,y2 in zip(x, y_res):
            w_y_res.append((x2, y2))


        File2 = open('data_res.csv', 'w')
        with File2:
            writer = csv.writer(File2)
            writer.writerows(w_y_res)

    #чтение данных из файла
    def read(self):
        self.tx.delete(1.0, END)
        self.x = []
        self.y = []
        count = 1
        try:
            with open("data.csv", encoding='utf-8') as r_file:
                # Создаем объект reader, указываем символ-разделитель ","
                file_reader = csv.reader(r_file, delimiter=",")

                count = 1
                # Считывание данных из CSV файла
                self.tx.insert(float(count), f'(X, Y)\n')
                count += 1
                for row in file_reader:
                    # Вывод строк

                    #print(row)
                    if len(row) != 0:
                        self.tx.insert(float(count), f'({row[0]}, {row[1]})\n')
                        count += 1
                        self.x.append(float(row[0]))
                        self.y.append(float(row[1]))
        except:
            self.tx.delete(1.0, END)
            self.tx.insert(float(0), f'FATAL ERROR!!! RETRY AGAIN!!!')

    #запуск программы
    def run(self):
        self.root.mainloop()


a = window(700, 700)

a.run()