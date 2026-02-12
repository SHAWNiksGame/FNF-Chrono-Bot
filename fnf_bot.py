import os
import json
import time
import keyboard
import sys
from colorama import init, Fore, Style

init()

# --- Configuration ---
SETTINGS_FILE = "settings.json"
KEYS = {0: 'left', 1: 'down', 2: 'up', 3: 'right'}

# --- Localization ---
LANGUAGES = {
    "en": {
        "title": "=== FNF ULTIMATE CHRONO BOT ===",
        "select_lang": "Select Language (en/ru/ua): ",
        "path_prompt": "Enter FNF assets/data path: ",
        "path_error": "Path not found!",
        "song_list": "Select a song:",
        "diff_list": "Select difficulty:",
        "notes_loaded": "Notes loaded: ",
        "how_to": "Press [{key}] when the first arrow reaches the gray arrow center!",
        "active": ">>> BOT ACTIVE! (Press [{key}] to stop) <<<",
        "finished": "Finished! Returning to menu...",
        "set_lang": "[L] Language",
        "set_path": "[P] Path",
        "set_binds": "[K] Keybinds",
        "exit": "[E] Exit",
        "goodbye": "Goodbye!",
        "bind_start": "Enter new START key: ",
        "bind_stop": "Enter new STOP key: "
    },
    "ru": {
        "title": "=== FNF ULTIMATE CHRONO BOT ===",
        "select_lang": "Выберите язык (en/ru/ua): ",
        "path_prompt": "Введите путь к assets/data: ",
        "path_error": "Путь не найден!",
        "song_list": "Выберите песню:",
        "diff_list": "Выберите сложность:",
        "notes_loaded": "Загружено нот: ",
        "how_to": "Нажмите [{key}], когда первая стрелка будет в центре серой стрелки!",
        "active": ">>> БОТ ВКЛЮЧЕН! (Нажми [{key}] для стопа) <<<",
        "finished": "Готово! Возврат в меню...",
        "set_lang": "[L] Язык",
        "set_path": "[P] Путь",
        "set_binds": "[K] Бинды",
        "exit": "[E] Выход",
        "goodbye": "До встречи!",
        "bind_start": "Введите новую клавишу СТАРТА: ",
        "bind_stop": "Введите новую клавишу СТОПА: "
    },
    "ua": {
        "title": "=== FNF ULTIMATE CHRONO BOT ===",
        "select_lang": "Оберіть мову (en/ru/ua): ",
        "path_prompt": "Введіть шлях до assets/data: ",
        "path_error": "Шлях не знайдено!",
        "song_list": "Оберіть пісню:",
        "diff_list": "Оберіть складність:",
        "notes_loaded": "Завантажено нот: ",
        "how_to": "Натисніть [{key}], коли перша стрілка буде в центрі сірої стрілки!",
        "active": ">>> БОТ ПРАЦЮЄ! (Тисни [{key}] для зупинки) <<<",
        "finished": "Готово! Повернення в меню...",
        "set_lang": "[L] Мова",
        "set_path": "[P] Шлях",
        "set_binds": "[K] Бінди",
        "exit": "[E] Вихід",
        "goodbye": "До зустрічі!",
        "bind_start": "Введіть нову клавішу СТАРТУ: ",
        "bind_stop": "Введіть нову клавішу СТОПУ: "
    }
}

class ChronoBot:
    def __init__(self):
        self.settings = self.load_settings()
        self.lang = LANGUAGES.get(self.settings.get("lang", "en"), LANGUAGES["en"])

    def load_settings(self):
        defaults = {"lang": "en", "game_path": "", "start_key": "1", "stop_key": "delete"}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    defaults.update(data)
                except: pass
        return defaults

    def save_settings(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def select_language(self):
        print(LANGUAGES["en"]["select_lang"])
        l = input("> ").lower()
        if l in LANGUAGES:
            self.settings["lang"] = l
            self.lang = LANGUAGES[l]
            self.save_settings()

    def update_path(self):
        print("\n" + self.lang["path_prompt"])
        p = input("> ").strip().strip('"')
        if os.path.exists(p):
            self.settings["game_path"] = p
            self.save_settings()
        else:
            print(Fore.RED + self.lang["path_error"] + Style.RESET_ALL)
            time.sleep(1)

    def update_binds(self):
        print("\n" + self.lang["bind_start"] + f"(Current: {self.settings['start_key']})")
        s = input("> ").lower()
        if s: self.settings["start_key"] = s
        print("\n" + self.lang["bind_stop"] + f"(Current: {self.settings['stop_key']})")
        st = input("> ").lower()
        if st: self.settings["stop_key"] = st
        self.save_settings()

    def get_notes(self, path, song):
        song_dir = os.path.join(path, song)
        try:
            files = [f for f in os.listdir(song_dir) if f.endswith('.json')]
            print("\n" + self.lang["diff_list"])
            for i, f in enumerate(files): print(f"{i+1}. {f}")
            choice = int(input("> ")) - 1
            with open(os.path.join(song_dir, files[choice]), 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            song_data = data.get("song", data)
            notes = []
            for section in song_data.get("notes", []):
                must_hit = section.get("mustHitSection", False)
                for n in section.get("sectionNotes", []):
                    t, d, l = n[0], int(n[1]), n[2]
                    is_player = (must_hit and 0 <= d <= 3) or (not must_hit and 4 <= d <= 7)
                    if is_player and (len(n) < 4 or n[3] is None or n[3] == 0):
                        notes.append({"t": t, "d": d % 4, "l": l})
            notes.sort(key=lambda x: x["t"])
            return notes
        except: return None

    def start_engine(self, notes):
        s_key = self.settings["start_key"]
        stop_key = self.settings["stop_key"]
        
        time.sleep(0.3)
        print("\n" + Fore.YELLOW + self.lang["how_to"].format(key=s_key) + Style.RESET_ALL)
        
        while True:
            if keyboard.is_pressed(s_key): break
            time.sleep(0.005)
            
        start_ts = time.perf_counter() * 1000
        # Tiny 5ms compensation for system latency
        offset = start_ts - notes[0]['t'] + 5 
        
        print(Fore.MAGENTA + self.lang["active"].format(key=stop_key) + Style.RESET_ALL)
        
        idx, total = 0, len(notes)
        holds = [] # (release_time, key)
        
        try:
            while idx < total or holds:
                now = (time.perf_counter() * 1000) - offset
                
                # 1. Release notes
                for h in holds[:]:
                    if now >= h[0]:
                        keyboard.release(h[1])
                        holds.remove(h)
                
                # 2. Press new notes
                if idx < total:
                    note = notes[idx]
                    if now >= note['t']:
                        key_name = KEYS[note['d']]
                        
                        # --- FIX FOR LOW FPS & RAPID NOTES ---
                        # 1. If key is already held, force release it for a new tap
                        for h in holds[:]:
                            if h[1] == key_name:
                                keyboard.release(key_name)
                                holds.remove(h)
                        
                        # 2. Press key
                        keyboard.press(key_name)
                        
                        # 3. Minimum hold duration (35ms) to ensure 60fps game registers it
                        # FNF Sick window is ~45ms, so 35ms is safe and perfect.
                        duration = note['l'] if note['l'] > 35 else 35
                        holds.append((now + duration, key_name))
                        
                        idx += 1
                        continue 
                
                if keyboard.is_pressed(stop_key): break
                if idx < total and (notes[idx]['t'] - now) > 2:
                    time.sleep(0.0001)
        except: pass
        
        for _, k in holds: keyboard.release(k)
        print("\n" + self.lang["finished"])
        time.sleep(1.5)

    def run(self):
        if not self.settings.get("lang_set"):
            self.select_language()
            self.settings["lang_set"] = True
            self.save_settings()
        if not self.settings.get("game_path"): self.update_path()
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.CYAN + self.lang["title"] + Style.RESET_ALL)
            path = self.settings.get("game_path")
            
            try:
                songs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
                print("\n" + self.lang["song_list"])
                for i, s in enumerate(songs): print(str(i+1) + ". " + s)
            except:
                print(Fore.RED + "Path Error!" + Style.RESET_ALL)
                self.update_path(); continue

            print(f"\n{self.lang['set_lang']} | {self.lang['set_path']} | {self.lang['set_binds']} | {self.lang['exit']}")
            
            cmd = input("> ").lower()
            if cmd == 'e':
                print(Fore.GREEN + self.lang["goodbye"] + Style.RESET_ALL)
                time.sleep(1)
                os._exit(0)
            if cmd == 'l': self.select_language(); continue
            if cmd == 'p': self.update_path(); continue
            if cmd == 'k': self.update_binds(); continue
            
            try:
                notes = self.get_notes(path, songs[int(cmd)-1])
                if notes:
                    print(Fore.GREEN + self.lang["notes_loaded"] + str(len(notes)) + Style.RESET_ALL)
                    self.start_engine(notes)
            except: pass

if __name__ == "__main__":
    ChronoBot().run()
