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
            sel_outdir_btn.configure(text=DISP_IDENT_OUTDIR + output_dir)

    def pathsel():
        output_dir = sel_outdir_btn.cget("text").lstrip(DISP_IDENT_OUTDIR)
        if not os.path.exists(output_dir):
            status_label.configure(text="Please select output folder firstly")
            return

        paths = tk.filedialog.askopenfilenames(filetypes=[("mid", "*.mid")])
        if len(paths) == 0:
            return

        prog_bar.set(0)
        sel_outdir_btn.configure(state=tk.DISABLED)
        sel_files_btn.configure(state=tk.DISABLED)
        threading.Thread(target=worker, args=(paths, output_dir)).start()

    tk.set_default_color_theme("dark-blue")
    app = tk.CTk()
    app.title("midihum with GUI")
    app.resizable(False, False)
    app.geometry("600x180")

    sel_outdir_btn = tk.CTkButton(app, text="Select output folder", fg_color="#343638", border_color="#565B5E", border_width=2, command=dirsel, anchor="w")
    sel_outdir_btn.pack(padx=20, pady=10, fill="x")
    sel_files_btn = tk.CTkButton(app, text="Select input midi files", fg_color="#343638", border_color="#565B5E", border_width=2, command=pathsel, anchor="w")
    sel_files_btn.pack(padx=20, pady=10, fill="x")
    prog_bar = tk.CTkProgressBar(app, mode="determinate")
    prog_bar.set(0)
    prog_bar.pack(padx=20, pady=10, fill="x")
    status_label = tk.CTkLabel(app, text="Select output folder and input files", anchor="w")
    status_label.pack(padx=20, pady=10, fill="x")

    app.mainloop()