import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from organizer import organize_files
import threading
from pathlib import Path
import shutil
# Importamos THEME_PALETTES para gestionar ambos temas
from palette import THEME_PALETTES, LIGHT_PALETTE
from translations import TRANSLATIONS


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.lang = "es"  # default language
        self.root.title(TRANSLATIONS[self.lang]["ui"]["title"])
        self.root.geometry("650x580") 
        self.last_moves = []  # [(dest_final, origen_inicial), ...]

        # State variables
        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.lang_var = tk.StringVar(value="Español")
        self.current_theme = tk.StringVar(value="light")
        self.palette = THEME_PALETTES[self.current_theme.get()]

        # UI setup
        self._build_ui()
        self._setup_style(self.palette)
        self._apply_language_texts()

    # --------- Styling (MEJORADO para Modo Oscuro) ---------
    def _setup_style(self, PALETTE):
        # Configura el color de fondo de la ventana
        self.root.configure(bg=PALETTE["bg"])
        style = ttk.Style()
        style.theme_use("clam")

        # Configuración de estilos generales
        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("Surface.TFrame", 
                        background=PALETTE["surface"], 
                        relief="flat", 
                        borderwidth=1)
        
        # Mapeo para añadir borde visual
        style.map("Surface.TFrame",
                  background=[("active", PALETTE["surface"])])

        # Etiquetas
        style.configure("TLabel",
                        background=PALETTE["bg"],
                        foreground=PALETTE["fg"],
                        font=("Inter", 10))
        style.configure("Muted.TLabel",
                        background=PALETTE["bg"],
                        foreground=PALETTE["muted"],
                        font=("Inter", 9))
        style.configure("Surface.TLabel",
                        background=PALETTE["surface"],
                        foreground=PALETTE["fg"],
                        font=("Inter", 10))
        style.configure("Title.TLabel",
                        background=PALETTE["bg"],
                        foreground=PALETTE["fg"],
                        font=("Inter", 16, "bold"))

        # Entradas de Texto - Configuración mejorada
        style.configure("TEntry", 
                        fieldbackground=PALETTE["surface"], 
                        foreground=PALETTE["fg"],
                        bordercolor=PALETTE["border"],
                        lightcolor=PALETTE["border"],
                        darkcolor=PALETTE["border"],
                        insertcolor=PALETTE["fg"],
                        padding=(8, 6))
        
        style.map("TEntry", 
                  fieldbackground=[("readonly", PALETTE["surface"]), ("disabled", PALETTE["bg"])],
                  foreground=[("disabled", PALETTE["muted"])],
                  bordercolor=[("focus", PALETTE["accent"])])

        # Botones principales
        style.configure("TButton",
                        font=("Inter", 10),
                        padding=(12, 8),
                        relief="flat",
                        borderwidth=0,
                        background=PALETTE["surface"],
                        foreground=PALETTE["fg"])
        
        style.map("TButton",
                  background=[("active", PALETTE["border"]), ("pressed", PALETTE["border"])],
                  foreground=[("disabled", PALETTE["muted"])])
                        
        style.configure("Primary.TButton",
                        font=("Inter", 10, "bold"),
                        background=PALETTE["primary"],
                        foreground="#FFFFFF",
                        padding=(15, 10))

        style.map("Primary.TButton",
                  background=[("active", PALETTE["primary_hover"]), 
                             ("pressed", PALETTE["primary_hover"]),
                             ("disabled", PALETTE["muted"])],
                  foreground=[("disabled", PALETTE["fg"])]) 
        
        # Botón de Alternancia de Tema
        style.configure("Theme.TButton",
                        background=PALETTE["surface"],
                        foreground=PALETTE["fg"],
                        padding=(10, 8),
                        borderwidth=1,
                        relief="flat",
                        font=("Segoe UI Emoji", 12))
        
        style.map("Theme.TButton",
                  background=[("active", PALETTE["border"])],
                  relief=[("pressed", "sunken")])

        # Barra de Progreso
        style.configure("Accent.Horizontal.TProgressbar",
                        troughcolor=PALETTE["trough"],
                        background=PALETTE["accent"],
                        lightcolor=PALETTE["accent"],
                        darkcolor=PALETTE["accent"],
                        bordercolor=PALETTE["border"],
                        borderwidth=0,
                        thickness=8)
        
        # Combobox - Configuración mejorada
        style.configure("TCombobox", 
                        fieldbackground=PALETTE["surface"], 
                        selectbackground=PALETTE["accent"],
                        selectforeground="#FFFFFF",
                        foreground=PALETTE["fg"],
                        background=PALETTE["surface"],
                        arrowcolor=PALETTE["fg"],
                        bordercolor=PALETTE["border"],
                        lightcolor=PALETTE["border"],
                        darkcolor=PALETTE["border"],
                        padding=(8, 6))
        
        style.map("TCombobox",
                  fieldbackground=[("readonly", PALETTE["surface"])],
                  selectbackground=[("readonly", PALETTE["accent"])],
                  bordercolor=[("focus", PALETTE["accent"])],
                  arrowcolor=[("disabled", PALETTE["muted"])])
        
        # Configura el área de log
        if hasattr(self, 'log_text'):
            self.log_text.config(
                bg=PALETTE["surface"],
                fg=PALETTE["fg"],
                insertbackground=PALETTE["fg"],
                selectbackground=PALETTE["accent"],
                selectforeground="#FFFFFF",
                highlightbackground=PALETTE["border"],
                highlightcolor=PALETTE["accent"],
                highlightthickness=1
            )
        
        # Actualizar el dropdown del Combobox (listbox)
        self.root.option_add("*TCombobox*Listbox.background", PALETTE["surface"])
        self.root.option_add("*TCombobox*Listbox.foreground", PALETTE["fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", PALETTE["accent"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")
             
    def toggle_theme(self):
        """Alterna entre el modo claro y oscuro y reaplica los estilos."""
        current = self.current_theme.get()
        new_theme = "dark" if current == "light" else "light"
        
        self.current_theme.set(new_theme)
        self.palette = THEME_PALETTES[new_theme]
        
        # Actualizar el texto del botón de tema
        self.theme_button.config(text="☀️" if new_theme == "dark" else "🌙")
        
        # Reaplica todos los estilos
        self._setup_style(self.palette)

    # --------- Build UI ---------
    def _build_ui(self):
        # Top bar with title, language, and theme selector
        top = ttk.Frame(self.root, style="TFrame")
        top.pack(fill="x", padx=24, pady=(20, 10))

        self.title_label = ttk.Label(top, text="", style="Title.TLabel")
        self.title_label.pack(side="left")

        # Contenedor para idioma y tema
        controls_frame = ttk.Frame(top, style="TFrame")
        controls_frame.pack(side="right")
        
        # Botón de Tema
        theme_text = "🌙" if self.current_theme.get() == "light" else "☀️"
        self.theme_button = ttk.Button(controls_frame, 
                                       text=theme_text,
                                       command=self.toggle_theme,
                                       style="Theme.TButton",
                                       width=3)
        self.theme_button.pack(side="right", padx=(10, 0))

        # Selector de Idioma
        lang_frame = ttk.Frame(controls_frame, style="TFrame")
        lang_frame.pack(side="right")
        
        self.lang_label = ttk.Label(lang_frame, text="", style="TLabel")
        self.lang_label.pack(side="left", padx=(0, 8))

        languages = ["English", "Español", "Français", "Deutsch", "Italiano", "Português"]
        self.lang_map = {
            "English": "en",
            "Español": "es",
            "Français": "fr",
            "Deutsch": "de",
            "Italiano": "it",
            "Português": "pt",
        }
        self.lang_combo = ttk.Combobox(lang_frame, 
                                       values=languages, 
                                       state="readonly", 
                                       width=12, 
                                       textvariable=self.lang_var)
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_changed)
        self.lang_combo.pack(side="left")

        # Form card
        card = ttk.Frame(self.root, style="Surface.TFrame")
        card.pack(fill="x", padx=24, pady=10, ipadx=16, ipady=16)

        # Source
        self.source_label = ttk.Label(card, text="", style="Surface.TLabel")
        self.source_label.grid(row=0, column=0, sticky="w", padx=(12, 12), pady=(8, 4))
        self.source_entry = ttk.Entry(card, textvariable=self.source_folder, width=50)
        self.source_entry.grid(row=1, column=0, sticky="we", padx=12, pady=(0, 4))
        self.source_browse = ttk.Button(card, text="", command=self.select_source, style="TButton")
        self.source_browse.grid(row=1, column=1, padx=(8, 12), pady=(0, 4))

        # Destination
        self.dest_label = ttk.Label(card, text="", style="Surface.TLabel")
        self.dest_label.grid(row=2, column=0, sticky="w", padx=(12, 12), pady=(12, 4))
        self.dest_entry = ttk.Entry(card, textvariable=self.dest_folder, width=50)
        self.dest_entry.grid(row=3, column=0, sticky="we", padx=12, pady=(0, 8))
        self.dest_browse = ttk.Button(card, text="", command=self.select_dest, style="TButton")
        self.dest_browse.grid(row=3, column=1, padx=(8, 12), pady=(0, 8))

        card.grid_columnconfigure(0, weight=1)

        # Actions
        btn_frame = ttk.Frame(self.root, style="TFrame")
        btn_frame.pack(pady=15)
        self.organize_button = ttk.Button(
            btn_frame,
            text="",
            style="Primary.TButton",
            command=self.start_organizing,
            width=22
        )
        self.organize_button.grid(row=0, column=0, padx=10)

        self.undo_button = ttk.Button(
            btn_frame,
            text="",
            command=self.start_undo,
            state=tk.DISABLED,
            width=22
        )
        self.undo_button.grid(row=0, column=1, padx=10)

        # Progress
        self.progress = ttk.Progressbar(self.root, length=500, mode="determinate", style="Accent.Horizontal.TProgressbar")
        self.progress.pack(pady=15)

        # Log area
        log_wrapper = ttk.Frame(self.root, style="Surface.TFrame")
        log_wrapper.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self.log_text = tk.Text(
            log_wrapper,
            height=12,
            bd=0,
            highlightthickness=1,
            relief="flat",
            font=("Consolas", 9),
            padx=8,
            pady=8,
            wrap=tk.WORD
        )
        self.log_text.pack(fill="both", expand=True, padx=12, pady=12)

    # --------- i18n helpers ---------
    def _t(self, section: str, key: str, **kwargs) -> str:
        lang = self.lang
        text = TRANSLATIONS.get(lang, {}).get(section, {}).get(key)
        if text is None:
            text = TRANSLATIONS["en"][section].get(key, key)
        return text.format(**kwargs) if kwargs else text

    def _apply_language_texts(self):
        self.root.title(self._t("ui", "title"))
        self.title_label.config(text=self._t("ui", "title"))
        self.lang_label.config(text=self._t("ui", "language") + ":")
        self.source_label.config(text=self._t("ui", "source"))
        self.source_browse.config(text=self._t("ui", "browse"))
        self.dest_label.config(text=self._t("ui", "destination"))
        self.dest_browse.config(text=self._t("ui", "browse"))
        self.organize_button.config(text=self._t("ui", "organize"))
        self.undo_button.config(text=self._t("ui", "undo"))

    def _on_language_changed(self, _evt=None):
        human = self.lang_var.get()
        self.lang = self.lang_map.get(human, "en")
        self._apply_language_texts()

    # --------- UI actions ---------
    def select_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_folder.set(folder)

    def select_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_folder.set(folder)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.yview(tk.END)

    def update_progress(self, value):
        self.progress["value"] = value * 100
        self.root.update_idletasks()

    def start_organizing(self):
        if not self.source_folder.get():
            messagebox.showerror(self._t("msg", "error_title"), self._t("msg", "please_select_source"))
            return
        self.organize_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_organizer, daemon=True).start()

    def run_organizer(self):
        self.progress["value"] = 0
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        self.undo_button.config(state=tk.DISABLED)

        try:
            moves = organize_files(
                self.source_folder.get(),
                self.dest_folder.get() if self.dest_folder.get() else None,
                progress_callback=self.update_progress,
                log_callback=self.log,
                messages=TRANSLATIONS[self.lang]["organizer"],
            )
            self.last_moves = moves or []
            if self.last_moves:
                self.undo_button.config(state=tk.NORMAL)
            messagebox.showinfo(self._t("msg", "done_title"), self._t("msg", "done_body"))
        except Exception as e:
            messagebox.showerror(self._t("msg", "error_title"), str(e))
        finally:
            self.organize_button.config(state=tk.NORMAL)

    # -------- Undo logic --------
    def _unique_destination(self, path: Path) -> Path:
        if not path.exists():
            return path
        i = 1
        while True:
            candidate = path.with_name(f"{path.stem} ({i}){path.suffix}")
            if not candidate.exists():
                return candidate
            i += 1

    def start_undo(self):
        if not self.last_moves:
            messagebox.showinfo(self._t("msg", "nothing_to_undo_title"), self._t("msg", "nothing_to_undo_body"))
            return
        
        self.undo_button.config(state=tk.DISABLED)
        self.organize_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_undo, daemon=True).start()

    def run_undo(self):
        try:
            total = len(self.last_moves)
            if total == 0:
                return

            self.progress["value"] = 0
            self.log_text.config(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state="disabled")
            self.log(self._t("msg", "undo_start"))

            for i, (dest_final, origen_inicial) in enumerate(reversed(self.last_moves), start=1):
                dest_path = Path(dest_final)
                orig_path = Path(origen_inicial)
                try:
                    if dest_path.exists():
                        orig_path.parent.mkdir(parents=True, exist_ok=True)
                        move_target = self._unique_destination(orig_path)
                        shutil.move(str(dest_path), str(move_target))
                        self.log(self._t("msg", "restored", name=move_target.name, folder=orig_path.parent.name))
                    else:
                        self.log(self._t("msg", "skipped_missing", name=dest_path.name))
                except Exception as ex:
                    self.log(self._t("msg", "error_restoring", name=dest_path.name, error=str(ex)))

                self.update_progress(i / total)

            self.last_moves = []
            messagebox.showinfo(self._t("msg", "undo_complete_title"), self._t("msg", "undo_complete_body"))
        except Exception as e:
            messagebox.showerror(self._t("msg", "error_title"), str(e))
        finally:
            self.undo_button.config(state=tk.DISABLED)
            self.organize_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()