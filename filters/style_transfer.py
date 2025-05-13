import cv2

def apply_style_transfer(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Image not found or unreadable.")
    
    stylized = cv2.stylization(image, sigma_s=60, sigma_r=0.07)
    output_path = image_path.replace(".jpg", "_stylized.jpg").replace(".png", "_stylized.png")
    
    cv2.imwrite(output_path, stylized)
    return output_path
