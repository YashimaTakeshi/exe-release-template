import tkinter as tk
from tkinter import ttk

try:
    from build_info import VERSION, BUILT_AT
except ImportError:
    VERSION, BUILT_AT = "dev", "ローカル実行"

root = tk.Tk()
root.title("Hello EXE")
root.geometry("360x170")

frm = ttk.Frame(root, padding=24)
frm.pack(fill="both", expand=True)
ttk.Label(frm, text="exeのビルドに成功しました", font=("Meiryo UI", 13)).pack()
ttk.Label(frm, text=f"{VERSION} / {BUILT_AT}", foreground="#666666").pack(pady=(8, 18))
ttk.Button(frm, text="閉じる", command=root.destroy).pack()

root.mainloop()
