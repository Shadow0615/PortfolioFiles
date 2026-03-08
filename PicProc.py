import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

current_cv_image = None

zoom_factor = 1.0
pan_x = 0
pan_y = 0

drag_start_x = 0
drag_start_y = 0


# -----------------------------
# IMAGE PROCESSING
# -----------------------------

def process_image(image):

    annotated = image.copy()

    gray = cv2.cvtColor(annotated, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(5,5),0)
    edges = cv2.Canny(blurred,50,150)

    contours,_ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    centers = []

    for cnt in contours:

        if cv2.contourArea(cnt) < 100:
            continue

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        cv2.drawContours(annotated,[box],0,(0,255,0),2)

        (cx,cy),(w,h),angle = rect

        cx = int(cx)
        cy = int(cy)

        centers.append((cx,cy))

        cv2.circle(annotated,(cx,cy),5,(0,0,255),-1)

    draw_center_list(annotated,centers)

    return annotated


# -----------------------------
# WRITE CENTER LIST
# -----------------------------

def draw_center_list(img, centers):

    height = img.shape[0]
    start_y = height - 20

    cv2.putText(img,"Centers:",(10,start_y),
                cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),1)

    for i,(cx,cy) in enumerate(centers):

        text = f"{i+1}: ({cx},{cy})"

        cv2.putText(img,text,
                    (10,start_y-(i+1)*20),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,
                    (0,255,255),1)


# -----------------------------
# LOAD IMAGE
# -----------------------------

def load_image():

    global current_cv_image
    global zoom_factor, pan_x, pan_y

    path = filedialog.askopenfilename(
        filetypes=[("Images","*.png *.jpg *.jpeg *.bmp")]
    )

    if not path:
        return

    current_cv_image = cv2.imread(path)

    zoom_factor = 1.0
    pan_x = 0
    pan_y = 0

    update_display()


# -----------------------------
# DISPLAY IMAGE
# -----------------------------

def update_display():

    if current_cv_image is None:
        return

    frame_w = image_frame.winfo_width()
    frame_h = image_frame.winfo_height()

    if frame_w < 10 or frame_h < 10:
        return

    img = process_image(current_cv_image)

    h,w = img.shape[:2]

    scale = min(frame_w/w,frame_h/h) * zoom_factor

    new_w = int(w*scale)
    new_h = int(h*scale)

    resized = cv2.resize(img,(new_w,new_h))

    canvas = np.zeros((frame_h,frame_w,3),dtype=np.uint8)

    x = (frame_w-new_w)//2 + pan_x
    y = (frame_h-new_h)//2 + pan_y

    x1 = max(x,0)
    y1 = max(y,0)

    x2 = min(x+new_w,frame_w)
    y2 = min(y+new_h,frame_h)

    img_x1 = max(0,-x)
    img_y1 = max(0,-y)

    img_x2 = img_x1 + (x2-x1)
    img_y2 = img_y1 + (y2-y1)

    if x2>x1 and y2>y1:

        canvas[y1:y2,x1:x2] = resized[img_y1:img_y2,img_x1:img_x2]

    rgb = cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(rgb)

    tk_img = ImageTk.PhotoImage(pil_img)

    image_label.config(image=tk_img)
    image_label.image = tk_img


# -----------------------------
# ZOOM
# -----------------------------

def zoom(event):

    global zoom_factor

    if event.delta > 0:
        zoom_factor *= 1.1
    else:
        zoom_factor /= 1.1

    update_display()


# -----------------------------
# PAN
# -----------------------------

def start_drag(event):

    global drag_start_x, drag_start_y

    drag_start_x = event.x
    drag_start_y = event.y


def drag(event):

    global pan_x, pan_y, drag_start_x, drag_start_y

    dx = event.x - drag_start_x
    dy = event.y - drag_start_y

    pan_x += dx
    pan_y += dy

    drag_start_x = event.x
    drag_start_y = event.y

    update_display()


# -----------------------------
# WINDOW RESIZE
# -----------------------------

def on_resize(event):
    update_display()


# -----------------------------
# GUI
# -----------------------------

root = tk.Tk()
root.title("Image Processor")
root.geometry("900x700")

image_frame = tk.Frame(root,bg="black")
image_frame.pack(fill="both",expand=True)

image_label = tk.Label(image_frame,bg="black")
image_label.pack(fill="both",expand=True)

controls = tk.Frame(root)
controls.pack(pady=10)

tk.Button(controls,text="Load Image",command=load_image).pack()

root.bind("<MouseWheel>",zoom)

image_label.bind("<ButtonPress-1>",start_drag)
image_label.bind("<B1-Motion>",drag)

root.bind("<Configure>",on_resize)

root.mainloop()