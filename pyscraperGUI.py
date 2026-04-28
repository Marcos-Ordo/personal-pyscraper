from scraper import *
from tkinter import PhotoImage
import customtkinter

PAGES = ["Maximus", "Compragamer", "ambas"]

## Handler:
class Handler():
    def __init__(self):
        self.__subscribers = []

    @property
    def subscribers(self):
        return self.__subscribers

    def subscribe(self, page):
        if page == "ambas":
            for each_page in ["Maximus", "Compragamer"]: # PAGES sin "ambas"
                # Deberia agregar concurrencia acá
                self.subscribers.append(Scraper_Adapter(each_page))
        else:
            self.subscribers.append(Scraper_Adapter(page))

    def search(self, value):
        for subscriber in self.subscribers:
            subscriber.update_search(value)

    def search_gpus(self):
        for subscriber in self.subscribers:
            subscriber.update_search_gpus()

    def search_cpus(self):
        for subscriber in self.subscribers:
            subscriber.update_search_cpus()
    
    def save(self):
        for subscriber in self.subscribers:
            subscriber.update_save()

class Scraper_Adapter():
    def __init__(self, page):
        match page:
            case "Maximus": 
                self.__scraper = Maximus()
            case "Compragamer": 
                self.__scraper = Compra()
            case _:
                pass
    
    @property
    def scraper(self):
        return self.scraper

    def search_gpus(self):
        pass

    def search_cpus(self):
        pass

    def search(self, value):
        pass

    def save(self):
        pass

HANDLER = Handler()
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

class Gui(customtkinter.CTk):
    def __init__(self):
        # SETUP
        super().__init__()

        self.title("pyscraper")
        img = PhotoImage(file='images/github-icon.png')
        self.tk.call('wm', 'iconphoto', self, img)
        self.geometry("700x450")

        self.check_var = customtkinter.BooleanVar(value=True)

        # WIDGETS
        self.top_section()
        self.search_section()
        self.default_buttons_section()

        self.save_button = customtkinter.CTkButton(self, width=50, text="Guardar", command=self.save, state="disabled")
        self.save_button.pack(pady=40)

    # WIDGETS
    def top_section(self):
        top_frame = customtkinter.CTkFrame(self)
        top_frame.pack(pady=10)

        self.page_buttons = customtkinter.CTkSegmentedButton(top_frame, values=PAGES, command=self.select_page)
        self.page_buttons.grid(row=0, column=1, columnspan=1, padx=10)

    def search_section(self):
        search_frame = customtkinter.CTkFrame(self)
        search_frame.pack(pady=20)

        self.search_button = customtkinter.CTkButton(search_frame, width=50, text="Buscar", command=self.search_for)
        self.search_button.grid(row=0, column=0, padx=10)

        self.search_entry = customtkinter.CTkEntry(search_frame, width=300, placeholder_text="Buscar ...")
        self.search_entry.grid(row=0, column=1, padx=10)

    def default_buttons_section(self):
        default_buttons_frame = customtkinter.CTkFrame(self)
        default_buttons_frame.pack(pady=20)

        self.gpus_button = customtkinter.CTkButton(default_buttons_frame, width=100, text="Buscar GPUs", command=self.search_gpus)
        self.gpus_button.grid(row=0, column=0, padx=10)

        self.cpus_button = customtkinter.CTkButton(default_buttons_frame, width=100, text="Buscar CPUs", command=self.search_cpus)
        self.cpus_button.grid(row=0, column=1, padx=10)

    # EVENTS
    def on_page_load(self):
        self.page_buttons.configure(state="disabled")
        self.search_button.configure(state="normal")
        self.search_entry.configure(state="normal")
        self.gpus_button.configure(state="normal")
        self.cpus_button.configure(state="normal")
        self.save_button.configure(state="normal")

    def on_page_close(self):
        self.page_buttons.configure(state="normal")
        self.search_button.configure(state="disabled")
        self.search_entry.configure(state="disabled")
        self.gpus_button.configure(state="disabled")
        self.cpus_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.search_entry.select_clear()
        self.search_entry.configure(placeholder_text="Buscar ...")
        self.page_buttons.set(value="None")

    # DEFS
    def select_page(self, page):
        pass

    def search_for(self):
        pass

    def search_gpus(self):
        pass

    def search_cpus(self):
        pass

    def save(self):
        pass

app = Gui()
app.mainloop()