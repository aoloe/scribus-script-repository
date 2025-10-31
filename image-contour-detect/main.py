import tkinter as tk

from PIL import ImageTk, Image

import cv2
import numpy as np

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


    def action_A(input_filename, output_filename):
        img = cv2.imread(input_filename, cv2.IMREAD_UNCHANGED)

        #convert img to grey
        # img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_grey = cv2.cvtColor(img,cv2.COLOR_RGBA2GRAY)
        cv2.imwrite('/tmp/grey.png',img_grey)
        #set a thresh
        thresh = 100
        #get threshold image
        ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
        #find contours
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #create an empty image for contours
        img_contours = np.zeros(img.shape)
        # draw the contours on the empty image
        cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
        #save image
        cv2.imwrite(output_filename,img_contours)

    def action_B(input_filename, output_filename):
        img = cv2.imread(input_filename, cv2.IMREAD_UNCHANGED)

        #convert img to grey
        img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # thresh = 100
        # ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

        # blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        canny = cv2.Canny(img_grey, 30, 200)

        contours, hierarchy = cv2.findContours(canny,
           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # print("Number of Contours = " ,len(contours))
        # cv2.imshow('Canny Edges', canny)
        
        # combining contours
        # contours = np.vstack([contours[5], contours[6]])
        # contours = np.vstack(contours)

        # for c in contours:
        #     hull = cv2.convexHull(c)

        # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
        #create an empty image for contours
        img_contours = np.zeros(img.shape)
        # draw the contours on the empty image
        cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
        #save image
        cv2.imwrite(output_filename,img_contours)
        cv2.imshow('Contours', img_contours)

        # for imshow
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def action_C(input_filename, output_filename):
        ...

    button_1_tk = tk.Button(p_left, text='A', command=lambda: action_A(filename, '/tmp/contour.png'))
    p_left.add(button_1_tk, sticky=tk.NW)
    button_2_tk = tk.Button(p_left, text='B', command=lambda: action_B(filename, '/tmp/contour.png'))
    button_3_tk = tk.Button(p_left, text='C', command=lambda: action_C(filename, '/tmp/contour.png'))
    p_left.add(button_2_tk, sticky=tk.NW)

    p2 = tk.PanedWindow(p1, orient=tk.VERTICAL)
    p1.add(p2)

    # filename = '/tmp/naturaleza.webp'
    # filename = '/tmp/naturaleza.png'
    filename = '/tmp/naturaleza-flat.png'
    # filename = '/tmp/mountains.png'

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
