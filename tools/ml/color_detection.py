import os 
import cv2
from colorthief import ColorThief
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

images_path = "../data/colorful_fashion_dataset_for_object_detection/JPEGImages/"

images = os.listdir(images_path)

for i, image_path in enumerate(images):
    full_img_path = os.path.join(images_path, image_path)
    image = Image.open(full_img_path)
    
    # Get the most prominent colors in the image to visualize
    ct = ColorThief(full_img_path)
    palette = ct.get_palette(color_count=15)

    image = np.array(image)  # Convert PIL image to numpy array
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Convert the image to HSV (Hue Saturation Values)

    for color in palette:
        # Convert the color to HSV
        c = np.uint8([[color]])
        hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

        lower_limit = hsvC[0][0][0] - 10, 50, 50
        upper_limit = hsvC[0][0][0] + 10, 255, 255

        lower_limit = np.array(lower_limit, dtype=np.uint8)
        upper_limit = np.array(upper_limit, dtype=np.uint8)

        mask = cv2.inRange(hsv_image, lower_limit, upper_limit)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # Draw bounding boxes for each contour
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            color_bgr = (int(color[2]), int(color[1]), int(color[0]))  # Convert RGB to BGR for OpenCV
            image = cv2.rectangle(image, (x, y), (x + w, y + h), color_bgr, 2)
    
    if i <= 5:
        # Convert BGR image to RGB for displaying with matplotlib
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
        plt.title('Detected Colors with Bounding Boxes')
        plt.axis('off')  # Hide axis
        plt.show()
    if i == 5:
        break