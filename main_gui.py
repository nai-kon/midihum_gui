import os
import subprocess
import threading

import customtkinter as tk

from midihum_model import MidihumModel

if __name__ == "__main__":

    DISP_IDENT_OUTDIR = "output: "
    model = MidihumModel()

    def worker(paths, output_dir):
        prog_bar.set(0)

        for i, path in enumerate(paths, start=1):
            fname = os.path.basename(path)
            status_label.configure(text=f"{i}/{len(paths)} processing...{fname}")
            outpath = os.path.join(output_dir, fname)
            model.humanize(path, outpath)
            prog_bar.set(i / len(paths))
            
        sel_outdir_btn.configure(state=tk.NORMAL)
        sel_files_btn.configure(state=tk.NORMAL)
        subprocess.Popen(["explorer", os.path.abspath(output_dir)], shell=True)
        status_label.configure(text=status_label.cget("text").replace("processing", "finished"))

    def dirsel():
        output_dir = tk.filedialog.askdirectory(mustexist=True)
        if output_dir != "":
            sel_outdir_label.configure(text=DISP_IDENT_OUTDIR + output_dir)

    def pathsel():
        output_dir = sel_outdir_label.cget("text").lstrip(DISP_IDENT_OUTDIR)
        if output_dir == "":
            status_label.configure(text="Please select output folder firstly")
            return

        paths = tk.filedialog.askopenfilenames(filetypes=[("mid", "*.mid")])
        if len(paths) == 0:
            return

        prog_bar.set(0)
        sel_outdir_btn.configure(state=tk.DISABLED)
        sel_files_btn.configure(state=tk.DISABLED)
        threading.Thread(target=worker, args=(paths, output_dir)).start()

    app = tk.CTk()
    app.title("midihum with GUI")
    app.resizable(False, False)
    app.geometry("600x140")

    sel_outdir_btn = tk.CTkButton(app, text="Select output folder", command=dirsel)
    sel_outdir_btn.pack()
    sel_outdir_label = tk.CTkLabel(app, text=DISP_IDENT_OUTDIR)
    sel_outdir_label.pack()
    sel_files_btn = tk.CTkButton(app, text="Select input midi files", command=pathsel)
    sel_files_btn.pack()
    status_label = tk.CTkLabel(app, text="")
    status_label.pack()
    prog_bar = tk.CTkProgressBar(app, width=550)
    prog_bar.set(0)
    prog_bar.pack()

    app.mainloop()