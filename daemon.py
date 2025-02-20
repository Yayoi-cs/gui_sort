import tkinter as tk
import subprocess

def run_quick():
    subprocess.Popen(["python3", "quick.py"])

def run_heap():
    subprocess.Popen(["python3", "heap.py"])

def run_selection():
    subprocess.Popen(["python3", "selection.py"])

def run_merge():
    subprocess.Popen(["python3", "merge.py"])

def run_insertion():
    subprocess.Popen(["python3", "insertion.py"])

def run_bubble():
    subprocess.Popen(["python3", "bubble.py"])

def main():
    root = tk.Tk()
    root.title("SortApplication Menu")

    menubar = tk.Menu(root)
    sort_menu = tk.Menu(menubar, tearoff=0)
    sort_menu.add_command(label="Quick Sort", command=run_quick)
    sort_menu.add_command(label="Heap Sort", command=run_heap)
    sort_menu.add_command(label="Selection Sort", command=run_selection)
    sort_menu.add_command(label="Merge Sort", command=run_merge)
    sort_menu.add_command(label="Insertion Sort", command=run_insertion)
    sort_menu.add_command(label="Bubble Sort", command=run_bubble)
    menubar.add_cascade(label="Sort Algorithm", menu=sort_menu)

    root.config(menu=menubar)

    label = tk.Label(root, text="Choose a sort algorithm to run from the menu above.")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
