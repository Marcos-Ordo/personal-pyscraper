import Compra
import Maximus

## TODO: Aprender tkinter orientado a objetos.
# from tkinter import * 
# from tkinter.ttk import *

def info_gpus_en_(page):
    if page == "Todo" or page == "Compragamer":
        o_compra = Compra.Compra()
        o_compra.reload_on(Compra.PLACAS)
        o_compra.get_content()
        o_compra.save_data()
        o_compra.destroy()
    if page == "Todo" or page == "Maximus":
        o_maximus = Maximus.Maximus()
        o_maximus.reload_on(Maximus.PLACAS)
        o_maximus.get_all()
        o_maximus.save_data()
        o_maximus.destroy()

def info_cpus_en_(page):
    if page == "Todo" or page == "Compragamer":
        o_compra = Compra.Compra()
        o_compra.reload_on(Compra.MICROS)
        o_compra.get_content()
        o_compra.save_data()
        o_compra.destroy()
    if page == "Todo" or page == "Maximus":
        o_maximus = Maximus.Maximus()
        o_maximus.reload_on(Maximus.MICROS)
        o_maximus.get_all()
        o_maximus.save_data()
        o_maximus.destroy()

def info_todo_en_(page):
    info_gpus_en_(page)
    info_cpus_en_(page)

def buscar_en_(search, page):
    if page == "Todo" or page == "Compragamer":
        o_compra = Compra.Compra()
        o_compra.search_for(search)
        o_compra.get_content()
        o_compra.save_data()
        o_compra.destroy()
    if page == "Todo" or page == "Maximus":
        o_maximus = Maximus.Maximus()
        o_maximus.search_for(search)
        o_maximus.get_all()
        o_maximus.save_data()
        o_maximus.destroy()