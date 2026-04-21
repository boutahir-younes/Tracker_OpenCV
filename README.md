# Tennis Ball Tracker — OpenCV 🎾

Real-time tennis ball tracking using OpenCV trackers (CSRT/KCF)
and HSV color segmentation.

---

## Demo

https://github.com/boutahir-younes/Tracker_OpenCV/raw/main/Videos/demo.mp4

---

## How It Works

| Step | Operation | Course Chapter |
|------|-----------|---------------|
| 1 | Video → Frames acquisition | CHAP 1 |
| 2 | Gaussian filter (noise reduction) | CHAP 2 |
| 3 | BGR → HSV color conversion | CHAP 1+3 |
| 4 | HSV thresholding → binary mask | CHAP 3 |
| 5 | Morphology — erosion + dilation | CHAP 4 |
| 6 | Contours + Bounding box | CHAP 5 |
| 7 | CSRT / KCF Tracker | CHAP 1+5 |

---

## Two Tracking Methods

| Method | How | Advantage |
|--------|-----|-----------|
| Manual (ROI) | Draw a rectangle around the ball | Works with any object |
| HSV Color | Automatic yellow-green detection | Fully automatic |

---

## Tracker Comparison

| Tracker | Speed | Accuracy | Choice |
|---------|-------|----------|--------|
| CSRT (2017) | ~25 fps | Very high | ✅ Recommended |
| KCF (2014) | ~60 fps | Good | For comparison |

---

## Installation

```bash
pip install opencv-contrib-python numpy Pillow
```

## Run

```bash
python app.py
```

---

## How to Use

1.Select a video from the dropdown menu
2.Click LAUNCH
3.Draw a rectangle around the ball → press ENTER
4.Tracking starts on 3 panels simultaneously
5.Click STOP to stop
---

## Project Structure

Tracker_OpenCV/
├── app.py        ← Graphical interface (3 panels)
├── utils.py      ← Image processing pipeline
└── Videos/
  ├── input_1.mp4
  ├── input_2.mp4
  ├── input_3.mp4
  └── demo.mp4
---

## Interface — 3 Panels

| Panel | Content |
|-------|---------|
| Left | Original video |
| Center | CSRT manual tracking + trajectory |
| Right | HSV automatic color tracking |

---

## Built With

![Python](https://img.shields.io/badge/Python-3.13-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
