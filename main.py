import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

CONFIG_PATH = os.path.expanduser("~/.r6s_settings_tool.cfg")
SETTINGS_FILENAME = "GameSettings.ini"


SERVERS = [
    ("Default", "default"),
    ("West US", "playfab/westus"),
    ("Central US", "playfab/centralus"),
    ("South Central US", "playfab/southcentralus"),
    ("East US", "playfab/eastus"),
    ("West Europe", "playfab/westeurope"),
    ("North Europe", "playfab/northeurope"),
    ("East Asia", "playfab/eastasia"),
    ("Southeast Asia", "playfab/southeastasia"),
    ("Japan East", "playfab/japaneast"),
    ("South Africa North", "playfab/southafricanorth"),
    ("Australia East", "playfab/australiaeast"),
    ("Brazil South", "playfab/brazilsouth"),
    ("UAE North", "playfab/uaenorth"),
]

def is_process_running(exe_name: str) -> bool:
    try:
        out = subprocess.check_output(
            ["tasklist", "/FO", "CSV", "/NH", "/FI", f"IMAGENAME eq {exe_name}"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True,
            errors="ignore",
        )
        return exe_name.lower() in out.lower()
    except Exception:
        return False

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            folder = f.readline().strip()
            if folder and os.path.exists(os.path.join(folder, SETTINGS_FILENAME)):
                return folder
    return None

def save_config(folder: str):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(folder.strip() + "\n")

def load_settings_fp(folder):
    return os.path.join(folder, SETTINGS_FILENAME)

def parse_settings(path):
    multiplier = None
    region = None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("MouseSensitivityMultiplierUnit="):
                multiplier = line.strip().split("=", 1)[1]
            if line.strip().startswith("DataCenterHint="):
                region = line.strip().split("=", 1)[1]
    return multiplier, region

def update_settings(path, multiplier=None, region=None):
    lines = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if multiplier is not None and line.startswith("MouseSensitivityMultiplierUnit="):
                lines.append(f"MouseSensitivityMultiplierUnit={multiplier}\n")
            elif region is not None and line.strip().startswith("DataCenterHint="):
                lines.append(f"DataCenterHint={region}\n")
            else:
                lines.append(line)
    with open(path, "w", encoding="utf-8", errors="ignore") as f:
        f.writelines(lines)

BG = "#121212"
PANEL = "#1E1E1E"
BTN = "#2A2A2A"
BTN_HOVER = "#333333"
FG = "#EAEAEA"
MUTED = "#B0B0B0"
ACCENT = "#3A86FF"
ACCENT_HOVER = "#4B97FF"

def apply_dark_theme(root: tk.Tk):
    root.configure(bg=BG)
    root.option_add("*Background", BG)
    root.option_add("*Foreground", FG)
    root.option_add("*Button.Background", BTN)
    root.option_add("*Button.Foreground", FG)
    root.option_add("*Label.Background", BG)
    root.option_add("*Label.Foreground", FG)

def set_button_hover(btn: tk.Button, *, normal_bg=BTN, hover_bg=BTN_HOVER):
    def on_enter(_):
        btn.configure(bg=hover_bg)
    def on_leave(_):
        btn.configure(bg=normal_bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def set_selected_accent_hover(btn: tk.Button):
    def on_enter(_):
        btn.configure(bg=ACCENT_HOVER)
    def on_leave(_):
        btn.configure(bg=ACCENT)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.configure(activebackground=ACCENT_HOVER)

def format_privacy_path(folder: str) -> str:
    if not folder:
        return SETTINGS_FILENAME
    folder_name = os.path.basename(os.path.normpath(folder)) or folder
    parent_name = os.path.basename(os.path.dirname(os.path.normpath(folder))) or ""
    if parent_name:
        return f"...{os.sep}{parent_name}{os.sep}{folder_name}{os.sep}{SETTINGS_FILENAME}"
    return f"...{os.sep}{folder_name}{os.sep}{SETTINGS_FILENAME}"

def center_window(root: tk.Tk):
    root.update_idletasks()

    w = root.winfo_width()
    h = root.winfo_height()

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = (sw - w) // 2
    y = (sh - h) // 2

    root.geometry(f"{w}x{h}+{x}+{y}")

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.folder = None
        self.settings_path = None

        self.root.title("R6S Settings Tool")
        self.root.geometry("600x400")
        self.root.minsize(600, 400)

        apply_dark_theme(self.root)

        self.container = tk.Frame(root, bg=BG)
        self.container.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.container,
            text="R6S Settings Tool",
            font=("Segoe UI", 18, "bold"),
            bg=BG,
            fg=FG
        )
        self.title_label.pack(pady=(18, 6))

        self.status_label = tk.Label(
            self.container,
            text="",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        )
        self.status_label.pack(pady=(0, 6))

        self.current_label = tk.Label(
            self.container,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=FG
        )
        self.current_label.pack(pady=(0, 14))

        self.panel = tk.Frame(self.container, bg=BG)
        self.panel.pack(fill="both", expand=True, padx=22, pady=6)

        self.btn_sens = tk.Button(
            self.panel,
            text="Change Sensitivity Multiplier",
            font=("Segoe UI", 14, "bold"),
            bg=BTN,
            fg=FG,
            activebackground=BTN_HOVER,
            activeforeground=FG,
            relief="flat",
            bd=0,
            height=3,
            command=self.change_sensitivity
        )
        self.btn_sens.pack(fill="x", pady=(0, 12))
        set_button_hover(self.btn_sens)

        self.btn_region = tk.Button(
            self.panel,
            text="Change Server Region",
            font=("Segoe UI", 14, "bold"),
            bg=BTN,
            fg=FG,
            activebackground=BTN_HOVER,
            activeforeground=FG,
            relief="flat",
            bd=0,
            height=3,
            command=self.change_region
        )
        self.btn_region.pack(fill="x")
        set_button_hover(self.btn_region)

        self.bottom = tk.Frame(self.container, bg=BG)
        self.bottom.pack(fill="x", side="bottom", padx=10, pady=10)

        self.btn_folder = tk.Button(
            self.bottom,
            text="Change settings folder…",
            font=("Segoe UI", 9),
            bg=BTN,
            fg=FG,
            activebackground=BTN_HOVER,
            activeforeground=FG,
            relief="flat",
            bd=0,
            padx=10,
            pady=6,
            command=self.change_folder
        )
        self.btn_folder.pack(side="left")
        set_button_hover(self.btn_folder)

        self.hint = tk.Label(
            self.bottom,
            text="PRESS ESCAPE TO CLOSE",
            font=("Segoe UI", 9),
            bg=BG,
            fg=MUTED
        )
        self.hint.pack(side="right")

        self.ensure_folder(startup=True)

    def refresh_ui(self):
        if self.folder and self.settings_path and os.path.exists(self.settings_path):
            self.status_label.configure(text=f"Config: {format_privacy_path(self.folder)}")
            multiplier, region = parse_settings(self.settings_path)

            multiplier_txt = multiplier if multiplier is not None else "(not found)"
            region_txt = region if region is not None else "(not found)"

            friendly_region = region_txt
            if region is not None:
                for label, value in SERVERS:
                    if value == region:
                        friendly_region = label
                        break

            self.current_label.configure(
                text=f"Current Multiplier: {multiplier_txt}    |    Current Region: {friendly_region}"
            )
        else:
            self.status_label.configure(text="Config: (not set)")
            self.current_label.configure(text="Current Multiplier: -    |    Current Region: -")

    def ensure_folder(self, startup=False):
        folder = load_config()
        if folder and os.path.exists(load_settings_fp(folder)):
            self.folder = folder
            self.settings_path = load_settings_fp(folder)
            self.refresh_ui()
            return True

        if startup:
            messagebox.showinfo("Select Folder", "Select your R6S settings folder (must contain GameSettings.ini).")
        return self.change_folder()

    def change_folder(self):
        folder = filedialog.askdirectory(title="Select R6S Settings Folder")
        if not folder:
            return False

        settings_path = load_settings_fp(folder)
        if not os.path.exists(settings_path):
            messagebox.showerror("Error", f"{SETTINGS_FILENAME} not found in selected folder.")
            return False

        save_config(folder)
        self.folder = folder
        self.settings_path = settings_path
        self.refresh_ui()
        return True

    def _ask_multiplier(self, current_multiplier: str | None):
        dlg = tk.Toplevel(self.root)
        dlg.title("Sensitivity")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)

        dlg.transient(self.root)
        dlg.grab_set()

        result = {"value": None}

        def close():
            try:
                dlg.grab_release()
            except tk.TclError:
                pass
            dlg.destroy()

        dlg.protocol("WM_DELETE_WINDOW", close)
        dlg.bind("<Escape>", lambda _e: close())

        title = tk.Label(
            dlg,
            text="Mouse Sensitivity Multiplier",
            font=("Segoe UI", 13, "bold"),
            bg=BG,
            fg=FG
        )
        title.pack(padx=16, pady=(14, 6))

        entry = tk.Entry(dlg, font=("Segoe UI", 12), relief="flat", bg=BTN, fg=FG, insertbackground=FG)
        entry.pack(padx=16, pady=(0, 12), fill="x")
        if current_multiplier:
            entry.insert(0, current_multiplier)
            entry.selection_range(0, "end")
        entry.focus_set()

        btn_row = tk.Frame(dlg, bg=BG)
        btn_row.pack(padx=16, pady=(0, 14), fill="x")

        def ok():
            value = entry.get().strip()
            if value == "":
                return
            result["value"] = value
            close()

        cancel_btn = tk.Button(
            btn_row, text="Cancel",
            font=("Segoe UI", 10, "bold"),
            bg=BTN, fg=FG, activebackground=BTN_HOVER, activeforeground=FG,
            relief="flat", bd=0, padx=10, pady=8,
            command=close
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
        set_button_hover(cancel_btn)

        ok_btn = tk.Button(
            btn_row, text="Apply",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT, fg=FG, activeforeground=FG,
            relief="flat", bd=0, padx=10, pady=8,
            command=ok
        )
        ok_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))
        set_selected_accent_hover(ok_btn)

        dlg.bind("<Return>", lambda _e: ok())

        dlg.update_idletasks()
        w = dlg.winfo_width()
        h = dlg.winfo_height()
        sw = dlg.winfo_screenwidth()
        sh = dlg.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        dlg.geometry(f"{w}x{h}+{x}+{y}")

        dlg.wait_window()
        return result["value"]

    def _ask_region_buttons(self, current_region: str | None):
        dlg = tk.Toplevel(self.root)
        dlg.title("Server Region")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)

        dlg.transient(self.root)
        dlg.grab_set()

        result = {"value": None}

        def close():
            try:
                dlg.grab_release()
            except tk.TclError:
                pass
            dlg.destroy()

        dlg.protocol("WM_DELETE_WINDOW", close)
        dlg.bind("<Escape>", lambda _e: close())

        title = tk.Label(
            dlg,
            text="Select Server Region",
            font=("Segoe UI", 14, "bold"),
            bg=BG,
            fg=FG
        )
        title.pack(padx=16, pady=(14, 6))

        wrap = tk.Frame(dlg, bg=BG)
        wrap.pack(padx=16, pady=(0, 14), fill="both")

        cols = 2
        for i, (label, value) in enumerate(SERVERS):
            r = i // cols
            c = i % cols

            btn = tk.Button(
                wrap,
                text=label,
                font=("Segoe UI", 11, "bold"),
                bg=BTN,
                fg=FG,
                activebackground=BTN_HOVER,
                activeforeground=FG,
                relief="flat",
                bd=0,
                padx=10,
                pady=10,
                command=lambda v=value: (result.__setitem__("value", v), close())
            )
            btn.grid(row=r, column=c, sticky="ew", padx=6, pady=6)

            if value == current_region:
                btn.configure(bg=ACCENT, activebackground=ACCENT_HOVER)
                set_selected_accent_hover(btn)
            else:
                set_button_hover(btn)

        wrap.grid_columnconfigure(0, weight=1)
        wrap.grid_columnconfigure(1, weight=1)

        dlg.update_idletasks()
        w = dlg.winfo_width()
        h = dlg.winfo_height()
        sw = dlg.winfo_screenwidth()
        sh = dlg.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        dlg.geometry(f"{w}x{h}+{x}+{y}")

        dlg.wait_window()
        return result["value"]

    def change_sensitivity(self):
        if not self.ensure_folder():
            return

        multiplier, _region = parse_settings(self.settings_path)

        new_multiplier = self._ask_multiplier(multiplier)
        if new_multiplier is None or new_multiplier == "":
            return

        update_settings(self.settings_path, multiplier=new_multiplier, region=None)
        self.refresh_ui()

    def change_region(self):
        if not self.ensure_folder():
            return

        _multiplier, region = parse_settings(self.settings_path)

        new_region = self._ask_region_buttons(region)
        if new_region is None or new_region == "":
            return

        update_settings(self.settings_path, multiplier=None, region=new_region)
        self.refresh_ui()

def make_window_draggable(root: tk.Tk):
    root._drag_start_x = 0
    root._drag_start_y = 0

    def on_press(e):
        root._drag_start_x = e.x
        root._drag_start_y = e.y

    def on_drag(e):
        x = root.winfo_x() + (e.x - root._drag_start_x)
        y = root.winfo_y() + (e.y - root._drag_start_y)
        root.geometry(f"+{x}+{y}")

    root.bind("<ButtonPress-1>", on_press)
    root.bind("<B1-Motion>", on_drag)

def main():
    if is_process_running("RainbowSix.exe"):
        tmp = tk.Tk()
        tmp.withdraw()
        messagebox.showerror(
            "Error",
            "Close RainbowSix.exe before using this tool.\n\n"
            "The game must be closed so GameSettings.ini can be edited safely."
        )
        tmp.destroy()
        return

    root = tk.Tk()

    root.overrideredirect(True)
    root.attributes("-topmost", True)

    root.bind("<Escape>", lambda e: root.destroy())
    make_window_draggable(root)

    app = App(root)

    root.update_idletasks()
    root.geometry("600x400")
    center_window(root)

    root.mainloop()

if __name__ == "__main__":
    main()