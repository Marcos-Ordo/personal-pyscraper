from scraper import *
from tkinter import ttk
import tkinter       as tk
import customtkinter as ctk

PAGES = ["Maximus", "Compragamer"]

class Handler():
    def __init__(self):
        self.__subscribers: set[Scraper_Adapter] = set()

    @property
    def subscribers(self):
        return self.__subscribers
    
    def subscribe(self, adapter):
        self.subscribers.add(adapter)

    def unsubscribe(self, adapter):
        self.subscribers.remove(adapter)

    def subscribe_websites(self, page):
        if page == "Ambas":
            for each_page in PAGES:
                self.subscribe(Scraper_Adapter(each_page))
        elif page != "None":
            self.subscribe(Scraper_Adapter(page))

    def unsubscribe_websites(self):
        self.subscribers.clear()

    def update(self, msg, strat):
        for subscriber in self.subscribers:
            subscriber.update(msg, strat)


class Scraper_Adapter():
    def __init__(self, page):
        match page:
            case "Maximus": 
                self.__scraper = Maximus()
            case "Compragamer": 
                self.__scraper = Compra()
            case _:
                pass

    def update(self, msg, strat):
        self.__scraper.change_strat_to(strat)
        self.__scraper.search(msg)
    
    def get_memory(self):
        return self.__scraper.memory.get()

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

class Gui(ctk.CTk):
    def __init__(self):
        # SETUP
        super().__init__()
        self.__handler = Handler()

        self.title("pyscraper")
        self.tk.call('wm', 'iconphoto', self, tk.PhotoImage(file='images/github-icon.png'))
        self.geometry("700x450")
        self.check_var = ctk.BooleanVar(value=True)

        # WIDGETS
        self.top_section()
        self.search_section()
        self.default_buttons_section()
        self.tableview()

        # self.save_button = ctk.CTkButton(self, width=50, text="Guardar", command=self.save, state="disabled")
        # self.save_button.pack(pady=40)

    # WIDGETS
    def top_section(self):
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=10)

        self.open_button = ctk.CTkSegmentedButton(top_frame, values=PAGES + ["Ambas", "None"], command=self.on_website_selection)
        self.open_button.grid(row=0, column=0, columnspan=2, padx=10)
        
        self.close_button = ctk.CTkButton(top_frame, width=100, text="Elegir de nuevo", command=self.on_website_reselection, state="disabled")
        self.close_button.grid(row=0, column=3, padx=10)

    def search_section(self):
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(pady=20)

        self.search_button = ctk.CTkButton(search_frame, width=50, text="Buscar", command=self.on_search, state="disabled")
        self.search_button.grid(row=0, column=0, padx=10)

        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Buscar ...", state="disabled")
        self.search_entry.grid(row=0, column=1, padx=10)

    def default_buttons_section(self):
        default_buttons_frame = ctk.CTkFrame(self)
        default_buttons_frame.pack(pady=20)

        self.gpus_button = ctk.CTkButton(default_buttons_frame, width=100, text="Buscar GPUs", command=self.on_search_of_gpu, state="disabled")
        self.gpus_button.grid(row=0, column=0, padx=10)

        self.cpus_button = ctk.CTkButton(default_buttons_frame, width=100, text="Buscar CPUs", command=self.on_search_of_cpu, state="disabled")
        self.cpus_button.grid(row=0, column=1, padx=10)

    def tableview(self):
        self.tree = ttk.Treeview(self, columns=("col1", "col2","col3","col4"), show="headings")
        self.tree.heading("col1", text="Tipo")
        self.tree.heading("col2", text="Nombre")
        self.tree.heading("col3", text="Precio")
        self.tree.heading("col4", text="Origen")
        self.tree.pack(fill="both", expand=True)

    ## EVENTS
    def on_website_selection(self, website):
        self.open_button.configure(state="disabled")
        self.close_button.configure(state="normal")
        self.search_button.configure(state="normal")
        self.search_entry.configure(state="normal")
        self.gpus_button.configure(state="normal")
        self.cpus_button.configure(state="normal")
        # self.save_button.configure(state="normal")

        self.__handler.subscribe_websites(website)

    def on_website_reselection(self):
        self.open_button.configure(state="normal")
        self.open_button.set("None")
        self.close_button.configure(state="disabled")
        self.search_button.configure(state="disabled")
        self.search_entry.configure(state="disabled")
        self.gpus_button.configure(state="disabled")
        self.cpus_button.configure(state="disabled")

        self.tree.delete(*self.tree.get_children())
        self.__handler.unsubscribe_websites()

    def on_search(self):
        self.__handler.update(self.search_entry.get(), "msg")
        self.process_events()

    def on_search_of_gpu(self):
        self.__handler.update(None, "gpu")
        self.process_events()
    
    def on_search_of_cpu(self):
        self.__handler.update(None, "cpu")
        self.process_events()

    ## DEFS
    def process_events(self):
        for adapter in self.__handler.subscribers:
            for item in adapter.get_memory():
                self.tree.insert("", "end", values=(item.value['type'], item.value['name'], item.value['price'], item.value['origin']))

        # self.after(100, self.process_events)

    # def save(self):
    #     pass

app = Gui()

app.mainloop()