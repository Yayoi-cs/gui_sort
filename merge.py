import tkinter as tk
import random

def mergeSort(data, left, right):
    if left >= right:
        return
    mid = (left + right) // 2
    yield from mergeSort(data, left, mid)
    yield from mergeSort(data, mid + 1, right)
    yield from merge(data, left, mid, right)

def merge(data, left, mid, right):
    temp = data[left:right + 1]
    i, j = 0, mid - left + 1
    k = left
    while i <= mid - left and j <= right - left:
        yield ("compare", k, left + j)
        if temp[i] <= temp[j]:
            data[k] = temp[i]
            i += 1
        else:
            data[k] = temp[j]
            j += 1
        k += 1
    while i <= mid - left:
        yield ("compare", k, left + i)
        data[k] = temp[i]
        i += 1
        k += 1
    while j <= right - left:
        yield ("compare", k, left + j)
        data[k] = temp[j]
        j += 1
        k += 1
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
            elif event[0] == "update":
                color = "orange"

        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(val), font=("Arial", 10))
    canvas.update()

class MergeSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()
        
        self.data = [random.randint(10, 400) for _ in range(20)]
        self.gen = mergeSort(self.data, 0, len(self.data) - 1)
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
    root.title("Merge Sort Visualizer")
    visualizer = MergeSortVisualizer(root)
    root.after(100, visualizer.step)
    root.mainloop()

if __name__ == "__main__":
    main()

