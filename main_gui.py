import os
import subprocess
import threading
import tkinter as tk
from tkinter import IntVar, filedialog, ttk

from midihum_model import MidihumModel

if __name__ == "__main__":

    DISP_IDENT_OUTDIR = "output: "
    model = MidihumModel()

    def worker(paths, output_dir):
        global pbar
        global pbtn
        global label

        pbar.set(0)

        for i, path in enumerate(paths, start=1):
            fname = os.path.basename(path)
            label["text"] = f"{i}/{len(paths)} processing...{fname}"

            outpath = os.path.join(output_dir, fname)
            model.humanize(path, outpath)
            pbar.set(100 * i / len(paths))
            
        pbtn["state"] = tk.NORMAL
        pbtn2["state"] = tk.NORMAL
        subprocess.Popen(["explorer", os.path.abspath(output_dir)], shell=True)
        label["text"] = label["text"].replace("processing", "finished")

    def dirsel():
        global label_output_dir
        output_dir = filedialog.askdirectory(mustexist=True)
        if output_dir != "":
            label_output_dir["text"] = DISP_IDENT_OUTDIR + output_dir

    def pathsel():
        output_dir = label_output_dir["text"].lstrip(DISP_IDENT_OUTDIR)
        if output_dir == "":
            tk.messagebox.showwarning(title="output folder error", message="Please select output folder firstly")
            return

        paths = filedialog.askopenfilenames(filetypes=[("mid", "*.mid")])
        if len(paths) == 0:
            return
        print(paths)
        global pbar
        pbar.set(0)
        global pbtn
        pbtn["state"] = tk.DISABLED
        pbtn2["state"] = tk.DISABLED
        global th
        th = threading.Thread(target=worker, args=(paths, output_dir))
        th.start()

    baseGround = tk.Tk()
    baseGround.title("midihum with GUI")
    baseGround.geometry("600x140")
    pbtn = tk.Button(baseGround, text="Select output folder", command=dirsel)
    pbtn.pack()
    label_output_dir = tk.Label(text=DISP_IDENT_OUTDIR)
    label_output_dir.pack()
    pbtn2 = tk.Button(baseGround, text="Select input midi files", command=pathsel)
    pbtn2.pack()
    label = tk.Label(text="")
    label.pack()
    pbar = IntVar()
    ttk.Progressbar(baseGround, maximum=100, mode="determinate", length=550, variable=pbar).pack()

    baseGround.mainloop()