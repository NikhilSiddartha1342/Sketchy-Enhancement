import cv2

def apply_hdr(image):
    hdr = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)
    return hdr
