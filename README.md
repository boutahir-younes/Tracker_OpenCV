# Tennis Ball Tracker — OpenCV 🎾

Real-time tennis ball tracking using OpenCV trackers (CSRT/KCF)
and HSV color segmentation.

---

## Demo

https://github.com/boutahir-younes/Tracker_OpenCV/raw/main/Videos/demo.mp4

---

## How It Works

| Step | Operation |
|------|-----------|
| 1 | Video decomposed into frames |
| 2 | Gaussian filter — noise reduction |
| 3 | BGR → HSV color conversion |
| 4 | HSV thresholding → binary mask |
| 5 | Morphology — erosion + dilation |
| 6 | Contours + Bounding box extraction |
| 7 | CSRT / KCF Tracker initialized |

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

```
1. Select a video from the dropdown menu
2. Click LAUNCH
3. Draw a rectangle around the ball
4. Press ENTER to confirm
5. Tracking starts on 3 panels simultaneously
6. Click STOP to stop
```

---

## Project Structure

```
Tracker_OpenCV/
│
├── app.py              ← Graphical interface (3 panels)
├── utils.py            ← Image processing pipeline
│
└── Videos/
    ├── input_1.mp4     ← Test video 1
    ├── input_2.mp4     ← Test video 2
    ├── input_3.mp4     ← Test video 3
    └── demo.mp4        ← Demo recording
```

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
