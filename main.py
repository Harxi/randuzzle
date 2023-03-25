import os, random, sys

screenX, screenY = os.get_terminal_size()
command = {"linux": "clear", "win32": "cls"}[sys.platform]

### CONFIGS ###
#### Менять значение после =
#### Размеры карты (x, y) менять цифры
#### В управление и в стиле менять символы только те которые находятся в кавычках ("")
x, y = 30, 15 # РАЗМЕР КАРТЫ
top = "w" # Кнопка идти вверх
left = "a" # Кнопка идти влево
bottom = "s" # Кнопка идти вниз
right = "d" # Кнопка идти вправо
debug = False
### END ###

### STYLE ###
background = "." # То что будет на заднем фоне
player = "@" # Как вы отображаетесь
line = "-" # Указатели на вас, если надо убрать установите тоже значение что и на заднем фоне, ту же самую махинацию можно проводить с другими вещами, к примеру игроком фруктом
fruit = "+" # Фрукт
### END ###

### CHECKERS ###

if x > screenX:
	print("Возникла ошибка, установленные размеры превышают размер консоли, расширьте консоль чтобы это избежать (К примеру открыть ее в полно экранноом размере)")
	exit(-1)

if (x < 0) or (y < 0):
	print("Возникла ошибка, установленный размер не предусмотрен консолью, расширьте консоль чтобы это исправить измените размер консли на положительный")
	exit(-1)
	
### END ###

class Controller:
	def __init__(self, top: str, left: str, bottom: str, right: str):
		self.top, self.left, self.bottom, self.right = top, left, bottom, right

class Player:
	def __init__(self, x: int, y: int, speed: int, controller: Controller):
		self.x, self.y = x, y
		self.speed = speed
		self.controller: Controller = controller

class Theme:
	def __init__(self, line: str, player: str, background: str, fruit: str):
		self.line, self.player, self.background, self.fruit = line, player, background, fruit

class Fruit:
	def __init__(self, x, y):
		self.x, self.y = x, y

class Map:
	def __init__(self, x: int, y: int, theme: Theme, player: Player, fruit: Fruit, debug: bool):
		self.x, self.y = x, y
		self.fruit = fruit
		self.theme: Theme = theme
		self.player: Player = player
		self.debug: bool = debug
	
	def render(self) -> None:
		if self.debug:
			print(f"""MAP:
  X: {self.x}
  Y: {self.y}
PLAYER:
 bX: {self.player.x}
 Y: {self.player.y}
 SPEED: {self.player.speed}
CONTROLLER:
  TOP: {self.player.controller.top}
  LEFT: {self.player.controller.left}
  BOTTOM: {self.player.controller.bottom}
  RIGHT: {self.player.controller.right}
THEME:
  LINE: {self.theme.line}
  PLAYER: {self.theme.player}
  BACKGROUND: {self.theme.background}
  FRUIT: {self.theme.fruit}
FRUIT:
  X: {self.fruit.x}
  Y: {self.fruit.y}""")
		for y in range(self.y+1):
			for x in range(self.x+1):
				print(self.theme.player if (y == self.player.y) and (x == self.player.x) else self.theme.fruit if (y == self.fruit.y) and (x == self.fruit.x) else self.theme.background if (y != self.player.y) and x != self.player.x else self.theme.line, end='')
			print()
	
	def check(self) -> None:
		if self.player.x < 0: self.player.x = 0
		if self.player.x > self.x: self.player.x = self.x
		if self.player.y < 0: self.player.y = 0
		if self.player.y > self.y: self.player.y = self.y
		if (self.player.x, self.player.y) == (self.fruit.x, self.fruit.y):
			if self.player.speed >= max(self.x, self.y)-1:
				return
			self.player.speed += 1
			self.fruit.x, self.fruit.y = random.randint(0, self.x), random.randint(0, self.y)
	
	def move(self, dir: str) -> None:
		for dir in dir:
			for _ in range(random.randint(1, self.player.speed)):
				os.system(move)
				if dir == self.player.controller.top: self.player.y -= 1
				if dir == self.player.controller.bottom: self.player.y += 1
				if dir == self.player.controller.left: self.player.x -= 1
				if dir == self.player.controller.right: self.player.x += 1
				self.check()
				self.render()

map = Map(x, y, Theme(line, player, background, fruit), Player(x//2, y//2, 1, Controller(top, left, bottom, right)), Fruit(random.randint(0, x), random.randint(0, y)), debug)

while True:
	map.render()
	print(f"""ВВЕРХ, ВНИЗ: {map.player.controller.top}, {map.player.controller.bottom}
ВЛЕВО, ВПРАВО: {map.player.controller.left}, {map.player.controller.right}
ВАША СКОРОСТЬ: {map.player.speed}""")
	dir = input("Выберите сторону: ")
	map.move(dir)
	os.system(command)
