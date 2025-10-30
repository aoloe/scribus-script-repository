import tkinter as tk

from PIL import ImageTk, Image

def cancel(root):
    root.quit()
    root.withdraw()

def main():
    root = tk.Tk()
    root.attributes('-type', 'dialog')
    root.geometry("500x300")


    root.bind('<Escape>', lambda *args: cancel(root))

    p1 = tk.PanedWindow()
    p1.pack(fill=tk.BOTH, expand=1)

    p_left = tk.PanedWindow(p1, orient=tk.VERTICAL)
    p1.add(p_left)


    def action_A():
        print('action 1')
    def action_B():
        print('action 2')

    button_1_tk = tk.Button(p_left, text='A', command=action_A)
    p_left.add(button_1_tk, sticky=tk.NW)
    button_2_tk = tk.Button(p_left, text='B', command=action_B)
    p_left.add(button_2_tk, sticky=tk.NW)

    p2 = tk.PanedWindow(p1, orient=tk.VERTICAL)
    p1.add(p2)

    filename = '/tmp/naturaleza.webp'

    canvas_width, canvas_height = 300, 300

    canvas = tk.Canvas(p2, width=canvas_width, height=canvas_height)
    canvas.pack()

    img = Image.open(filename)
    img = img.resize((200, 200))
    image_tk = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, anchor=tk.NW, image=image_tk)

    # Draw something on top of image.
    points = [100, 140, 110, 110, 140, 100, 110, 90, 100, 60, 90, 90, 60, 100, 90, 110]
    canvas.create_polygon(points, outline='green', fill='yellow', width=3)


    root.mainloop()

if __name__ == '__main__':
    main()
