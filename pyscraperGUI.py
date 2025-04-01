## TODO: Aprender tkinter orientado a objetos.
# from tkinter import * 
# from tkinter.ttk import *

from scraper import *
from tkinter import *
import customtkinter

## DEFS:
def info_gpus_en_(page, show):
    if page == "Todo" or page == "Compragamer":
        o_compra = Compra.Compra(show)
        o_compra.reload_on(Compra.PLACAS)
        o_compra.get_content()
        o_compra.save_data()
        o_compra.destroy()
    if page == "Todo" or page == "Maximus":
        o_maximus = Maximus.Maximus(show)
        o_maximus.reload_on(Maximus.PLACAS)
        o_maximus.get_all()
        o_maximus.save_data()
        o_maximus.destroy()

def info_cpus_en_(page, show):
    if page == "Todo" or page == "Compragamer":
        o_compra = Compra.Compra(show)
        o_compra.reload_on(Compra.MICROS)
        o_compra.get_content()
        o_compra.save_data()
        o_compra.destroy()
    if page == "Todo" or page == "Maximus":
        o_maximus = Maximus.Maximus(show)
        o_maximus.reload_on(Maximus.MICROS)
        o_maximus.get_all()
        o_maximus.save_data()
        o_maximus.destroy()

def info_todo_en_(page, show):
    info_gpus_en_(page, show)
    info_cpus_en_(page, show)

def buscar_en_(search, page, show):
    if page == "Todo" or page == "Compragamer":
        o_compra = Compra.Compra(show)
        o_compra.search_for(search)
        o_compra.get_content()
        o_compra.save_data()
        o_compra.destroy()
    if page == "Todo" or page == "Maximus":
        o_maximus = Maximus.Maximus(show)
        o_maximus.search_for(search)
        o_maximus.get_all()
        o_maximus.save_data()
        o_maximus.destroy()

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.title("pyscraper")
img = PhotoImage(file='images/github-icon.png')
root.tk.call('wm', 'iconphoto', root._w, img)
root.geometry("700x450")

#DEFS:
check_var = customtkinter.BooleanVar(value=True)
pages = ["Maximus", "Compragamer", "Todas"]

def game():
    if check_var.get():
        my_label.configure(text="It's clicked!")
    else:
        my_label.configure(text="It's not clicked!")

def open_page(page):
    info_gpus_en_(page, check_var.get())

#WIDGETS:
my_check = customtkinter.CTkCheckBox(root, text="esconder págs", variable=check_var, command=game, onvalue=True, offvalue=False)
my_check.pack(pady=20)

my_label = customtkinter.CTkLabel(root, text="")
my_label.pack()

page_buttons = customtkinter.CTkSegmentedButton(root, values=pages, command=open_page)
page_buttons.pack(pady=20)

root.mainloop()