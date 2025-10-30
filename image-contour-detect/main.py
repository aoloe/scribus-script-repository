import tkinter as tk
import cv2
import numpy as np

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

    #filename = '/tmp/stick-figures.webp'
    #filename = '/tmp/stick-figure.png'
    filename = '/tmp/naturaleza.png'
    #filename = '/tmp/test.png'

    def alpha_channel_to_white(img):
        #make mask of where the transparent bits are
        trans_mask = img[:,:,3] == 0
        
        #replace areas of transparency with white and not transparent
        img[trans_mask] = [255, 255, 255, 255]
        
        #new image without alpha channel...
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img

    def reduce_to_outer_contour(img, invert_mask, simplify, original_img):
        # Blur the image to fill gaps
        # The kernel must be two odd integers. Bigger numbers -> more blurred
        blurred = cv2.GaussianBlur(img, (9,9), 0)
        # cv2.threshhold expects uint8
        blurred = blurred.astype(np.uint8)

        _, mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if invert_mask:
            # invert the mask (only needed in first iteration)
            mask = cv2.bitwise_not(mask)

        # Fill small gaps and remove noise
        # The kernel must be two odd integers. Bigger numbers -> smoother
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill small gaps
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Remove small noise

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Simplifies the image (not great results, creats more straight lines)
        # The variable 'reduce_percentage_of_arc' is how strong this simplification is.
        # I believe it is the percentage of the arc that it is straightening
        reduce_percentage_of_arc = 0.0001
        if simplify:
            contours = list(contours)
            for idx, c in enumerate(contours):
                epsilon = reduce_percentage_of_arc * cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon, True)
                # convexHull is quite strong, you can try disabling it as well
                # convexHull hides a lot of what the 'reduce_percentage_of_arc' does.
                # However, I think for what you want to achieve, you want to have convexHull on, and not make 'reduce_percentage_of_arc' a value available to the user, just set it to something low.
                approx = cv2.convexHull(approx)
                contours[idx] = approx

        print("Number of Contours = " ,len(contours))
        print(hierarchy)
        #cv2.imshow('Edges', mask)

        if original_img is None:
            img = np.zeros(img.shape)
            cv2.drawContours(img, contours, -1, (255, 255, 255), 10)
        else:
            # show final image
            cv2.drawContours(original_img, contours, -1, (0, 0, 255), 3)
            img = original_img

        return img

    def action_A():
        print('2 iterations - no simplification (What we ended the Hackergarten with)')
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        img = alpha_channel_to_white(img)
        
        cv2.imshow('Original', img)
        original_img = img

        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

        # This is the main part where it loops the operation
        iterations = 2
        for i in range(iterations):
            img = reduce_to_outer_contour(img, (i == 0), False, original_img if i == iterations-1 else None)

        cv2.imwrite("/tmp/outputA.png", img)
        cv2.imshow('Contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def action_B():
        print('10 iterations - no simplification')
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        img = alpha_channel_to_white(img)
        
        cv2.imshow('Original', img)
        original_img = img

        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

        # Doing more iterations increases the size of the hull and absorbes the surrounding contours each iteration.
        iterations = 10
        for i in range(iterations):
            img = reduce_to_outer_contour(img, (i == 0), False, original_img if i == iterations-1 else None)

        cv2.imwrite("/tmp/outputB.png", img)
        cv2.imshow('Contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def action_C():
        print('10 iterations, with simplifying in the last iteration')
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        img = alpha_channel_to_white(img)
        
        cv2.imshow('Original', img)
        original_img = img

        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

        # Simplificaiton gives the straight lines with a sort approximation of the shape
        iterations = 10
        for i in range(iterations):
            img = reduce_to_outer_contour(img, (i == 0), i>=iterations-1, original_img if i == iterations-1 else None)

        cv2.imwrite("/tmp/outputC.png", img)
        cv2.imshow('Contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def action_D():
        print('3 iterations, with simplifying in the last two iterations')
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        img = alpha_channel_to_white(img)
        
        cv2.imshow('Original', img)
        original_img = img

        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

        # The simplification works well when more than one iteration is simplified.
        # It can even bring down the number of iterations, keeping the shape tighter around the object
        iterations = 3
        for i in range(iterations):
            img = reduce_to_outer_contour(img, (i == 0), i>=iterations-2, original_img if i == iterations-1 else None)

        cv2.imwrite("/tmp/outputD.png", img)
        cv2.imshow('Contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    button_1_tk = tk.Button(p_left, text='A', command=action_A)
    p_left.add(button_1_tk, sticky=tk.NW)
    button_2_tk = tk.Button(p_left, text='B', command=action_B)
    p_left.add(button_2_tk, sticky=tk.NW)
    button_3_tk = tk.Button(p_left, text='C', command=action_C)
    p_left.add(button_3_tk, sticky=tk.NW)
    button_4_tk = tk.Button(p_left, text='D', command=action_D)
    p_left.add(button_4_tk, sticky=tk.NW)


    p2 = tk.PanedWindow(p1, orient=tk.VERTICAL)
    p1.add(p2)

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
