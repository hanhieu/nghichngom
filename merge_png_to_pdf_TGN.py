import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def merge_images_in_folder_to_pdf(folder_path, output_pdf_path):
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_paths:
        print("No images found in the specified folder.")
        return

    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    for image_path in image_paths:
        img = ImageReader(image_path)
        img_width, img_height = img.getSize()

        c.setPageSize((img_width, img_height))
        c.drawImage(img, 0, 0, width=img_width, height=img_height)
        c.showPage()

    c.save()

# Example usage
folder_path = "E:/Report/TGN/73-23T12"
output_pdf_path = folder_path+ "/merged_images.pdf"

merge_images_in_folder_to_pdf(folder_path, output_pdf_path)