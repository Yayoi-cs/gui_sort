import tkinter as tk
import random

def insertionSort(data):
    n = len(data)
    for i in range(1,n):
        for j in range(i-1,0,-1):
            yield ("compare", j, j-1)
            if data[j] < data[j-1]:
                yield ("swap", j, j-1)
                data[j], data[j-1] = data[j-1], data[j]
                yield ("update", data)
            else:
                break
    yield ("done", data)

def drawArray(canvas, data, event=None):
    canvas.delete("all")
    width = int(canvas['width'])
    height = int(canvas['height'])
    n = len(data)
    bar_width = width / n
    max_val = max(data) if data else 1

    for i, val in enumerate(data):
        x0 = i * bar_width
        y0 = height - (val / max_val * (height - 20))
        x1 = (i + 1) * bar_width
        y1 = height

        color = "blue"
        if event:
            if event[0] == "compare" and (i == event[1] or i == event[2]):
                color = "red"
            elif event[0] == "swap" and (i == event[1] or i == event[2]):
                color = "orange"

        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(val), font=("Arial", 10))
    canvas.update()

class InsertionSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()
        
        self.data = [random.randint(10, 400) for _ in range(20)]
        self.gen = insertionSort(self.data)
        self.current_event = None

        drawArray(self.canvas, self.data)

    def step(self):
        try:
            self.current_event = next(self.gen)
            drawArray(self.canvas, self.data, self.current_event)
            self.root.after(100, self.step)
        except StopIteration:
            drawArray(self.canvas, self.data)
            print("[*] Sorting finished")

def main():
    root = tk.Tk()
    root.title("Bubble Sort Visualizer")
    visualizer = InsertionSortVisualizer(root)
    root.after(100, visualizer.step)
    root.mainloop()

if __name__ == "__main__":
    main()
