import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
from utils import get_hsv_mask, clean_mask, get_bbox


BG_MAIN    = "#FFFFFF"  
BG_HEADER  = "#F8FAFC"  
ACCENT     = "#2563EB"  
TEXT_MAIN  = "#1E293B"  
BORDER     = "#E2E8F0"  

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SSuvoui ball de tennis")
        self.root.configure(bg=BG_MAIN)
        
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.WIN_W, self.WIN_H = int(sw * 0.95), int(sh * 0.85)
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")

        self.PW = (self.WIN_W - 120) // 3
        self.PH = int(self.PW * 9 / 16)

        self.running = False
        self.cap = None
        self.manual_tracker = None
        
        self._build_ui()
        self._load_videos()

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG_HEADER, height=70, bd=0, highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x", side="top")
        
        tk.Label(header, text="ANALYSE DE TRAJECTOIRE (TENNIS)", font=("Segoe UI", 14, "bold"), 
                 fg=ACCENT, bg=BG_HEADER).pack(side="left", padx=30)

        ctrl = tk.Frame(header, bg=BG_HEADER)
        ctrl.pack(side="right", padx=30)
        
        self.video_var = tk.StringVar()
        self.combo = ttk.Combobox(ctrl, textvariable=self.video_var, width=25, state="readonly")
        self.combo.pack(side="left", padx=10)

        tk.Button(ctrl, text="LANCER", command=self._start, bg=ACCENT, fg="white", 
                  relief="flat", font=("Segoe UI", 9, "bold"), padx=15, cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(ctrl, text="STOP", command=self._stop, bg="#EF4444", fg="white", 
                  relief="flat", font=("Segoe UI", 9, "bold"), padx=15, cursor="hand2").pack(side="left", padx=5)

        self.main_zone = tk.Frame(self.root, bg=BG_MAIN)
        self.main_zone.pack(expand=True, fill="both", pady=30)

       
        labels = ["FLUX ORIGINAL", "TRACKING CSRT (MANUEL)", "TRACKING COULEUR (HSV)"]
        self.panels = []
        
        for i in range(3):
            card = tk.Frame(self.main_zone, bg=BG_MAIN)
            card.pack(side="left", padx=15, expand=True)
            
            tk.Label(card, text=labels[i], font=("Segoe UI", 10, "bold"), fg=TEXT_MAIN, bg=BG_MAIN).pack(pady=(0, 10))
            
            p = tk.Label(card, bg="#F1F5F9", bd=1, relief="solid")
            p.pack()
            self.panels.append(p)

    def _load_videos(self):
        vids = [f for f in os.listdir("videos") if f.endswith((".mp4", ".avi"))]
        self.combo["values"] = vids if vids else ["Aucun fichier"]
        if vids: self.combo.current(0)

    def _start(self):
        path = f"videos/{self.video_var.get()}"
        self.cap = cv2.VideoCapture(path)
        ret, frame = self.cap.read()
        if not ret: return

        frame = cv2.resize(frame, (self.PW, self.PH))
        bbox = cv2.selectROI("Initialisation de la balle", frame, False)
        cv2.destroyAllWindows()

        self.manual_tracker = cv2.TrackerCSRT_create()
        self.manual_tracker.init(frame, bbox)

        self.running = True
        threading.Thread(target=self._run_logic, daemon=True).start()

    def _run_logic(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret: break

            frame = cv2.resize(frame, (self.PW, self.PH))
            v_orig = frame.copy()
            v_man  = frame.copy()
            v_color = frame.copy() # On utilise une copie de l'image originale pour le tracking couleur
            
            
            ok, box = self.manual_tracker.update(frame)
            if ok:
                x, y, w, h = [int(v) for v in box]
                cv2.rectangle(v_man, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(v_man, "Manuel", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            
            mask = clean_mask(get_hsv_mask(frame))
            bbox_c = get_bbox(mask)
            
            if bbox_c:
                x, y, w, h = bbox_c
                cv2.rectangle(v_color, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(v_color, "Couleur", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            
            self._update_img(v_orig, self.panels[0])
            self._update_img(v_man, self.panels[1])
            self._update_img(v_color, self.panels[2])
            
            self.root.update()

    def _update_img(self, cv_img, label):
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        tk_img = ImageTk.PhotoImage(pil)
        label.config(image=tk_img)
        label.image = tk_img

    def _stop(self):
        self.running = False
        if self.cap: self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()