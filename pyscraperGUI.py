from scraper import *
from tkinter import *
import customtkinter

PAGES = ["Maximus", "Compragamer", "Todas"]

## Handler:
class Handler():
    def __init__(self, page, show):
        self.handler = []
        if page == "Todas":
            handler_pages = PAGES
            handler_pages.remove("Todas")
            for each_page in handler_pages:
                self.handler.append(Scraper_Header(each_page, show))
        else:
            self.handler.append(Scraper_Header(page, show))

    def destroy(self):
        for each_header in self.handler:
            each_header.destroy()

    def search(self, value):
        for each_header in self.handler:
            each_header.search(value)

    def info_gpus(self):
        for each_header in self.handler:
            each_header.info_gpus()

    def info_cpus(self):
        for each_header in self.handler:
            each_header.info_cpus()
    
    def save(self):
        for each_header in self.handler:
            each_header.save()

class Scraper_Header():
    def __init__(self, scraper, show):
        match scraper:
            case "Maximus": 
                self.scraper = Maximus.Maximus(show)
            case "Compragamer": 
                self.scraper = Compra.Compra(show)
            case _:
                print("Error NoPageFound ...")

    def destroy(self):
        self.scraper.destroy()
    
    def info_gpus(self):
        self.scraper.reload_on(self.PLACAS)
        self.scraper.get_all()

    def info_cpus(self):
        self.scraper.reload_on(self.MICROS)
        self.scraper.get_all()

    def search(self, value):
        self.scraper.search_for(value)
        self.scraper.get_all()

    def save(self):
        self.scraper.save_data()

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

class Gui(customtkinter.CTk):
    def __init__(self):
        # SETUP
        super().__init__()

        self.title("pyscraper")
        img = PhotoImage(file='images/github-icon.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
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

        self.view_check = customtkinter.CTkCheckBox(top_frame, text="esconder págs", variable=self.check_var, onvalue=True, offvalue=False)
        self.view_check.grid(row=0, column=0, padx=10)

        self.page_buttons = customtkinter.CTkSegmentedButton(top_frame, values=PAGES, command=self.open_pages)
        self.page_buttons.grid(row=0, column=1, columnspan=2, padx=10)

        self.close_button = customtkinter.CTkButton(top_frame, width=100, text="Cerrar página", command=self.close_pages, state="disabled")
        self.close_button.grid(row=0, column=3, padx=10)

    def search_section(self):
        search_frame = customtkinter.CTkFrame(self)
        search_frame.pack(pady=20)

        self.search_button = customtkinter.CTkButton(search_frame, width=50, text="Buscar", command=self.search_for, state="disabled")
        self.search_button.grid(row=0, column=0, padx=10)

        self.search_entry = customtkinter.CTkEntry(search_frame, width=300, placeholder_text="Buscar ...", state="disabled")
        self.search_entry.grid(row=0, column=1, padx=10)

    def default_buttons_section(self):
        default_buttons_frame = customtkinter.CTkFrame(self)
        default_buttons_frame.pack(pady=20)

        self.gpus_button = customtkinter.CTkButton(default_buttons_frame, width=100, text="Buscar GPUs", command=self.info_gpus, state="disabled")
        self.gpus_button.grid(row=0, column=0, padx=10)

        self.cpus_button = customtkinter.CTkButton(default_buttons_frame, width=100, text="Buscar CPUs", command=self.info_cpus, state="disabled")
        self.cpus_button.grid(row=0, column=1, padx=10)

    # EVENTS
    def on_page_load(self):
        self.view_check.configure(state="disabled")
        self.page_buttons.configure(state="disabled")
        self.close_button.configure(state="normal")
        self.search_button.configure(state="normal")
        self.search_entry.configure(state="normal")
        self.gpus_button.configure(state="normal")
        self.cpus_button.configure(state="normal")
        self.save_button.configure(state="normal")

    def on_page_close(self):
        self.view_check.configure(state="normal")
        self.page_buttons.configure(state="normal")
        self.close_button.configure(state="disabled")
        self.search_button.configure(state="disabled")
        self.search_entry.configure(state="disabled")
        self.gpus_button.configure(state="disabled")
        self.cpus_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.search_entry.select_clear()
        self.search_entry.configure(placeholder_text="Buscar ...")
        self.page_buttons.set(value="None")

    # DEFS
    def open_pages(self, page):
        self.handler = Handler(page, self.check_var.get())
        self.on_page_load()

    def close_pages(self):
        self.handler.destroy()
        self.on_page_close()

    def search_for(self):
        if self.search_entry.get():
            self.handler.search(self.search_entry.get()) # Falta que si no encontró nada, avise
        else:
            print("Error NoSearchInput ...")

    def info_gpus(self):
        self.handler.info_gpus()

    def info_cpus(self):
        self.handler.info_cpus()

    def save(self):
        self.handler.save()

app = Gui()
app.mainloop()