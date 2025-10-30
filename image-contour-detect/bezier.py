import tkinter as tk

# https://stackoverflow.com/questions/50297255/trouble-drawing-bezier-curve


def draw_bezier():
    # Start x and y coordinates, when t = 0
    x_start = control_points[0][0]
    y_start = control_points[0][1]

    p = control_points

    # loops through
    n = 50
    for i in range(50):
        t = i / n
        x = (p[0][0] * (1-t)**3 + p[1][0] * 3 * t * (1-t)**2 + p[2][0] * 3 * t**2 * (1-t) + p[3][0] * t**3)
        y = (p[0][1] * (1-t)**3 + p[1][1] * 3 * t * (1-t)**2 + p[2][1] * 3 * t**2 * (1-t) + p[3][1] * t**3)

        canvas.create_line(x, y, x_start, y_start)
        # updates initial values
        x_start = x
        y_start = y


def get_point(event):
    global control_points
    point = x, y = (event.x, event.y)
    control_points.append(point)
    canvas.create_oval(x, y, x+3, y+3)
    if len(control_points) == 4:
        draw_bezier()
        control_points = []


if __name__ == '__main__':

    control_points = []

    root = tk.Tk()

    canvas = tk.Canvas(root, width=800, height=800)
    canvas.pack()

    canvas.bind('<Button-1>', get_point)

    root.mainloop()
