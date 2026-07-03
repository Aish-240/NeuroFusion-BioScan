import cv2
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Load Image
# ----------------------------
image = cv2.imread("images/sample_scan.jpg")

if image is None:
    print("Image not found!")
    exit()

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# ----------------------------
# Convert to Gray
# ----------------------------
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# ----------------------------
# Noise Removal
# ----------------------------
blur = cv2.GaussianBlur(gray, (5,5), 0)

# ----------------------------
# Contrast Enhancement
# ----------------------------
clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8,8)
)

enhanced = clahe.apply(blur)

# ----------------------------
# Edge Detection
# ----------------------------
edges = cv2.Canny(
    enhanced,
    40,
    120
)

# ----------------------------
# Threshold Segmentation
# ----------------------------
_, threshold = cv2.threshold(
    enhanced,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# ----------------------------
# Contour Detection
# ----------------------------
contours, _ = cv2.findContours(
    threshold,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

result = image.copy()

for contour in contours:

    area = cv2.contourArea(contour)

    if area > 300:

        x, y, w, h = cv2.boundingRect(contour)

        cv2.rectangle(
            result,
            (x, y),
            (x+w, y+h),
            (255,0,0),
            2
        )

# ----------------------------
# Save Results
# ----------------------------
cv2.imwrite(
    "output/detected_regions.png",
    cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
)

# ----------------------------
# Display
# ----------------------------
titles = [
    "Original",
    "Gray",
    "Enhanced",
    "Edges",
    "Threshold",
    "Detected Region"
]

images = [
    image,
    gray,
    enhanced,
    edges,
    threshold,
    result
]

plt.figure(figsize=(14,8))

for i in range(len(images)):

    plt.subplot(2,3,i+1)

    if len(images[i].shape)==2:
        plt.imshow(images[i], cmap='gray')
    else:
        plt.imshow(images[i])

    plt.title(titles[i])
    plt.axis("off")

plt.tight_layout()
plt.show()

print("Processing Complete!")
