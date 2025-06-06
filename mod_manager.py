import os
import requests
import zipfile
import shutil
import subprocess
import winreg
import locale
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import time
import sys
import configparser


CREATION_FLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


# region CONFIG

MODPACK_REPOSITORY_URL = "https://github.com/furkanaliunal/R.E.P.O-Modpack.git"
MODLOADER_REPOSITORY_URL = "https://github.com/furkanaliunal/R.E.P.O-Modloader.git"
CURRENT_VERSION_URL = "https://github.com/furkanaliunal/R.E.P.O-Modloader/releases/download/Release-0.4_HotFix2/Lethal.Mod.Manager.exe"
UPDATE_CHECK_URL = "https://api.github.com/repos/furkanaliunal/R.E.P.O-Modloader/releases/latest"
STEAM_APP_ID = "3241660"


# region LOCALE
MESSAGES = {
    "tr": {
        "app_title" : "Furkis Mod Yükleyici",
        "app_button_update" : "Güncelle",
        "app_button_start" : "Oyunu Başlat",
        "app_selection_copied" : "Seçilen Satır Kopyalandı!",
        "git_install" : "Git kurulumu yapılıyor",
        "git_folder_not_found" : "Çekirdek bulunamadı",
        "git_installation_complete" : "Git kurulumu tamamlandı",
        "git_fetching_updates" : "Çekirdek kuruluyor",
        "git_cleaning_files" : "Oyun dosyaları temizleniyor",
        "git_update_completed" : "Çekirdek kurulumu tamamlandı",
        "starting_game": "Oyun başlatılıyor..",
        "game_found": "Oyun bulundu!",
        "game_exe_path_not_found": "Oyunun başlatıcısı(.exe) bulunamadı",
        "game_start_failed": "Oyun başlatılamadı.",
        "game_directory_path_not_found": "Oyun dizini bulunamadı.",
        "mods_file_not_found": "Ek paketler bulunamadı",
        "mod_already_updated": "{} zaten güncel.",
        "downloading": "{} indiriliyor...",
        "download_failed": "{} indirilemedi!",
        "download_progress": "İndirme ilerlemesi: {:.2f}%",
        "download_completed": "İndirme tamamlandı!",
        "extracting": "{} başarıyla indirildi. Çıkarılıyor...",
        "installed_successfully": "{} başarıyla yüklendi!",
        "mod_install_complete": "Mod yükleme işlemi tamamlandı!",
        "modloader_update_checking": "Furkis Mod Yükleyicisi Güncellesi Kontrol Ediliyor..",
        "modloader_update_available": "Furkis Mod Yükleyicisinin Güncellemesi Mevcut!",
        "modloader_update_download": "İndirme Bağlantısı:\n{}\n\nÇift tıklayarak metni kopyalayabilirsin",
        "modloader_uptodate": "Furkis Mod Yükleyicisi Güncel",
        "modpack_update_checking": "Mod Paketi Güncellesi Kontrol Ediliyor..",
        "modpack_update_available": "Mod Paketinin Güncellemesi Mevcut!",
        "modpack_update_download": "Güncelle tuşuna basarak güncellemeni alabilirsin",
        "modpack_uptodate": "Mod Paketi Güncel",
        "updates_checking": "Güncellemeler kontrol ediliyor..",
        "mod_start_install" : "Güncelle tuşuna basarak kurulumu yapın",
        "mod_pack_activated" : "Mod paketi aktif edildi",
        "mod_pack_deactivated" : "Mod paketi iptal edildi",
        "settings" : "Ayarlar",
        "save" : "Kaydet",
        "cancel" : "Vazgeç",
        "select_game_manual_prompt": "Oyun dizini bulunamadı. Lütfen manuel olarak seçin.",
        "select_game_folder_dialog_title": "Oyun Klasörünü Seçin",
        "invalid_directory_selected": "Seçilen klasörde '{}' bulunamadı.",
        "game_path_saved_success": "Oyun dizini başarıyla kaydedildi.",
        "game_path_save_error": "Registry kaydedilirken bir hata oluştu:\n{}",
        "git_restart_required": "Git başarıyla yüklendi.\nUygulamayı yeniden başlatın.",

    },
    "en": {
        "app_title" : "Furkis Mod Loader",
        "app_button_update" : "Update",
        "app_button_start" : "Start Game",
        "app_selection_copied" : "Selected Line Copied!",
        "git_install" : "Installing Git",
        "git_folder_not_found" : "Git not found",
        "git_installation_complete" : "Git installation completed",
        "git_fetching_updates" : "Fetching updates",
        "git_cleaning_files" : "Cleaning game files",
        "git_update_completed" : "Update completed",
        "starting_game": "Starting the game..",
        "game_found": "Game found!",
        "game_exe_path_not_found": "Game launcher (.exe) not found",
        "game_start_failed": "Game failed to start.",
        "game_directory_path_not_found": "Game directory not found.",
        "mods_file_not_found": "Mods not found",
        "mod_already_updated": "{} is already up to date.",
        "downloading": "Downloading {}...",
        "download_failed": "Failed to download {}!",
        "download_progress": "Download progress: {:.2f}%",
        "download_completed": "Download completed!",
        "extracting": "{} downloaded successfully. Extracting...",
        "installed_successfully": "{} installed successfully!",
        "mod_install_complete": "Mod installation complete!",
        "modloader_update_checking": "Checking for Furkis Mod Loader updates..",
        "modloader_update_available": "Furkis Mod Loader update available!",
        "modloader_update_download": "Download link:\n{}\n\nDouble-click to copy",
        "modloader_uptodate": "Furkis Mod Loader is up to date",
        "modpack_update_checking": "Checking for Mod Pack updates..",
        "modpack_update_available": "Mod Pack update available!",
        "modpack_update_download": "Press the update button to install the latest version",
        "modpack_uptodate": "Mod Pack is up to date",
        "updates_checking": "Checking for updates..",
        "mod_start_install" : "Press the update button to start installation",
        "mod_pack_activated" : "Mod pack activated",
        "mod_pack_deactivated" : "Mod pack deactivated",
        "settings" : "Settings",
        "save" : "Save",
        "cancel" : "Cancel",
        "select_game_manual_prompt": "Game directory not found. Please select it manually.",
        "select_game_folder_dialog_title": "Select Game Folder",
        "invalid_directory_selected": "'{}' not found in the selected folder.",
        "game_path_saved_success": "Game path successfully saved.",
        "game_path_save_error": "An error occurred while saving to registry:\n{}",
        "git_restart_required": "Git installed successfully.\nPlease restart the application.",

    },
    "nl": {
        "app_title" : "Furkis Mod Loader",
        "app_button_update" : "Bijwerken",
        "app_button_start" : "Spel Starten",
        "app_selection_copied" : "Geselecteerde regel gekopieerd!",
        "git_install" : "Git wordt geïnstalleerd",
        "git_folder_not_found" : "Git niet gevonden",
        "git_installation_complete" : "Git-installatie voltooid",
        "git_fetching_updates" : "Updates ophalen",
        "git_cleaning_files" : "Spelbestanden opruimen",
        "git_update_completed" : "Update voltooid",
        "starting_game": "Spel wordt gestart..",
        "game_found": "Spel gevonden!",
        "game_exe_path_not_found": "Spel launcher (.exe) niet gevonden",
        "game_start_failed": "Spel kon niet worden gestart.",
        "game_directory_path_not_found": "Spelmap niet gevonden.",
        "mods_file_not_found": "Mods niet gevonden",
        "mod_already_updated": "{} is al up-to-date.",
        "downloading": "{} wordt gedownload...",
        "download_failed": "{} kon niet worden gedownload!",
        "download_progress": "Downloadvoortgang: {:.2f}%",
        "download_completed": "Download voltooid!",
        "extracting": "{} is succesvol gedownload. Uitpakken...",
        "installed_successfully": "{} is succesvol geïnstalleerd!",
        "mod_install_complete": "Mod-installatie voltooid!",
        "modloader_update_checking": "Controleren op updates voor Furkis Mod Loader..",
        "modloader_update_available": "Update voor Furkis Mod Loader beschikbaar!",
        "modloader_update_download": "Downloadlink:\n{}\n\nDubbelklik om te kopiëren",
        "modloader_uptodate": "Furkis Mod Loader is up-to-date",
        "modpack_update_checking": "Controleren op updates voor Mod Pack..",
        "modpack_update_available": "Update voor Mod Pack beschikbaar!",
        "modpack_update_download": "Druk op de updateknop om de nieuwste versie te installeren",
        "modpack_uptodate": "Mod Pack is up-to-date",
        "updates_checking": "Controleren op updates..",
        "mod_start_install" : "Druk op de updateknop om de installatie te starten",
        "mod_pack_activated" : "Modpakket geactiveerd",
        "mod_pack_deactivated" : "Modpakket gedeactiveerd",
        "settings" : "Instellingen",
        "save" : "Opslaan",
        "cancel" : "Annuleren",
        "select_game_manual_prompt": "Spelmap niet gevonden. Selecteer deze handmatig.",
        "select_game_folder_dialog_title": "Selecteer Spelmap",
        "invalid_directory_selected": "'{}' niet gevonden in de geselecteerde map.",
        "game_path_saved_success": "Spelpad succesvol opgeslagen.",
        "game_path_save_error": "Er is een fout opgetreden bij het opslaan in het register:\n{}",
        "git_restart_required": "Git is succesvol geïnstalleerd.\nHerstart de applicatie.",

    }
}



# region UTILITIES


def get_system_language():
    lang, encoding = locale.getlocale()
    if lang.startswith("Turkish"): lang = "tr"
    elif lang.startswith("Dutch"): lang = "nl"
    else: lang = "en"
    return lang



def fetch_origin_and_reset_local_repo(game_dir, repo_url=MODPACK_REPOSITORY_URL):
    if not os.path.exists(os.path.join(game_dir, ".git")):
        APP.write_to_text_area(MSG["git_folder_not_found"])
        temp_dir = os.path.join(game_dir, "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        subprocess.run(["git", "clone", repo_url, temp_dir], shell=False, creationflags=CREATION_FLAGS)
        for item in os.listdir(temp_dir):
            s = os.path.join(temp_dir, item)
            d = os.path.join(game_dir, item)
            if os.path.isdir(s):
                shutil.move(s, d)
            else:
                shutil.move(s, d)
        shutil.rmtree(temp_dir)
        APP.init_variables()
    else:
        APP.write_to_text_area(MSG["git_fetching_updates"])
        prev_dir = os.getcwd()
        os.chdir(game_dir)
        try:
        # repo = git.Repo(game_dir)
        # origin = repo.remotes.origin
        # origin.fetch()
        # repo.head.reset('origin/main', index=True, working_tree=True)
            subprocess.run(["git", "fetch", "origin"], shell=False, creationflags=CREATION_FLAGS)
            subprocess.run(["git", "reset", "--hard", "origin/main"], shell=False, creationflags=CREATION_FLAGS)
        finally:
            os.chdir(prev_dir)

    APP.write_to_text_area(MSG["git_cleaning_files"])
    # repo.git.clean('-fd')
    subprocess.run(["git", "clean", "-fd"], shell=False, creationflags=CREATION_FLAGS)
    APP.write_to_text_area(MSG["git_update_completed"])

def get_git_branch(game_dir):
    prev_dir = os.getcwd()
    os.chdir(game_dir)
    # repo = git.Repo(game_dir)
    # return repo.active_branch.name
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                                         stderr=subprocess.DEVNULL).decode().strip()
        return branch
    except Exception:
        return None
    finally:
        os.chdir(prev_dir)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



# region GLOBAL VARIABLES

LANG = get_system_language()
MSG = MESSAGES[LANG]
APP = None

def check_git():
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError as e:
        return False

def install_git():
    winget_path = shutil.which("winget")
    if not winget_path:
        return False
    try:
        process = subprocess.run(
            ["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        return False

def ensure_git_installed():
    if not check_git():
        success = install_git()
        messagebox.showinfo("GIT", MSG["git_restart_required"])
        os._exit(0)
        if success:
            return check_git()
        else:
            return False
    return True

ensure_git_installed()
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = r"C:\\Program Files\\Git\bin\\git.exe"



# region APPLICATION

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(MSG["app_title"])

        self.init_variables()
        self.build_gui()

    def init_variables(self):
        try:
            self.game_path, self.game_exe_path = self.find_game_directory(with_exe_path=True)
        except TypeError:
            self.select_game_directory()
            self.game_path, self.game_exe_path = self.find_game_directory(with_exe_path=True)


        if self.game_path is not None:
            self.is_git_installed = check_git()
            self.is_repository_installed = os.path.exists(os.path.join(self.game_path, ".git"))
            self.config_path = os.path.join(self.game_path, "BepInEx", "config")
            self.external_mods_path = os.path.join(self.game_path, "BepInEx", "plugins", "externals")
            os.makedirs(self.config_path, exist_ok=True)
            os.makedirs(self.external_mods_path, exist_ok=True)
            if self.is_git_installed and self.is_repository_installed:
                self.config_files = [f for f in os.listdir(self.config_path) if f.endswith(".cfg")]
                self.external_mods_file = os.path.join(self.game_path, "external_mods.txt")
                self.installed_mods_file = os.path.join(self.game_path, "installed_mods.txt")
                self.installed_mods = self.read_installed_mods()
                self.current_branch = get_git_branch(self.game_path)
                self.toggle_state = self.current_branch != "nomod"
                threading.Thread(target=self.check_updates).start()
            else:
                self.toggle_state = False
        


    def build_gui(self):
        self.geometry("600x400")
        self.resizable(False, False)
        self.iconbitmap(get_resource_path("logo.ico"))
        
        self.attributes('-alpha', 0.95)

        self.bg_image = Image.open(get_resource_path("src/background.png"))
        self.bg_image = self.bg_image.resize((600, 400))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        

        # text_frame = tk.Frame(self, bg="#2c2f33")
        self.text_frame = tk.Frame(self, bg="")
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 60))

        self.copy_label = tk.Label(self, text="", fg="green", bg="#23272a", font=("Arial", 10, "bold"))
        self.copy_label.pack(pady=5, before=self.text_frame)
        

        self.text_area = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD, height=10, bg="#23272a", fg="white")
        self.text_area.bind("<Button-1>", self.highlight_line)
        self.text_area.bind("<Double-Button-1>", self.copy_selected_text)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.tag_configure("gray", foreground="gray")
        self.text_area.tag_configure("red", foreground="red")
        self.text_area.tag_configure("green", foreground="green")
        

        self.update_button = tk.Button(self, text=MSG["app_button_update"], command=self.update_action, height=2, width=12)
        self.update_button.place(x=200, y=350)

        self.start_button = tk.Button(self, text=MSG["app_button_start"], command=self.start_action, height=2, width=12)
        self.start_button.place(x=320, y=350)

        self.settings_button_image = Image.open(get_resource_path("src/settings.png"))
        self.settings_button_image = self.settings_button_image.resize((40, 40))
        self.settings_button_photo = ImageTk.PhotoImage(self.settings_button_image)
        self.settings_button = tk.Button(self, text="Ayarlar", command=self.open_settings, image=self.settings_button_photo, borderwidth=2, highlightthickness=0, background="black")
        self.settings_button.place(x=550, y=350)

        self.game_dir_button_image = Image.open(get_resource_path("src/directory.png"))
        self.game_dir_button_image = self.game_dir_button_image.resize((40, 40))
        self.game_dir_button_photo = ImageTk.PhotoImage(self.game_dir_button_image)
        self.game_dir_button = tk.Button(self, text="Dizin", command=self.open_game_folder, image=self.game_dir_button_photo, borderwidth=2, highlightthickness=0, background="black")
        self.game_dir_button.place(x=490, y=350)

        self.open_image = Image.open(get_resource_path("src/toggle_button_on.png"))
        self.closed_image = Image.open(get_resource_path("src/toggle_button_off.png"))
        self.open_image = self.open_image.resize((45, 25))
        self.closed_image = self.closed_image.resize((45, 25))
        self.open_photo = ImageTk.PhotoImage(self.open_image)
        self.closed_photo = ImageTk.PhotoImage(self.closed_image)
        self.toggle_button = tk.Button(self, image=self.closed_photo, command=self.toggle_button_action, borderwidth=2, highlightthickness=0, background="black")
        self.toggle_button.place(x=540, y=7)
        if self.toggle_state: 
            self.toggle_button.config(image=self.open_photo)
        else: 
            self.toggle_button.config(image=self.closed_photo)


        if self.game_path is None:
            self.write_to_text_area(MSG["game_directory_path_not_found"], "red")

        if not self.is_git_installed:
            self.write_to_text_area(MSG["mod_start_install"])

    def toggle_button_action(self):
        # repo = git.Repo(self.game_path)
        self.toggle_state = not self.toggle_state
        self.toggle_button.config(state="disabled")
        if self.toggle_state:
            self.toggle_button.config(image=self.open_photo)
            self.write_to_text_area(MSG["mod_pack_activated"], "green")
            # repo.git.checkout("main")
            
            subprocess.run(["git", "reset", "--hard", "origin/main"], shell=False, creationflags=CREATION_FLAGS)
            subprocess.run(["git", "clean", "-fd"], shell=False, creationflags=CREATION_FLAGS)
            subprocess.run(["git", "checkout", "main"], shell=False, creationflags=CREATION_FLAGS)
        else:
            self.toggle_button.config(image=self.closed_photo)
            self.write_to_text_area(MSG["mod_pack_deactivated"], "red")
            # repo.git.checkout("nomod")
            
            subprocess.run(["git", "reset", "--hard", "origin/main"], shell=False, creationflags=CREATION_FLAGS)
            subprocess.run(["git", "clean", "-fd"], shell=False, creationflags=CREATION_FLAGS)
            subprocess.run(["git", "checkout", "nomod"], shell=False, creationflags=CREATION_FLAGS)
        self.toggle_button.config(state="active")

    def open_game_folder(self):
        if self.game_path is not None:
            os.startfile(self.game_path)

    def open_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title(MSG["settings"])
        settings_window.geometry("600x400")
        
        list_frame = tk.Frame(settings_window)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        list_scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        file_listbox = tk.Listbox(list_frame, height=20, yscrollcommand=list_scroll.set)
        list_scroll.config(command=file_listbox.yview)

        file_listbox.pack(side=tk.LEFT, fill=tk.Y)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        file_listbox.bind("<<ListboxSelect>>", lambda event: self.load_config_file(event, settings_window))
        
        for file in self.config_files:
            file_listbox.insert(tk.END, file)
        
        self.config_frame = tk.Frame(settings_window)
        self.config_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    def load_config_file(self, event, settings_window):
        selected_index = event.widget.curselection()
        if not selected_index:
            return
        selected_file = event.widget.get(selected_index)
        file_path = os.path.join(self.config_path, selected_file)
        self.display_config_values(file_path, settings_window)

    def display_config_values(self, file_path, settings_window):
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        
        parser = configparser.ConfigParser()
        parser.read(file_path)

        canvas = tk.Canvas(self.config_frame)
        scrollbar = tk.Scrollbar(self.config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row = 0
        for section in parser.sections():
            tk.Label(scrollable_frame, text=f"[{section}]", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            row += 1
            for key, value in parser.items(section):
                tk.Label(scrollable_frame, text=key).grid(row=row, column=0, sticky="w", padx=5, pady=2)
                entry = tk.Entry(scrollable_frame)
                entry.insert(0, value)
                entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                row += 1

        button_frame = tk.Frame(self.config_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        save_button = tk.Button(button_frame, text=MSG["save"], command=lambda: self.save_config(file_path, scrollable_frame))
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = tk.Button(button_frame, text=MSG["cancel"], command=settings_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def save_config(self, file_path, scrollable_frame):
        parser = configparser.ConfigParser()
        parser.read(file_path)

        row = 0
        for section in parser.sections():
            row += 1
            for key in parser[section]:
                entry = scrollable_frame.grid_slaves(row=row, column=1)[0]  # Entry nesnesini al
                parser[section][key] = entry.get()
                row += 1
        
        with open(file_path, 'w') as configfile:
            parser.write(configfile)


    def copy_selected_text(self, event):
        try:
            self.text_area.tag_remove("sel", "1.0", tk.END) 
            self.text_area.tag_add("sel", "current linestart", "current lineend")
            
            selected_text = self.text_area.get("sel.first", "sel.last")
            
            if selected_text:  
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                self.update_idletasks()
                self.copy_label.config(text=MSG["app_selection_copied"], fg="green")
                self.after(2000, lambda: self.copy_label.config(text=""))
        except tk.TclError:
            pass

    def highlight_line(self, event):
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        current_line = self.text_area.index(tk.CURRENT).split(".")[0]
        line_start = f"{current_line}.0"
        line_end = f"{current_line}.end"
        self.text_area.tag_add("highlight", line_start, line_end)
        self.text_area.tag_configure("highlight", background="green", foreground="black")
        # self.after(1000, lambda: self.text_area.tag_remove("highlight", line_start, line_end))

    def write_to_text_area_from_async(self, messages, color=None):
        self.after(0, self.write_to_text_area, messages, color)

    def write_to_text_area(self, messages, color=None):
        self.text_area.config(state=tk.NORMAL)
        if isinstance(messages, str):
            self.text_area.insert(tk.END, f"{messages}\n", color)
        else:
            for message in messages:
                self.text_area.insert(tk.END, f"{message}\n", color)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def write_to_text_area_last_row(self, message, color=None):
        self.text_area.config(state=tk.NORMAL)
        lines = self.text_area.get("1.0", tk.END).splitlines()
        if lines:
            lines[-1] = message
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "\n".join(lines))
        else:
            self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)
        self.text_area.update_idletasks()
        self.text_area.config(state=tk.DISABLED)

    def start_action(self):
        if not self.game_exe_path:
            self.write_to_text_area(MSG["game_exe_path_not_found"], "red")
            return
        self.write_to_text_area(MSG["game_found"])
        try:
            self.write_to_text_area(MSG["starting_game"])
            subprocess.Popen(["start", f"steam://run/{STEAM_APP_ID}"], shell=True, creationflags=CREATION_FLAGS)
        except Exception as e:
            self.write_to_text_area(MSG["game_start_failed"].format(e), "red")
            self.write_to_text_area(str(e), "red")


    def update_action(self):
        if not self.game_path:
            self.write_to_text_area(MSG["game_directory_path_not_found"], "red")
            return
        if not self.is_git_installed:
            self.write_to_text_area(MSG["git_install"])
            install_git()
            self.write_to_text_area(MSG["git_installation_complete"])
            self.init_variables()
        fetch_origin_and_reset_local_repo(self.game_path)
        
        self.config_files = [f for f in os.listdir(self.config_path) if f.endswith(".cfg")]
        self.external_mods_file = os.path.join(self.game_path, "external_mods.txt")
        self.installed_mods_file = os.path.join(self.game_path, "installed_mods.txt")
        self.installed_mods = self.read_installed_mods()
        self.current_branch = get_git_branch(self.game_path)
        self.toggle_state = self.current_branch != "nomod"
        self.clean_external_mods()

        thread = threading.Thread(target=self.install_external_mods, daemon=True).start()

    def select_game_directory(self):
        messagebox.showinfo(MSG["app_title"], MSG["select_game_manual_prompt"])
        
        selected_dir = filedialog.askdirectory(title=MSG["select_game_folder_dialog_title"])
        exe_name = "REPO.exe"
        exe_path = os.path.join(selected_dir, exe_name)

        if not os.path.exists(exe_path):
            messagebox.showerror(MSG["app_title"], MSG["invalid_directory_selected"].format(exe_name))
            self.select_game_directory()
            return

        try:
            reg_path = r"System\GameConfigStore\Children\FurkiREPO"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
                winreg.SetValueEx(key, "ExeParentDirectory", 0, winreg.REG_SZ, selected_dir)
                winreg.SetValueEx(key, "MatchedExeFullPath", 0, winreg.REG_SZ, exe_path)
            messagebox.showinfo(MSG["app_title"], MSG["game_path_saved_success"])
            return True
        except Exception as e:
            messagebox.showerror(MSG["app_title"], MSG["game_path_save_error"].format(e))
            return False


    def find_game_directory(self, with_exe_path = False, search_value = "REPO"):
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "System\\GameConfigStore\\Children")
        for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
            subkey_name = winreg.EnumKey(reg_key, i)
            subkey = winreg.OpenKey(reg_key, subkey_name)
            try:
                exe_parent_dir = winreg.QueryValueEx(subkey, "ExeParentDirectory")[0]
                if search_value.lower() in exe_parent_dir.lower():
                    matched_exe_full_path = winreg.QueryValueEx(subkey, "MatchedExeFullPath")[0]
                    if with_exe_path:
                        return os.path.dirname(matched_exe_full_path), matched_exe_full_path
                    return os.path.dirname(matched_exe_full_path)
            except FileNotFoundError:
                continue
        return None



    def clean_external_mods(self):

        self.installed_mods = self.read_installed_mods()
        if os.path.exists(self.external_mods_file):
            with open(self.external_mods_file, "r", encoding="utf-8") as f:
                allowed_mods = {line.split(";")[0].strip() for line in f if line.strip()}
        else:
            allowed_mods = set()


        installed_mods_to_remove = {mod for mod in self.installed_mods if mod not in allowed_mods}
        folders_to_remove = {folder for folder in os.listdir(self.external_mods_path) if folder not in allowed_mods}


        for folder in folders_to_remove:
            shutil.rmtree(os.path.join(self.external_mods_path, folder))
        for mod_to_remove in installed_mods_to_remove:
            self.installed_mods.pop(mod_to_remove)

        self.write_installed_mods()

    def install_external_mods(self):
        self.installed_mods = self.read_installed_mods()
        if not os.path.exists(self.external_mods_path):
            os.makedirs(self.external_mods_path)
        
        if not os.path.exists(self.external_mods_file):
            self.write_to_text_area(MSG["mods_file_not_found"])
            return

        with open(self.external_mods_file, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) != 3:
                    continue
                
                mod_name, version, url = parts
                mod_path = os.path.join(self.external_mods_path, mod_name)
                
                if mod_name in self.installed_mods and self.installed_mods[mod_name] == version:
                    self.write_to_text_area(MSG["mod_already_updated"].format(mod_name))
                    continue
                
                self.write_to_text_area(MSG["downloading"].format(mod_name))
                zip_path = os.path.join(self.game_path, f"{mod_name}.zip")
                
                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                if response.status_code == 200:
                    with open(zip_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=65536):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk) 
                                    
                                if total_size > 0:
                                    percent_complete = (downloaded_size / total_size) * 100
                                    self.write_to_text_area_last_row(f"İndirme ilerlemesi: %{percent_complete:.2f}")
                    self.write_to_text_area(MSG["download_completed"])
                    self.write_to_text_area(MSG["extracting"].format(mod_name))
                            
                    if os.path.exists(mod_path):
                        shutil.rmtree(mod_path)
                        os.makedirs(mod_path)
                    extract_zip(zip_path, mod_path)
                    os.remove(zip_path)
                    self.installed_mods[mod_name] = version
                    self.write_to_text_area(MSG["installed_successfully"].format(mod_name))

                else:
                    self.write_to_text_area(MSG["download_failed"].format(mod_name), "red")

        self.write_installed_mods()
        self.write_to_text_area(MSG["mod_install_complete"])


    def read_installed_mods(self):
        installed_mods = {}
        if os.path.exists(self.installed_mods_file):
            with open(self.installed_mods_file, "r") as f:
                for line in f:
                    parts = line.strip().split(";")
                    if len(parts) == 2:
                        installed_mods[parts[0]] = parts[1]
        return installed_mods

    def write_installed_mods(self):
        with open(self.installed_mods_file, "w") as f:
            for mod_name, version in self.installed_mods.items():
                f.write(f"{mod_name};{version}\n")

    def check_for_modloader_updates(self):
        response = requests.get(UPDATE_CHECK_URL)
        result = False, CURRENT_VERSION_URL
        if response.status_code == 200:
            release = response.json()
            asset_url = release['assets'][0]['browser_download_url']
            asset_id = release['assets'][0]['id']
            download_url = asset_url
            if download_url != CURRENT_VERSION_URL:
                result = True, download_url
        return result

    def print_modloader_update_status(self):
        self.write_to_text_area_from_async(MSG["modloader_update_checking"])
        is_available, url = self.check_for_modloader_updates()
        if is_available:
            self.write_to_text_area_from_async(MSG["modloader_update_available"])
            self.write_to_text_area_from_async(MSG["modloader_update_download"].format(url), "green")
        else:
            self.write_to_text_area_from_async(MSG["modloader_uptodate"], "gray")


    def check_for_modpack_updates(self):

        os.chdir(self.game_path)

        # local commit
        local_commit_hash = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, creationflags=CREATION_FLAGS)
        if local_commit_hash.returncode == 0:
            local_commit_hash = local_commit_hash.stdout.strip()
        else:
            return False
        # remote commit
        remote_commit_hash = subprocess.run(["git", "ls-remote", "origin", "main"], capture_output=True, text=True, creationflags=CREATION_FLAGS)
        if remote_commit_hash.returncode == 0:
            remote_commit_hash = remote_commit_hash.stdout.split()[0]
        else:
            return False
        
        if local_commit_hash is None or remote_commit_hash is None:
            return False
        
        return local_commit_hash != remote_commit_hash



    def print_modpack_update_status(self):
        self.write_to_text_area_from_async(MSG["modpack_update_checking"])
        if self.check_for_modpack_updates():
            self.write_to_text_area_from_async(MSG["modpack_update_available"])
            self.write_to_text_area_from_async(MSG["modpack_update_download"], "green")
        else:
            self.write_to_text_area_from_async(MSG["modpack_uptodate"], "gray")

    def check_updates(self):
        self.write_to_text_area_from_async(MSG["updates_checking"])
        self.print_modloader_update_status()
        self.print_modpack_update_status()

        

def main():
    global APP
    APP = App()
    APP.mainloop()
        

if __name__ == "__main__":
    main()
    
