from tkinter import *
from tkinter import messagebox as mb
"""
Данный файл нужен на случай, если возникнет необходимость в создании
нового рабочего окна программы (не в качестве виджета).
"""


class ChildWindow:
	def __init__(self, parent, width, height, title="MyWindow", resizable=(False, False), icon=None, x=None, y=None):
		self.ch_root = Toplevel(parent)  # Создаётся дочернее окно
		self.ch_root.title(title)
		self.p = parent
		if not x:
			x = self.ch_root.winfo_screenwidth()//2 - width//2
		if not y:
			y = self.ch_root.winfo_screenheight()//2 - height//2

		self.ch_root.geometry(f"{width}x{height}+{x}+{y}")
		self.ch_root.resizable(resizable[0], resizable[1])
		if icon:
			self.ch_root.iconbitmap(icon)

		self.login_entry = Entry(self.ch_root)
		self.password_entry = Entry(self.ch_root, show="🞄")

	def draw_widget(self):
		Label(self.ch_root, text="Введите логин: ", justify=LEFT).grid(row=0, column=0, sticky=W)
		self.login_entry.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)
		Label(self.ch_root, text="Введите пароль: ", justify=LEFT).grid(row=2, column=0, sticky=W)
		self.password_entry.grid(row=2, column=1, sticky=W + E, padx=5, pady=5)

		Button(self.ch_root, text="Войти", width=10, command=self.enter,
			relief=GROOVE).grid(row=3, column=0, padx=5, pady=5, sticky=W)
		Button(self.ch_root, text="Выход", width=10, command=self.sure_exit, relief=GROOVE).grid(row=3, column=1, sticky=E)

	def enter(self):
		pass

	def sure_exit(self):
		# Диалоговое окно выхода из приложения.
		choice = mb.askyesno("Выход", "Вы уверены, что хотите выйти?")
		if choice:
			self.ch_root.destroy()

	def grab_focus(self):  # Захват фокуса окна на себя
		self.ch_root.grab_set()  # Перехват всех событий, происходящих в приложении
		self.ch_root.focus_set()  # Метод захвата фокуса
		self.ch_root.wait_window()  # Метод ждёт когда будет уничтожен текущий объект
		# Работа не возобновляется, при этом не оказывается влияние на основной цикл
