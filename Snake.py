from tkinter import *
import random
#aeraeae
WIDTH = 800# ширина экрана
HEIGHT = 600# высота экрана
SEG_SIZE = 20# Размер сегмента змейки
IN_GAME = True# Переменная отвечающая за состояние игры
def create_block():#Создает блок в случайной позиции на карте
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(posx, posy, posx+SEG_SIZE, posy+SEG_SIZE, fill="red")# блок это кружочек красного цвета
def main():# Управление игровым процессом
    global IN_GAME
    if IN_GAME:
        s.move()# Двигаем змейку
        head_coords = c.coords(s.segments[-1].instance)# Определяем координаты головы
        x1, y1, x2, y2 = head_coords
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:# Столкновение с границами экрана
            IN_GAME = False
        elif head_coords == c.coords(BLOCK):# Поедание яблок
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        else:# Самоедство
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
        root.after(100, main)
    else:# Если не в игре выводим сообщение о проигрыше
        c.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER!", font="Arial 20", fill="red")
class Segment(object):# Один скгмент змейки
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="white")
class Snake(object):# Простые классы змеи
    def __init__(self, segments):
        self.segments = segments
        self.mapping = {"Down": (0, 1), "Right": (1, 0), "Up": (0, -1), "Left": (-1, 0)}# список доступных направлений движения змейки
        self.vector = self.mapping["Right"]# изначально змейка двигается вправо
    def move(self):#Двигает змейку в заданном направлении 
        for index in range(len(self.segments)-1):# перебираем все сегменты кроме первого
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)# задаем каждому сегменту позицию сегмента стоящего после него
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)# получаем координаты сегмента перед "головой"
        c.coords(self.segments[-1].instance,# помещаем "голову" в направлении указанном в векторе движения
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)
    def add_segment(self):#Добавляет сегмент змейке
        last_seg = c.coords(self.segments[0].instance)# определяем последний сегмент
        x = last_seg[2] - SEG_SIZE# определяем координаты куда поставить следующий сегмент
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))# добавляем змейке еще один сегмент в заданных координатах
    def change_direction(self, event):# Изменяет направление движения змейки
        if event.keysym in self.mapping:# event передаст нам символ нажатой клавиши
            self.vector = self.mapping[event.keysym]# и если эта клавиша в доступных направлениях изменяем направление    
root = Tk()# Создаем окно
root.title("PythonicWay Snake")# Устанавливаем название окна
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.grid()#создаем экземпляр класса Canvas (его мы еще будем использовать) и заливаем все зеленым цветом
c.focus_set()# Наводим фокус на Canvas, чтобы мы могли ловить нажатия клавиш
segments = [Segment(SEG_SIZE, SEG_SIZE),Segment(SEG_SIZE*2, SEG_SIZE),Segment(SEG_SIZE*3, SEG_SIZE)]# создаем набор сегментов
s = Snake(segments)# собственно змейка
c.bind("<KeyPress>", s.change_direction)
create_block()
main()
root.mainloop()# Запускаем окно
