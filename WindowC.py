from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Combobox
from MathCore import *
from DrawModel import *


# Размеры экрана
HEIGHT = 600
WIDTH = 750
# Размеры холста
scrn_width = 300
scrn_height = 400


class Window:
	def __init__(self, width, height, title="MyWindow", resizable=(False, False), icon=None, x=None, y=None):
		# Конструктор класса окна
		self.root = Tk()
		self.root.title(title)
		# Центрирование окна, если не заданы x, y
		if not x:
			x = self.root.winfo_screenwidth() // 2 - width // 2
		if not y:
			y = self.root.winfo_screenheight() // 2 - height // 2

		self.root.geometry(f"{width}x{height}+{x}+{y}")
		self.root.resizable(resizable[0], resizable[1])
		if icon:
			self.root.iconbitmap(icon)

		# ---Фреймы---
		self.top_frame = Frame(self.root, background="#dddddd")
		self.picture_frame = Frame(self.root, background="#ffffaa")
		self.bottom_frame = Frame(self.root, background="#cccccc", borderwidth=5)

		# ---Поля-ввода---
		self.metal = Combobox(self.top_frame, values=("Zn", "Cu"),
							  state="readonly", width=17)
		self.anion = Combobox(self.top_frame, values=("SO4", "Cl2"),
							  state="readonly", width=17)
		self.culture = Combobox(self.top_frame, values=("Томаты", "Огурцы"),
								state="readonly", width=17)
		self.part = Combobox(self.top_frame, values=("Зелёная часть", "Корневая система", "Всё"),
							 state="readonly", width=17)
		self.concentrate = Spinbox(self.top_frame, values=(2, 3.9, 7.8, 15.6, 31.3, 62.5, 125, 250, 500, 1000),
								   state="readonly", width=17, wrap=True)
		self.n = Spinbox(self.top_frame, from_=2, to=30, state="readonly", width=17, wrap=True)  # Объем выборки

		# ---Для-ввода-парматра-альфа---
		self.onoff_alpha = BooleanVar(value=False)
		self.alpha_widget_label = Label(self.top_frame, text="Введите уровень\nзначимости в %:")
		self.alpha_widget_entry = Spinbox(self.top_frame, from_=0, to=100, state="readonly", width=17, wrap=True)
		# ---Поля-вывода---
		# Атрибуты для расчета угнетённых частей растения
		# и доверительного интервала с уровнями значимости α.
		self.l_alpha_ci10_g = Label(self.bottom_frame, text="α = 10% : ")
		self.l_alpha_ci5_g = Label(self.bottom_frame, text="α = 5% : ")
		self.l_alpha_ci1_g = Label(self.bottom_frame, text="α = 1% : ")
		self.l_alpha_ci01_g = Label(self.bottom_frame, text="α = 0.1% : ")
		self.l_alpha_ci10_r = Label(self.bottom_frame, text="α = 10% : ")
		self.l_alpha_ci5_r = Label(self.bottom_frame, text="α = 5% : ")
		self.l_alpha_ci1_r = Label(self.bottom_frame, text="α = 1% : ")
		self.l_alpha_ci01_r = Label(self.bottom_frame, text="α = 0.1% : ")
		self.l_alpha_ci_custom_g = Label(self.bottom_frame, text="α = ? : ")
		self.l_alpha_ci_custom_r = Label(self.bottom_frame, text="α = ? : ")
		self.inghib_g = 0  # Угнетение зелёной части
		self.inghib_r = 0  # Угнентение корневой системы

		# ---Поле-изображения---(атрибуты "художника" холста)
		self.canv = Canvas(self.picture_frame, width=scrn_width, height=scrn_height, bg="white")
		self.turt_screen = TurtleScreen(self.canv)
		self.turt_screen.tracer(False)
		self.turt = RawTurtle(self.turt_screen)
		self.turt_stack = []
		self.turt_deg = 0
		self.turt.ht()

	def run(self):
		# Запуск основного цикла
		self.draw_widgets()
		self.root.mainloop()

	def draw_widgets(self):
		self.draw_menu()

		self.top_frame.grid(row=0, column=0, sticky=W)
		self.draw_top_frame(tf=self.top_frame)
		self.picture_frame.grid(row=0, column=1, sticky=E)
		self.draw_picture_frame(pf=self.picture_frame)
		self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky=W+E)
		self.draw_bottom_frame(bf=self.bottom_frame)

	def draw_top_frame(self, tf):
		Label(tf, text="Катион (Металл):").grid(row=0, column=0, sticky=W, pady=10)
		self.metal.grid(row=0, column=1, sticky=W, pady=10, padx=10)
		Label(tf, text="Анион:").grid(row=1, column=0, sticky=W, pady=10)
		self.anion.grid(row=1, column=1, sticky=W, pady=10, padx=10)
		Label(tf, text="Культура растения:").grid(row=2, column=0, sticky=W, pady=10)
		self.culture.grid(row=2, column=1, sticky=W, pady=10, padx=10)

		Label(tf, text="Часть растения").grid(row=3, column=0, sticky=W, pady=10)
		self.part.grid(row=3, column=1, sticky=W, pady=1, padx=10)

		Label(tf, text="Концентрация в мг/л (от 2 до 1000):").grid(row=4, column=0, sticky=W, pady=10)
		self.concentrate.grid(row=4, column=1, sticky=W, pady=10, padx=10)
		Label(tf, text="Объём выборки (от 2 до 30):").grid(row=5, column=0, sticky=W, pady=10)
		self.n.grid(row=5, column=1, sticky=W, pady=10, padx=10)

		Button(tf, text="Вычислить", width=10, command=self.calculate,
			relief=GROOVE).grid(row=6, column=3, sticky=W, pady=10, padx=10)
		Button(tf, text="Отчистить\nхолст", width=10, command=self.clear_canvas,
			relief=GROOVE).grid(row=7, column=3, sticky=W, pady=10, padx=10)

	def draw_picture_frame(self, pf):
		Label(pf, text="Модель культуры").grid(row=0, column=0)
		self.canv.grid(row=1, column=0)

	def draw_bottom_frame(self, bf):
		Label(bf, text="Результат для зелёной части в мм:").grid(row=0, column=0, sticky=W, pady=10)
		self.l_alpha_ci10_g.grid(row=2, column=0, sticky=W, pady=5)
		self.l_alpha_ci5_g.grid(row=3, column=0, sticky=W, pady=5)
		self.l_alpha_ci1_g.grid(row=4, column=0, sticky=W, pady=5)
		self.l_alpha_ci01_g.grid(row=5, column=0, sticky=W, pady=5)

		Label(bf, text="Результат для корневой системы в мм:").grid(row=0, column=2, sticky=W, pady=10, padx=60)
		self.l_alpha_ci10_r.grid(row=2, column=2, sticky=W, pady=5, padx=60)
		self.l_alpha_ci5_r.grid(row=3, column=2, sticky=W, pady=5, padx=60)
		self.l_alpha_ci1_r.grid(row=4, column=2, sticky=W, pady=5, padx=60)
		self.l_alpha_ci01_r.grid(row=5, column=2, sticky=W, pady=5, padx=60)

	def draw_menu(self):
		menu_bar = Menu(self.root)

		file_menu = Menu(menu_bar, tearoff=0)
		file_menu.add_separator()
		file_menu.add_command(label="Выход", command=self.sure_exit)

		edit_menu = Menu(menu_bar, tearoff=0)
		edit_menu.add_command(label="Очистить холст", command=self.clear_canvas)
		edit_menu.add_separator()
		edit_menu.add_checkbutton(label="Ввод α (уровень значимости)", offvalue=0, onvalue=1,
								variable=self.onoff_alpha, command=self.on_alpha)

		menu_bar.add_cascade(label="Файл", menu=file_menu)
		menu_bar.add_cascade(label="Изменить", menu=edit_menu)
		self.root.configure(menu=menu_bar)

	def calculate(self):
		# Подключаемся к БД
		workbook = openpyxl.reader.excel.load_workbook(filename="db_toxic.xlsx")
		workbook.active = 1
		active_sheet = workbook.active

		# Выбираем, что вычислять и рисовать
		if self.part.get() == "Зелёная часть":
			plant_part = GREEN_PART
		elif self.part.get() == "Корневая система":
			plant_part = ROOT_SYSTEM
		else:
			plant_part = BOTH_PART

		# Определение основных переменных, с которыми предстоит оперировать
		metal = self.metal.get()
		anion = self.anion.get()
		culture = self.culture.get()
		concentrate = float(self.concentrate.get()) / 100
		n = int(self.n.get())

		if plant_part == GREEN_PART or plant_part == BOTH_PART:
			y_g = active_sheet[get_probit_cell(metal, anion, culture, GREEN_PART)].value
			coefficient = get_coefficient(y_g)
			self.inghib_g = ingib_percent_g = get_ingib(coefficient, concentrate)
			result_model_g = round(get_control_mm(culture, GREEN_PART) * (1 - ingib_percent_g), 4)
			self.l_alpha_ci10_g.configure(
				text=f"α = 10% : {result_model_g} ± {round(get_confidence_interval(n, culture, GREEN_PART, 0.1), 4)} [мм]")
			self.l_alpha_ci5_g.configure(
				text=f"α = 5% : {result_model_g} ± {round(get_confidence_interval(n, culture, GREEN_PART, 0.05), 4)} [мм]")
			self.l_alpha_ci1_g.configure(
				text=f"α = 1% : {result_model_g} ± {round(get_confidence_interval(n, culture, GREEN_PART, 0.01), 4)} [мм]")
			self.l_alpha_ci01_g.configure(
				text=f"α = 0.1% : {result_model_g} ± {round(get_confidence_interval(n, culture, GREEN_PART, 0.001), 4)} [мм]")

			if self.onoff_alpha.get():
				alph = float(self.alpha_widget_entry.get()) / 100
				confidence_interval = round(get_confidence_interval(n, culture, GREEN_PART, float(alph)), 4)
				self.l_alpha_ci_custom_g.configure(
					text=f"α = {round(int(alph * 100), 4)}% :{result_model_g} ± {confidence_interval} [мм]")

		if plant_part == ROOT_SYSTEM or plant_part == BOTH_PART:
			y_r = active_sheet[get_probit_cell(metal, anion, culture, ROOT_SYSTEM)].value
			coefficient = get_coefficient(y_r)
			self.inghib_r = ingib_percent_r = get_ingib(coefficient, concentrate)
			result_model_r = round(get_control_mm(culture, ROOT_SYSTEM) * (1 - ingib_percent_r), 4)
			self.l_alpha_ci10_r.configure(
				text=f"α = 10% : {result_model_r} ± {round(get_confidence_interval(n, culture, ROOT_SYSTEM, 0.1), 4)} [мм]")
			self.l_alpha_ci5_r.configure(
				text=f"α = 5% : {result_model_r} ± {round(get_confidence_interval(n, culture, ROOT_SYSTEM, 0.05), 4)} [мм]")
			self.l_alpha_ci1_r.configure(
				text=f"α = 1% : {result_model_r} ± {round(get_confidence_interval(n, culture, ROOT_SYSTEM, 0.01), 4)} [мм]")
			self.l_alpha_ci01_r.configure(
				text=f"α = 0.1% : {result_model_r} ± {round(get_confidence_interval(n, culture, ROOT_SYSTEM, 0.001), 4)} [мм]")

			if self.onoff_alpha.get():
				alph = float(self.alpha_widget_entry.get()) / 100
				confidence_interval = round(get_confidence_interval(n, culture, ROOT_SYSTEM, float(alph)), 4)
				self.l_alpha_ci_custom_r.configure(
					text=f"α = {round(int(alph * 100), 4)}% :{result_model_r} ± {confidence_interval} [мм]")

		# -----Цвета-----
		B = "#000000"  # Чёрный
		G = "#20991a"  # Зелёный
		R = "#752d19"  # Коричневый
		# -----Подготовка к рисованию-----
		self.turt.goto(0, 0)  # Нужно для корректного отображения модели.
		self.turt_stack = []
		self.turt.setheading(0)
		self.turt_deg = 0
		self.canv.delete("all")
		# -----Рисование модели абстрактного растения-----
		self.turt.penup()
		self.turt.goto(-scrn_width//2, -scrn_height//6)
		self.turt.pendown()

		self.turt.forward(scrn_width//2 - 30)
		self.turt.left(90)
		self.turt_deg += 90
		draw_circe_part(self.turt, 4)
		self.turt_deg -= 90

		# Рисование зелёной части.
		self.turt.color(G)  # (#20991a_)
		pushT(self.turt, self.turt_deg, self.turt_stack)
		self.turt.left(90)
		self.turt_deg += 90
		if plant_part == GREEN_PART or plant_part == BOTH_PART:
			draw_lsys(self.turt, self.turt_deg, green_rule(4), 4 * (1 - self.inghib_g), 20, self.turt_stack)
		popT(self.turt, self.turt_deg, self.turt_stack)
		self.turt.color(B)

		draw_circe_part(self.turt, 4)
		self.turt_deg -= 90

		pushT(self.turt, self.turt_deg, self.turt_stack)
		self.turt.left(90)
		self.turt_deg += 90
		self.turt.forward(scrn_width // 2 - 30)
		popT(self.turt, self.turt_deg, self.turt_stack)

		self.turt.right(90)
		self.turt_deg -= 90
		# Рисование корневой системы.
		for n in range(3):
			if n == 1:
				self.turt.right(90)
				self.turt_deg -= 90
			self.turt.color(B)
			draw_circe_part(self.turt, 8)
			self.turt.color(R)
			self.turt_deg -= 45
			if n != 0:
				self.turt.left(90)
			pushT(self.turt, self.turt_deg, self.turt_stack)
			self.turt.left(90)
			self.turt_deg += 90
			if plant_part == ROOT_SYSTEM or plant_part == BOTH_PART:
				if n == 0:
					self.turt.right(90)
					self.turt_deg -= 90
				draw_lsys(self.turt, self.turt_deg, root_rule(3), 1 * (1 - self.inghib_r), 15, self.turt_stack)
			self.turt_deg = self.turt_stack[-1][2]
			popT(self.turt, self.turt_deg, self.turt_stack)

		self.turt.color(B)
		draw_circe_part(self.turt, 6)

	def clear_canvas(self):
		# Отчистка холста.
		self.turt.goto(0, 0)
		self.turt_stack = []
		self.turt.setheading(0)
		self.turt_deg = 0
		self.canv.delete("all")

	def on_alpha(self):
		# Включение\отключение поля ввода alpha - уровня значимости.
		# А также изменение формата вывода данных.

		if self.onoff_alpha.get():
			self.alpha_widget_label.grid(row=6, column=0, sticky=W)
			self.alpha_widget_entry.grid(row=6, column=1, sticky=W, padx=10)
			self.l_alpha_ci_custom_g.grid(row=6, column=0, sticky=W, pady=5)
			self.l_alpha_ci_custom_r.grid(row=6, column=2, sticky=W, pady=5, padx=60)

			self.l_alpha_ci10_g.grid_forget()
			self.l_alpha_ci5_g.grid_forget()
			self.l_alpha_ci1_g.grid_forget()
			self.l_alpha_ci01_g.grid_forget()
			self.l_alpha_ci10_r.grid_forget()
			self.l_alpha_ci5_r.grid_forget()
			self.l_alpha_ci1_r.grid_forget()
			self.l_alpha_ci01_r.grid_forget()
		else:
			self.alpha_widget_label.grid_forget()
			self.alpha_widget_entry.grid_forget()
			self.l_alpha_ci_custom_g.grid_forget()
			self.l_alpha_ci_custom_r.grid_forget()

			self.l_alpha_ci10_g.grid(row=1, column=0, sticky=W, pady=5)
			self.l_alpha_ci5_g.grid(row=2, column=0, sticky=W, pady=5)
			self.l_alpha_ci1_g.grid(row=3, column=0, sticky=W, pady=5)
			self.l_alpha_ci01_g.grid(row=4, column=0, sticky=W, pady=5)
			self.l_alpha_ci10_r.grid(row=1, column=2, sticky=W, pady=5, padx=60)
			self.l_alpha_ci5_r.grid(row=2, column=2, sticky=W, pady=5, padx=60)
			self.l_alpha_ci1_r.grid(row=3, column=2, sticky=W, pady=5, padx=60)
			self.l_alpha_ci01_r.grid(row=4, column=2, sticky=W, pady=5, padx=60)

	def sure_exit(self):
		# Диалоговое окно выхода из приложения.
		choice = mb.askyesno("Выход", "Вы уверены, что хотите выйти?")
		if choice:
			self.root.destroy()


if __name__ == "__main__":
	# Запуск программы.
	window = Window(WIDTH, HEIGHT, "PyToxicology", resizable=(False, False))
	window.run()
