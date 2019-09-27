# - in a document add empty image frames
# - all empty image frames will be filled with the images collected
import os
import sys
import scribus

if not scribus.haveDoc():
    scribus.messagebarText("No .")
    sys.exit()

def get_all_images(path):
    extensions = ['jpg', 'jpeg', 'JPG', 'png', 'PNG', 'tif', 'TIF']
    filenames = [f for f in os.listdir(path)
                 if any(f.endswith(ext) for ext in extensions)]
    filenames.sort()
    return filenames

def get_all_empty_images_frames():
    image_frames = []
    for page in range(1, scribus.pageCount() + 1):
        page_image_frames = []
        scribus.gotoPage(page)
        # get all empty image frames on the page
        for item in scribus.getPageItems():
            if item[1] == 2:
                if scribus.getImageFile(item[0]) == "":
                    x, y = scribus.getPosition(item[0])
                    page_image_frames.append((item[0], x, y))
        # sort the frames by position
        page_image_frames.sort(key=lambda k: [k[2], k[1]])
        image_frames += [i[0] for i in page_image_frames]
    return image_frames

path = scribus.fileDialog("Pick a directory", scribus.getDocName(), isdir = True)
if path == '':
   scribus.messagebarText("No directory selected.")

print('chuila')

images = get_all_images(path)
if not images:
    scribus.messagebarText("No image found.")
    sys.exit()

print(images)

frames = get_all_empty_images_frames()
print(frames)


for frame, image in zip(frames, images):
    scribus.loadImage(os.path.join(path, image), frame)
    # scribus.setScaleImageToFrame(True, True, new_image)
