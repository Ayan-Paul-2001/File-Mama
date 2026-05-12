import os, sys, shutil, subprocess, ctypes, winreg
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

def get_active_explorer_path():
    try:
        import comtypes.client as cc
        shell = cc.CreateObject("Shell.Application")
        hwnd_fg = ctypes.windll.user32.GetForegroundWindow()
        for w in shell.Windows():
            try:
                if w.HWND == hwnd_fg:
                    loc = w.LocationURL
                    if loc.startswith("file:///"):
                        path = loc[8:].replace("/", "\\").replace("%20", " ")
                        if os.path.isdir(path):
                            return path
            except Exception:
                continue
        for w in shell.Windows():
            try:
                loc = w.LocationURL
                if loc.startswith("file:///"):
                    path = loc[8:].replace("/", "\\").replace("%20", " ")
                    if os.path.isdir(path):
                        return path
            except Exception:
                continue
    except Exception:
        pass
    return None

def get_target_directory():
    path = get_active_explorer_path()
    if path:
        return path, "Active File Explorer window"
    if getattr(sys, 'frozen', False):
        fallback = os.path.dirname(sys.executable)
    else:
        fallback = os.path.dirname(os.path.abspath(__file__))
    return fallback, "Executable's directory (no Explorer window detected)"

CATEGORIES = {
    "Images":       [".jpg",".jpeg",".png",".gif",".bmp",".svg",".webp",
                     ".ico",".tiff",".tif",".raw",".heic",".heif",".avif"],
    "Videos":       [".mp4",".avi",".mkv",".mov",".wmv",".flv",".webm",
                     ".m4v",".mpeg",".mpg",".3gp",".ts",".vob"],
    "Audio":        [".mp3",".wav",".flac",".aac",".ogg",".wma",".m4a",
                     ".opus",".aiff",".ape",".ac3"],
    "Documents":    [".pdf",".doc",".docx",".txt",".odt",".rtf",".tex",
                     ".wpd",".pages",".md",".log"],
    "Spreadsheets": [".xls",".xlsx",".csv",".ods",".numbers",".tsv"],
    "Slides":       [".ppt",".pptx",".odp",".key"],
    "Archives":     [".zip",".rar",".7z",".tar",".gz",".bz2",
                     ".xz",".iso",".cab",".lzh"],
    "Code":         [".py",".js",".ts",".jsx",".tsx",".html",".htm",".css",
                     ".scss",".java",".c",".cpp",".cs",".go",".rb",".php",
                     ".swift",".kt",".rs",".sh",".bat",".ps1",".json",
                     ".xml",".yaml",".yml",".toml",".ini",".cfg",".sql",
                     ".dart",".lua",".r",".m",".h",".hpp"],
    "Executables":  [".exe",".msi",".apk",".dmg",".deb",".rpm",".appimage",".jar"],
    "Fonts":        [".ttf",".otf",".woff",".woff2",".eot"],
    "Design":       [".psd",".ai",".xd",".fig",".sketch",".blend",
                     ".obj",".fbx",".stl",".eps",".indd"],
    "Ebooks":       [".epub",".mobi",".azw",".azw3",".djvu"],
}

def get_category(ext: str) -> str:
    e = ext.lower()
    for cat, exts in CATEGORIES.items():
        if e in exts:
            return cat
    return "Others"

def scan_directory(target_dir: str):
    exe_name = os.path.basename(sys.executable).lower() if getattr(sys,'frozen',False) else ""
    results = []
    for item in Path(target_dir).iterdir():
        if not item.is_file():
            continue
        if item.name.lower() == exe_name:
            continue
        if item.name == "file_mama_log.txt":
            continue
        cat = get_category(item.suffix)
        results.append({
            "name":     item.name,
            "ext":      item.suffix.lower() or "(none)",
            "category": cat,
            "path":     str(item),
        })
    return sorted(results, key=lambda x: x["category"])

def organise(target_dir: str, files: list):
    log_ok, log_err = [], []
    for f in files:
        dest_dir = Path(target_dir) / f["category"]
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f["name"]
        counter = 1
        while dest.exists():
            stem   = Path(f["name"]).stem
            suffix = Path(f["name"]).suffix
            dest   = dest_dir / f"{stem} ({counter}){suffix}"
            counter += 1
        try:
            shutil.move(f["path"], str(dest))
            log_ok.append(f"  ✓  {f['name']}  →  {f['category']}\\")
        except Exception as e:
            log_err.append(f"  ✗  {f['name']}: {e}")
    log_path = Path(target_dir) / "file_mama_log.txt"
    with open(log_path, "w", encoding="utf-8") as lf:
        lf.write(f"File Mama  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lf.write("=" * 60 + "\n\n")
        for l in log_ok:  lf.write(l + "\n")
        if log_err:
            lf.write("\nErrors:\n")
            for e in log_err: lf.write(e + "\n")
    return log_ok, log_err

BG     = "#0A0A0A"
PANEL  = "#111111"
CARD   = "#161616"
ACC    = "#C8FF00"
FG     = "#EFEFEF"
DIM    = "#555555"
ERR    = "#FF4444"
BORDER = "#252525"
MONO   = "Consolas"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.target_dir, self.source_label = get_target_directory()
        self.files = []
        self.title("File Mama")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._build()
        self._scan()
        self._center()

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

    def _label(self, parent, text, font_size=9, bold=False, color=None, **kw):
        weight = "bold" if bold else "normal"
        return tk.Label(parent, text=text,
                        font=(MONO, font_size, weight),
                        bg=kw.pop("bg", BG),
                        fg=color or FG, **kw)

    def _build(self):
        top = tk.Frame(self, bg=BG, padx=24, pady=20)
        top.pack(fill="x")
        self._label(top, "FILE MAMA", 18, bold=True, color=ACC, bg=BG).pack(anchor="w")
        self._label(top, "Organises files by type into sub-folders", 8, color=DIM, bg=BG).pack(anchor="w", pady=(2,0))

        src = tk.Frame(self, bg=CARD, padx=24, pady=10, highlightbackground=BORDER,
                       highlightthickness=1)
        src.pack(fill="x", padx=24)
        self._label(src, "TARGET DIRECTORY", 7, bold=True, color=DIM, bg=CARD).pack(anchor="w")
        self.src_lbl = self._label(src, "", 8, color=ACC, bg=CARD, wraplength=540, justify="left")
        self.src_lbl.pack(anchor="w", pady=(3,0))
        self.src_type = self._label(src, "", 7, color=DIM, bg=CARD)
        self.src_type.pack(anchor="w", pady=(1,0))

        tk.Frame(self, bg=ACC, height=2).pack(fill="x", padx=0, pady=(14,0))

        hdr = tk.Frame(self, bg=PANEL, padx=24, pady=8)
        hdr.pack(fill="x")
        for txt, w in [("FILE NAME",36),("TYPE",7),("→ DESTINATION",20)]:
            self._label(hdr, txt, 7, bold=True, color=DIM, bg=PANEL, width=w, anchor="w").pack(side="left")

        list_wrap = tk.Frame(self, bg=BG)
        list_wrap.pack(fill="both", expand=True, padx=0)
        self.canvas = tk.Canvas(list_wrap, bg=BG, highlightthickness=0, height=300, width=640)
        sb = tk.Scrollbar(list_wrap, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=BG)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))

        stat = tk.Frame(self, bg=PANEL, padx=24, pady=8, highlightbackground=BORDER,
                        highlightthickness=1)
        stat.pack(fill="x")
        self.stat_lbl = self._label(stat, "Scanning…", 8, color=DIM, bg=PANEL)
        self.stat_lbl.pack(anchor="w")

        btn_row = tk.Frame(self, bg=BG, padx=24, pady=18)
        btn_row.pack(fill="x")
        self.run_btn = tk.Button(btn_row, text="▶  ORGANISE NOW",
            font=(MONO,11,"bold"), bg=ACC, fg=BG,
            relief="flat", padx=22, pady=11, cursor="hand2",
            activebackground="#aed600", activeforeground=BG,
            command=self._run)
        self.run_btn.pack(side="left")
        tk.Button(btn_row, text="✕  CANCEL",
            font=(MONO,11,"bold"), bg="#1a1a1a", fg=DIM,
            relief="flat", padx=22, pady=11, cursor="hand2",
            activebackground="#222", command=self.destroy).pack(side="left", padx=(12,0))
        self.note_lbl = self._label(btn_row, "", 7, color=DIM, bg=BG)
        self.note_lbl.pack(side="left", padx=(16,0))

        footer = tk.Frame(self, bg=BG, pady=6)
        footer.pack(fill="x")
        tk.Label(footer, text="Developed by ", font=(MONO, 6), bg=BG, fg="#3a3a3a").pack(side="left", padx=(24,0))
        link = tk.Label(footer, text="Ayan Paul", font=(MONO, 6, "underline"), bg=BG, fg="#4a4a4a", cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: __import__("webbrowser").open("https://ayan-portfolio-dev.vercel.app/"))
        link.bind("<Enter>", lambda e: link.config(fg=DIM))
        link.bind("<Leave>", lambda e: link.config(fg="#4a4a4a"))

    def _scan(self):
        self.src_lbl.config(text=self.target_dir)
        self.src_type.config(text=f"Source: {self.source_label}")
        self.files = scan_directory(self.target_dir)

        for w in self.inner.winfo_children():
            w.destroy()

        if not self.files:
            self._label(self.inner, "No files found in this directory.", 9, color=DIM).pack(pady=30)
            self.run_btn.config(state="disabled")
            self.stat_lbl.config(text="Nothing to organise.")
            return

        cats = {}
        for f in self.files:
            cats[f["category"]] = cats.get(f["category"], 0) + 1

        self.stat_lbl.config(
            text=f"{len(self.files)} file(s)  ·  {len(cats)} folder(s)  ·  "
                 + "  ".join(f"{v}× {k}" for k,v in sorted(cats.items())),
            fg=FG)
        self.note_lbl.config(text="Existing folders will be reused, not duplicated.")

        prev_cat = None
        for i, f in enumerate(self.files):
            if f["category"] != prev_cat:
                div = tk.Frame(self.inner, bg="#1a1a1a")
                div.pack(fill="x")
                self._label(div, f"  {f['category'].upper()}", 7, bold=True,
                            color=ACC, bg="#1a1a1a").pack(side="left", pady=4, padx=20)
                prev_cat = f["category"]

            row_bg = BG if i % 2 == 0 else "#0e0e0e"
            row = tk.Frame(self.inner, bg=row_bg)
            row.pack(fill="x")

            name_txt = f["name"] if len(f["name"]) <= 36 else f["name"][:33] + "…"
            self._label(row, name_txt, 9, color=FG, bg=row_bg,
                        width=36, anchor="w", padx=20, pady=4).pack(side="left")
            self._label(row, f["ext"], 8, color=DIM, bg=row_bg,
                        width=7, anchor="w").pack(side="left")
            self._label(row, f"→  {f['category']}\\", 9, color=ACC,
                        bg=row_bg, anchor="w").pack(side="left")

    def _run(self):
        if not self.files:
            return
        ans = messagebox.askyesno(
            "Confirm",
            f"Organise {len(self.files)} file(s) in:\n\n{self.target_dir}\n\n"
            "Folders will be created only if they don't already exist.\nProceed?")
        if not ans:
            return
        self.run_btn.config(state="disabled", text="Working…")
        self.stat_lbl.config(text="Moving files…", fg=ACC)
        self.update()

        ok, errors = organise(self.target_dir, self.files)

        if errors:
            messagebox.showwarning("Done with errors",
                f"Moved {len(ok)} file(s).\n{len(errors)} error(s).\n\nSee file_mama_log.txt")
        else:
            messagebox.showinfo("Done ✓",
                f"Successfully organised {len(ok)} file(s).\n\nSee file_mama_log.txt for the full list.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
