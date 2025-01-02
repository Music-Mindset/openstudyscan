from PIL import Image
import pytesseract
import os


def perform_ocr(image_path, brightness=1.5, contrast=2.0):
    """Perform OCR on a single image."""
    try:
        with Image.open(image_path) as img:
            # Apply brightness and contrast adjustments
            img = img.point(lambda p: p * brightness).point(lambda p: (p - 128) * contrast + 128)
            text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        raise RuntimeError(f"Error processing image {image_path}: {e}")


def scan_all_images(image_dir, brightness=1.5, contrast=2.0, progress_callback=None):
    """Scan all images in the folder and save results to a text file."""
    if not image_dir:
        raise ValueError("No folder selected.")

    # Create a directory for scanned text
    scanned_text_dir = os.path.join(image_dir, "ScannedText")
    os.makedirs(scanned_text_dir, exist_ok=True)

    # Determine the next available filename
    existing_files = [f for f in os.listdir(scanned_text_dir) if f.startswith("Scanned text") and f.endswith(".txt")]
    next_file_number = len(existing_files) + 1
    output_file = os.path.join(scanned_text_dir, f"Scanned text {next_file_number:02d}.txt")

    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    total_files = len(image_files)

    # Initialize progress
    if progress_callback:
        progress_callback("init", total_files)

    results = []
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(image_dir, image_file)
        try:
            text = perform_ocr(image_path, brightness, contrast)
            results.append((image_file, text))
        except Exception as e:
            results.append((image_file, f"Error: {e}"))

        # Update progress
        if progress_callback:
            progress_callback("update", i + 1)

    with open(output_file, "w", encoding="utf-8") as file:
        for image_file, text in results:
            file.write(f"<---->\n{text}\n\n")

    if progress_callback:
        progress_callback("done")

    return output_file


def find_and_remove_duplicate_text(scanned_text_dir):
    """Find and remove duplicate text blocks within scanned text files."""
    unique_blocks = set()
    deduplicated_content = []
    original_files = [f for f in os.listdir(scanned_text_dir) if f.endswith(".txt")]

    for file_name in original_files:
        with open(os.path.join(scanned_text_dir, file_name), "r", encoding="utf-8") as file:
            content = file.read()
            blocks = content.split("<---->")
            for block in blocks:
                block = block.strip()
                if block and block not in unique_blocks:
                    unique_blocks.add(block)
                    deduplicated_content.append(block)

    # Save deduplicated content to a new file
    deduplicated_file = os.path.join(scanned_text_dir, "Deduplicated text.txt")
    with open(deduplicated_file, "w", encoding="utf-8") as file:
        for block in deduplicated_content:
            file.write(f"<---->\n{block}\n\n")

    return deduplicated_file
