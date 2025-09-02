import os
import re
import requests
from io import BytesIO
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import sys

# ------------------ Helper Functions ------------------

def extract_image_links(readme_path):
    """Extract all https image links from a README.md file."""
    with open(readme_path, "r", encoding="utf-8") as f:
        contents = f.read()
    return re.findall(r"(https://[^\s)]+\.png)", contents)


def fetch_image(url, size=(120, 120)):
    """Download image from URL and return a Tkinter-compatible thumbnail."""
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
        img.thumbnail(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def _on_mousewheel(event, canvas):
    """Scroll canvas vertically with mouse wheel (Windows/macOS/Linux)."""
    if event.num == 4:   # Linux scroll up
        canvas.yview_scroll(-1, "units")
    elif event.num == 5: # Linux scroll down
        canvas.yview_scroll(1, "units")
    else:  # Windows/macOS
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def make_scrollable_frame(parent, width=500, height=620):
    """Create a scrollable frame inside a canvas."""
    canvas = tk.Canvas(parent, width=width, height=height)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview, width=40)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bind mouse wheel directly to the canvas
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: _on_mousewheel(ev, canvas)))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<Button-4>", lambda ev: _on_mousewheel(ev, canvas)))
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<Button-5>", lambda ev: _on_mousewheel(ev, canvas)))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<Button-4>"))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<Button-5>"))

    return canvas, scroll_frame


def find_file_by_number(folder_path, number):
    """Find a file in folder_path whose filename contains the given number."""
    for f in os.listdir(folder_path):
        if number in f:
            return os.path.normpath(os.path.join(folder_path, f))
    return None


def open_in_explorer(path):
    """Open File Explorer highlighting the file (Windows/macOS/Linux)."""
    path = os.path.abspath(path)
    path = os.path.normpath(path)
    if sys.platform.startswith("win"):
        subprocess.run(["explorer", "/select,", path])
    elif sys.platform.startswith("darwin"):
        subprocess.run(["open", "-R", path])
    else:
        subprocess.run(["xdg-open", os.path.dirname(path)])


# ------------------ Tertiary Window ------------------

def show_subfolder_images(folder_name, links, folder_path):
    """Level 3 window: shows all images in a chromas subfolder."""
    top = tk.Toplevel(root)
    top.title(folder_name)
    canvas, scroll_frame = make_scrollable_frame(top)

    for url in links:
        frame = tk.Frame(scroll_frame, pady=5)
        frame.pack(fill="x", padx=10)

        img = fetch_image(url, size=(200, 200))
        if img:
            img_label = tk.Label(frame, image=img, cursor="hand2")
            img_label.image = img
            img_label.pack(side="left")
            img_label.bind("<Button-1>", lambda e, u=url, p=folder_path: on_image_click(u, p))

        file_name = os.path.basename(url)

        file_label = tk.Label(frame, text=file_name, font=("Corbel", 14), cursor="hand2")
        file_label.pack(side="left", padx=10)
        file_label.bind("<Button-1>", lambda e, u=url, p=folder_path: on_image_click(u, p))


def on_image_click(url, folder_path):
    match = re.search(r"/(\d+)\.png$", url)
    number = match.group(1) if match else None
    if number:
        file_path = find_file_by_number(folder_path, number)
        if file_path:
            print(f"Clicked image corresponds to file: {file_path}")
            open_in_explorer(file_path)
        else:
            print(f"No matching file found in {folder_path} for number {number}")
    else:
        print("Could not extract number from URL:", url)


# ------------------ Secondary Window ------------------

def show_main_folder(main_folder_name, main_folder_path):
    """Level 2 window: shows all chromas subfolders in a main folder."""
    top = tk.Toplevel(root)
    top.title(main_folder_name)
    canvas, container = make_scrollable_frame(top)

    chromas_path = os.path.join(main_folder_path, "chromas")
    if not os.path.isdir(chromas_path):
        return

    for child in os.listdir(chromas_path):
        child_path = os.path.join(chromas_path, child)
        if os.path.isdir(child_path):
            readme_path = os.path.join(child_path, "README.md")
            if os.path.isfile(readme_path):
                links = extract_image_links(readme_path)
                if links:
                    first_img = fetch_image(links[0], size=(230, 257))
                    frame = tk.Frame(container, pady=5)
                    frame.pack(fill="x", padx=10, anchor="w")

                    if first_img:
                        img_label = tk.Label(frame, image=first_img)
                        img_label.image = first_img
                        img_label.pack(side="left")

                    btn = tk.Button(
                        frame,
                        text=child,
                        font=("Corbel", 16),
                        cursor="hand2",
                        command=lambda c=child, l=links, p=child_path: show_subfolder_images(c, l, p)
                    )
                    btn.pack(side="left", padx=10)


# ------------------ Main Window ------------------

main_folder_buttons = []  # Keep references to buttons for search

def on_drop(event):
    super_folder_path = event.data.strip("{}")

    # --- Check if dropped item is a valid super folder ---
    if not os.path.isdir(super_folder_path):
        messagebox.showerror("Error", "Please drag the main 'skins' folder containing all champion skins. from the darkseal-org/lol-skins/ github.")  # Not a folder
        return

    # Check if it contains at least one main folder with a 'chromas' folder
    valid = False
    for main_folder_name in os.listdir(super_folder_path):
        main_folder_path = os.path.join(super_folder_path, main_folder_name)
        chromas_path = os.path.join(main_folder_path, "chromas")
        if os.path.isdir(main_folder_path) and os.path.isdir(chromas_path):
            valid = True
            break

    if not valid:
        messagebox.showerror("Error", "stop")  # Folder structure invalid
        return

    # --- Clear previous buttons ---
    for widget in container.winfo_children():
        widget.destroy()
    main_folder_buttons.clear()

    # --- Populate main folder buttons ---
    for main_folder_name in os.listdir(super_folder_path):
        main_folder_path = os.path.join(super_folder_path, main_folder_name)
        chromas_path = os.path.join(main_folder_path, "chromas")
        if os.path.isdir(main_folder_path) and os.path.isdir(chromas_path):
            btn = tk.Button(
                container,
                text=main_folder_name,
                font=("Corbel", 18),
                cursor="hand2",
                width=40,
                command=lambda n=main_folder_name, p=main_folder_path: show_main_folder(n, p)
            )
            btn.pack(pady=10)
            main_folder_buttons.append(btn)


# ------------------ GUI Setup ------------------

root = TkinterDnD.Tk()

root.title("LOL Chroma Browser")
root.geometry("620x790")
root.resizable(False, False)
try:
    img = Image.open("assets/terry.png")
    icon = ImageTk.PhotoImage(img)
    root.iconphoto(True, icon)
except:
    pass  # Ignore if icon not found

label = ttk.Label(root, text="LOL Chroma Browser", font=("Corbel", 22, "bold"))
label.pack(pady=5)

label = ttk.Label(root, text="By: Mariusz T.", font=("Corbel", 11))
label.pack(pady=1)

label = ttk.Label(root, text="Drag Skins Folder:", font=("Corbel", 16))
label.pack(pady=1)

# --- Scrollable frame for main folder buttons ---
scroll_frame_holder = tk.Frame(root)
scroll_frame_holder.pack(side="top", fill="both", expand=True)

canvas, container = make_scrollable_frame(scroll_frame_holder)

canvas.drop_target_register(DND_FILES)
canvas.dnd_bind("<<Drop>>", on_drop)

# --- Fixed search bar at bottom ---
search_frame = tk.Frame(root)
search_frame.pack(side="bottom", fill="x", pady=5)

search_label = tk.Label(search_frame, text="Search Champion:", font=("Corbel", 14))
search_label.pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, font=("Corbel", 14))
search_entry.pack(side="left", fill="x", expand=True, padx=5)

search_btn = tk.Button(search_frame, cursor="hand2", text="Search", bg="lightblue", font=("Corbel", 14), command=lambda: on_search())
search_btn.pack(side="left", padx=5)

# ------------------ Partial Search Function ------------------

def on_search(event=None):
    query = search_entry.get().lower()
    canvas.update_idletasks()  # Ensure layout is updated
    for btn in main_folder_buttons:
        folder_name = btn.cget("text").lower()
        if query in folder_name:  # Partial match
            y = btn.winfo_y()
            total_height = container.winfo_height()
            if total_height > 0:
                fraction = y / total_height
                canvas.yview_moveto(fraction)
            break  # Stop at first match

search_entry.bind("<Return>", on_search)

root.mainloop()
