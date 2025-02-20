import tkinter as tk
import random
import math

mmax = lambda i, j: i if i > j else j
pyrhead = lambda r: 2**r - 1
pyrlow = lambda i: int(math.log2(i+1))
pyrlownum = lambda r: 2**r
pyrchild = lambda i: [2*i+1, 2*i+2]
pyrparent = lambda i: None if i <= 0 else (i-1)//2

WIDTH = 800
HEIGHT = 600
NODE_RADIUS = 20
VERTICAL_SPACING = 80
DELAY = 200

def draw_tree(canvas, data, highlights=set(), swap_highlights=set()):
    canvas.delete("all")
    n = len(data)
    positions = {}
    
    for i in range(n):
        row = pyrlow(i)
        row_nodes = pyrlownum(row)
        pos_in_row = i - pyrhead(row)
        spacing = WIDTH / (row_nodes + 1)
        x = spacing * (pos_in_row + 1)
        y = VERTICAL_SPACING * (row + 1)
        positions[i] = (x, y)
    
    for i in range(n):
        parent = pyrparent(i)
        if parent is not None:
            x1, y1 = positions[parent]
            x2, y2 = positions[i]
            canvas.create_line(x1, y1, x2, y2)
    
    for i in range(n):
        x, y = positions[i]
        if i in swap_highlights:
            fill_color = "orange"
        elif i in highlights:
            fill_color = "red"
        else:
            fill_color = "lightblue"
        canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS,
                           x + NODE_RADIUS, y + NODE_RADIUS,
                           fill=fill_color, outline="black")
        canvas.create_text(x, y, text=str(data[i]), font=("Arial", 12, "bold"))
    
    canvas.update()


def heapify_gen(data, n, i):
    largest = i
    l, r = pyrchild(i)
    
    if l < n:
        yield ("highlight", i, l)
        yield ("pause",)
        if data[l] > data[largest]:
            largest = l
        yield ("unhighlight", i, l)
    
    if r < n:
        yield ("highlight", i, r)
        yield ("pause",)
        if data[r] > data[largest]:
            largest = r
        yield ("unhighlight", i, r)
    
    if largest != i:
        yield ("highlight_swap", i, largest)
        yield ("pause",)
        data[i], data[largest] = data[largest], data[i]
        yield ("draw",)
        yield ("unhighlight_swap", i, largest)
        yield from heapify_gen(data, n, largest)
    yield ("draw",)

def heap_sort_gen(data):
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify_gen(data, n, i)
    
    for i in range(n - 1, 0, -1):
        yield ("highlight_swap", 0, i)
        yield ("pause",)
        data[0], data[i] = data[i], data[0]
        yield ("draw",)
        yield ("unhighlight_swap", 0, i)
        yield from heapify_gen(data, i, 0)
    yield ("done",)

class HeapSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()
        
        self.data = [random.randint(10, 400) for _ in range(20)]
        self.highlights = set()
        self.swap_highlights = set()
        
        self.gen = heap_sort_gen(self.data)
        
        draw_tree(self.canvas, self.data, self.highlights, self.swap_highlights)
    
    def step(self):
        try:
            op = next(self.gen)
            if op[0] == "highlight":
                self.highlights.add(op[1])
                self.highlights.add(op[2])
            elif op[0] == "unhighlight":
                self.highlights.discard(op[1])
                self.highlights.discard(op[2])
            elif op[0] == "highlight_swap":
                self.swap_highlights.add(op[1])
                self.swap_highlights.add(op[2])
            elif op[0] == "unhighlight_swap":
                self.swap_highlights.discard(op[1])
                self.swap_highlights.discard(op[2])
            elif op[0] == "draw":
                pass
            elif op[0] == "pause":
                pass
            elif op[0] == "done":
                print("[*]finish")
                return
            
            draw_tree(self.canvas, self.data, self.highlights, self.swap_highlights)
            self.root.after(DELAY, self.step)
        except StopIteration:
            print("[*]finish")
            return

def main():
    root = tk.Tk()
    root.title("Heap Sort")
    visualizer = HeapSortVisualizer(root)
    root.after(1000, visualizer.step)
    root.mainloop()

if __name__ == "__main__":
    main()
