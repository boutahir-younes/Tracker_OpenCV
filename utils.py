import cv2
import numpy as np

# ── Etape 1 : filtre gaussien
def preprocess(frame):
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    return blurred

# ── Etape 2 : conversion BGR→HSV + seuillage
def get_hsv_mask(frame):
    blurred = preprocess(frame)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    
    lower = np.array([20,  80,  80])
    upper = np.array([70, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    return mask

# ── Etape 4 : morphologie mathématique
def clean_mask(mask):
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

# ── Etape 5 : detection contours + bounding box
def get_bbox(mask):
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    # Filtrer : garder seulement les contours circulaires

    candidats = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 30:          # trop petit = bruit
            continue
        if area > 50000:       # trop grand = ligne/panneau
            continue
        x, y, w, h = cv2.boundingRect(c)
        if h == 0:
            continue
        ratio = w / h
        if 0.4 < ratio < 2.5: # forme arrondie
            candidats.append((area, c))

    if not candidats:
        return None

    # Prendre le candidat le plus proche d'un cercle parfait
    def circularite(item):
        area, c = item
        x, y, w, h = cv2.boundingRect(c)
        return abs(1.0 - (w / h)) 

    candidats.sort(key=circularite)
    _, best = candidats[0]

    x, y, w, h = cv2.boundingRect(best)
    return (x, y, w, h)