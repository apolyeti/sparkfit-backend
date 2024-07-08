import os 
import cv2
from colorthief import ColorThief
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

images_path = "../data/colorful_fashion_dataset_for_object_detection/JPEGImages/"
os.system("ls " + images_path)