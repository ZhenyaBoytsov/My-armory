from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

g = -1

class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        damp = 0.5 #empiric
        self.y += -self.vy
        self.x += self.vx
        self.vy += g
        self.set_coords()
        if self.y - self.vy > 600 - self.r:
            self.vy = -damp*self.vy
            self.y = 600 - self.r
            self.live -= 5
        if self.y - self.vy < self.r:
            self.vy = -damp*self.vy
            self.y = self.r
            self.live -= 5
        if self.x > 800 - self.r:
            self.vx = -damp*self.vx
            self.x = 800 - self.r
            self.live -= 5
        if self.x < self.r:
            self.vx = -damp*self.vx
            self.x = self.r
            self.live -= 5
        if self.live <= 0:
            balls.pop(balls.index(self))
            canv.delete(self.id)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return ((obj.x-self.x)*(obj.x-self.x) + (obj.y-self.y)*(obj.y-self.y) <= (obj.r+self.r)*(obj.r+self.r))


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

id_points = canv.create_text(30,30,text = 0,font = '28')
sum_points = 0

class target():
    def __init__(self):
        self.points = 0
        self.live = 1 #Что значит комментарий снизу? Не совсем понял формулировку проблемы.
        # FIXME: don't work!!! How to call this functions when object is created?
        self.id = canv.create_oval(0,0,0,0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        global sum_points
        sum_points += points
        canv.itemconfig(id_points, text=sum_points)


t = [target(), target()]
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []


def new_game(event=''):
    global gun, t, screen1, balls, bullet, sum_points
    for target in t:
        target.new_target()
    sum_points = 0
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    canv.itemconfig(id_points, text=sum_points)

    z = 0.03
    for target in t:
        target.live = 1
    while sum(target.live for target in t) or balls:
        for b in balls:
            b.move()
            for target in t:
                if b.hittest(target) and target.live:
                    target.live = 0
                    target.hit()
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.bind('<Button-1>', '')
    canv.bind('<ButtonRelease-1>', '')
    canv.delete(gun)

while True:
    new_game()
    time.sleep(0.750)
