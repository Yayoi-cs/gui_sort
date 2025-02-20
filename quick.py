import tkinter as tk
import random

def swap(data, i, j):
    data[i], data[j] = data[j], data[i]

def quickSort(data, l: int, r: int):
    tl: int = l
    tr: int = r
    pvt = data[(l + r) // 2]
    yield ("pivot", (l + r) // 2)
    while True:
        while data[tl] < pvt:
            yield ("compare_left", tl, pvt)
            tl += 1
            yield ("update", data, l, r, tl, tr, pvt)
        while pvt < data[tr]:
            yield ("compare_right", tr, pvt)
            tr -= 1
            yield ("update", data, l, r, tl, tr, pvt)
        if tl >= tr:
            yield ("partition_done", l, r, tl, tr)
            break
        yield ("swap", tl, tr)
        swap(data, tl, tr)
        yield ("update", data, l, r, tl, tr, pvt)
        tl += 1
        tr -= 1
        yield ("update", data, l, r, tl, tr, pvt)
    if l < tr:
        yield from quickSort(data, l, tr)
    if tr + 1 < r:
        yield from quickSort(data, tr + 1, r)

def drawArray(canvas, data, event=None, pivot_index=None):
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
            if event[0] in ("compare_left", "compare_right") and i == event[1]:
                color = "red"
            elif event[0] == "swap" and (i == event[1] or i == event[2]):
                color = "orange"
            elif event[0] == "update":
                cl = event[1]
                cr = event[2]
                if i == cl:
                    color = "purple"
                elif i == cr:
                    color = "yellow"
            elif event[0] == "pivot" and i == event[1]:
                if color == "blue":
                    color = "green"
        if color == "blue" and pivot_index is not None and i == pivot_index:
            color = "green"

        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(val), font=("Arial", 10))
    canvas.update()

class QuickSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()

        self.data = [random.randint(10, 400) for _ in range(20)]
        self.gen = quickSort(self.data, 0, len(self.data) - 1)
        self.current_event = None
        self.pivot = None

        drawArray(self.canvas, self.data, pivot_index=self.pivot)

    def step(self):
        try:
            self.current_event = next(self.gen)
            if self.current_event[0] == "pivot":
                self.pivot = self.current_event[1]
            drawArray(self.canvas, self.data, self.current_event, pivot_index=self.pivot)
            self.root.after(100, self.step)
        except StopIteration:
            drawArray(self.canvas, self.data, pivot_index=None)
            print("[*]finish")

def main():
    root = tk.Tk()
    root.title("Quick Sort Visualizer")
    visualizer = QuickSortVisualizer(root)
    root.after(100, visualizer.step)
    root.mainloop()

if __name__ == "__main__":
    main()
