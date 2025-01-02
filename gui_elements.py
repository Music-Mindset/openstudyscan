from tkinter import Button, Label, Text, Canvas, Frame, Scale, Scrollbar, filedialog, HORIZONTAL, END
from tkinter.ttk import Progressbar
from utils import preview_image, preview_processed_image
from ocr_module import perform_ocr, scan_all_images, find_and_remove_duplicate_text
import os


def setup_gui(root):
    """Setup the main GUI layout and components."""
    # Define frames
    left_frame = Frame(root)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    middle_frame = Frame(root)
    middle_frame.pack(side="left", fill="y", padx=10, pady=10)

    right_frame = Frame(root)
    right_frame.pack(side="left", fill="y", padx=10, pady=10)

    bottom_frame = Frame(root)
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    # Global variables
    global canvas, processed_canvas, result_box, image_dir, test_image_path, brightness_slider, contrast_slider, progress_bar
    canvas = None
    processed_canvas = None
    result_box = None
    image_dir = ""
    test_image_path = ""

    # Left Frame: Folder controls
    folder_label = Label(left_frame, text="No folder selected", wraplength=200)
    folder_label.pack(pady=10)

    def select_folder():
        global image_dir
        folder = filedialog.askdirectory()
        if folder:
            image_dir = folder
            folder_label.config(text=f"Selected Folder: {folder}")

    Button(left_frame, text="Select Folder", command=select_folder).pack(pady=10)

    def scan_folder():
        global brightness_slider, result_box, image_dir
        if not image_dir:
            result_box.insert(END, "Please select a folder first!\n")
            return

        def update_progress(status, value=0):
            if status == "init":
                progress_bar["maximum"] = value
                progress_bar["value"] = 0
            elif status == "update":
                progress_bar["value"] = value
                root.update_idletasks()
            elif status == "done":
                progress_bar["value"] = progress_bar["maximum"]

        try:
            brightness = brightness_slider.get() / 10
            contrast = contrast_slider.get() / 10
            output_file = scan_all_images(image_dir, brightness, contrast, progress_callback=update_progress)
            result_box.insert(END, f"Scanned text saved to: {output_file}\n")
        except Exception as e:
            result_box.insert(END, f"Error scanning folder: {e}\n")

    Button(left_frame, text="Scan All Images in Folder", command=scan_folder).pack(pady=10)

    def find_duplicates():
        if not image_dir:
            result_box.insert(END, "Please select a folder first!\n")
            return

        scanned_text_dir = os.path.join(image_dir, "ScannedText")
        if not os.path.exists(scanned_text_dir):
            result_box.insert(END, "No scanned text folder found. Please scan images first!\n")
            return

        try:
            deduplicated_file = find_and_remove_duplicate_text(scanned_text_dir)
            result_box.insert(END, f"Duplicates removed. Deduplicated text saved to: {deduplicated_file}\n")
        except Exception as e:
            result_box.insert(END, f"Error processing duplicates: {e}\n")

    Button(left_frame, text="Find Duplicate Text", command=find_duplicates).pack(pady=10)

    # Middle Frame: Image previews
    canvas = Canvas(middle_frame, width=300, height=300, bg="lightgrey")
    canvas.pack(pady=10)
    Label(middle_frame, text="Original Image").pack()

    processed_canvas = Canvas(middle_frame, width=300, height=300, bg="lightgrey")
    processed_canvas.pack(pady=10)
    Label(middle_frame, text="Processed Image").pack()

    # Right Frame: Test image and settings
    def select_test_image():
        global test_image_path
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            test_image_path = file_path
            preview_image(file_path, canvas)

    Button(right_frame, text="Select Test Image", command=select_test_image).pack(pady=10)

    def run_test_ocr():
        if not test_image_path:
            result_box.insert(END, "Please select a test image first!\n")
            return

        try:
            brightness = brightness_slider.get() / 10
            contrast = contrast_slider.get() / 10
            preview_processed_image(test_image_path, processed_canvas, brightness, contrast)
            text = perform_ocr(test_image_path, brightness, contrast)
            result_box.delete(1.0, END)  # Clear previous text
            result_box.insert(END, f"<---->\n{text}\n")
        except Exception as e:
            result_box.insert(END, f"Error processing test image: {e}\n")

    Button(right_frame, text="Run Test OCR", command=run_test_ocr).pack(pady=10)

    brightness_label = Label(right_frame, text="Adjust Brightness:")
    brightness_label.pack(pady=5)
    brightness_slider = Scale(right_frame, from_=5, to=30, orient=HORIZONTAL)
    brightness_slider.set(15)
    brightness_slider.pack(pady=10)

    contrast_label = Label(right_frame, text="Adjust Contrast:")
    contrast_label.pack(pady=5)
    contrast_slider = Scale(right_frame, from_=10, to=50, orient=HORIZONTAL)
    contrast_slider.set(20)
    contrast_slider.pack(pady=10)

    # Bottom Frame: Output and progress
    result_box = Text(bottom_frame, height=15, width=150)
    result_box.pack(pady=10, padx=10, fill="x")

    scroll = Scrollbar(bottom_frame, command=result_box.yview)
    scroll.pack(side="right", fill="y")
    result_box.config(yscrollcommand=scroll.set)

    progress_bar = Progressbar(bottom_frame, orient="horizontal", length=500, mode="determinate")
    progress_bar.pack(pady=10)
