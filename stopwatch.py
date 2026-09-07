import tkinter as tk

root = tk.Tk()

root.title("Stopwatch")
root.geometry("300x180")
root.resizable(False, False)
root.configure(bg="#0a0a1a")

running = False
counter = 0
job = None


def update_time():
    global counter, job

    minutes, seconds = divmod(counter // 60, 60)
    milliseconds = counter % 60

    time_label.config(
        text=f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
    )

    if running:
        counter += 1
        job = root.after(10, update_time)


def start():
    global running

    if not running:
        running = True
        update_time()


def stop():
    global running, job

    running = False

    if job is not None:
        root.after_cancel(job)
        job = None


def reset():
    global counter, running, job

    running = False
    counter = 0

    if job is not None:
        root.after_cancel(job)
        job = None

    time_label.config(text="00:00:00")


title_label = tk.Label(
    root,
    text="Stopwatch",
    font=("Consolas", 16, "bold"),
    bg="#0a0a1a",
    fg="#00ffff"
)

title_label.pack(pady=(10, 0))


time_label = tk.Label(
    root,
    text="00:00:00",
    font=("ds-digital", 50, "bold"),
    fg="#39ff14",
    bg="#0a0a1a"
)

time_label.pack(pady=10)


frame = tk.Frame(root, bg="#0a0a1a")
frame.pack()


tk.Button(
    frame,
    text="▶ START",
    command=start,
    font=("Consolas", 12),
    bg="#00ffaa",
    fg="black",
    relief="flat",
    padx=10
).pack(side=tk.LEFT, padx=5)


tk.Button(
    frame,
    text="⏸ STOP",
    command=stop,
    font=("Consolas", 12),
    bg="#ff5555",
    fg="white",
    relief="flat",
    padx=10
).pack(side=tk.LEFT, padx=5)


tk.Button(
    frame,
    text="↻ RESET",
    command=reset,
    font=("Consolas", 12),
    bg="#ffaa00",
    fg="black",
    relief="flat",
    padx=10
).pack(side=tk.LEFT, padx=5)


root.mainloop()