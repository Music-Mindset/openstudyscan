from PIL import Image, ImageEnhance, ImageTk

def preprocess_image_for_ocr(image_path, brightness=1.5, contrast=2.0):
    """Preprocess the image for better OCR results."""
    with Image.open(image_path) as img:
        img = img.convert("L")  # Convert to grayscale
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)  # Adjust contrast
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)  # Adjust brightness
        img = img.point(lambda x: 0 if x < 128 else 255, "1")  # Apply thresholding
        return img

def preview_image(image_path, canvas):
    """Display the selected image in the specified preview canvas."""
    with Image.open(image_path) as img:
        img.thumbnail((300, 300))  # Resize for preview
        img_tk = ImageTk.PhotoImage(img)
        canvas.image = img_tk  # Keep a reference to avoid garbage collection
        canvas.create_image(150, 150, image=img_tk)

def preview_processed_image(image_path, canvas, brightness=1.5, contrast=2.0):
    """Display the processed image in the preview canvas."""
    img = preprocess_image_for_ocr(image_path, brightness, contrast)
    img.thumbnail((300, 300))  # Resize for preview
    img_tk = ImageTk.PhotoImage(img)
    canvas.image = img_tk  # Keep a reference to avoid garbage collection
    canvas.create_image(150, 150, image=img_tk)
