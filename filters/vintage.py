import cv2
import numpy as np

def apply_vintage(image):
    rows, cols = image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, 200)
    kernel_y = cv2.getGaussianKernel(rows, 200)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    vintage = np.copy(image)
    for i in range(3):
        vintage[:, :, i] = vintage[:, :, i] * mask
    return vintage
