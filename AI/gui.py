pip install opencv-python pillow numpy matplotlib
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import cv2
import numpy as np

class NeuroFusionGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("NeuroFusion BioScan")
        self.root.geometry("1200x700")
        self.root.configure(bg="#EAF4FC")

        title = tk.Label(
            root,
            text="NeuroFusion BioScan",
            font=("Arial",24,"bold"),
            bg="#1976D2",
            fg="white",
            pady=10
        )

        title.pack(fill="x")

        self.image_label = tk.Label(root,bg="white")
        self.image_label.pack(pady=20)

        button_frame = tk.Frame(root,bg="#EAF4FC")
        button_frame.pack()

        tk.Button(
            button_frame,
            text="Upload Image",
            command=self.upload_image,
            width=18,
            bg="#4CAF50",
            fg="white"
        ).grid(row=0,column=0,padx=10)

        tk.Button(
            button_frame,
            text="Enhance",
            command=self.enhance,
            width=18,
            bg="#2196F3",
            fg="white"
        ).grid(row=0,column=1,padx=10)

        tk.Button(
            button_frame,
            text="Detect Region",
            command=self.detect,
            width=18,
            bg="#FF9800",
            fg="white"
        ).grid(row=0,column=2,padx=10)

        tk.Button(
            button_frame,
            text="Save",
            command=self.save,
            width=18,
            bg="#9C27B0",
            fg="white"
        ).grid(row=0,column=3,padx=10)

        self.image = None
        self.processed = None

    def upload_image(self):

        file = filedialog.askopenfilename(
            filetypes=[("Images","*.png *.jpg *.jpeg")]
        )

        if file:

            self.image = cv2.imread(file)
            self.display(self.image)

    def display(self,img):

        rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        image = Image.fromarray(rgb)

        image = image.resize((600,450))

        photo = ImageTk.PhotoImage(image)

        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def enhance(self):

        if self.image is None:
            return

        gray = cv2.cvtColor(
            self.image,
            cv2.COLOR_BGR2GRAY
        )

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8,8)
        )

        enhanced = clahe.apply(gray)

        self.processed = cv2.cvtColor(
            enhanced,
            cv2.COLOR_GRAY2BGR
        )

        self.display(self.processed)

    def detect(self):

        if self.image is None:
            return

        gray = cv2.cvtColor(
            self.image,
            cv2.COLOR_BGR2GRAY
        )

        blur = cv2.GaussianBlur(gray,(5,5),0)

        _,th = cv2.threshold(
            blur,
            0,
            255,
            cv2.THRESH_BINARY+cv2.THRESH_OTSU
        )

        contours,_ = cv2.findContours(
            th,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        result = self.image.copy()

        for c in contours:

            if cv2.contourArea(c)>400:

                x,y,w,h = cv2.boundingRect(c)

                cv2.rectangle(
                    result,
                    (x,y),
                    (x+w,y+h),
                    (0,0,255),
                    2
                )

        self.processed = result

        self.display(result)

    def save(self):

        if self.processed is None:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png"
        )

        if filename:

            cv2.imwrite(
                filename,
                self.processed
            )

root = tk.Tk()

app = NeuroFusionGUI(root)

root.mainloop()
