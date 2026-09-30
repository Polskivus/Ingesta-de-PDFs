from pypdf import PdfReader
import pytesseract
from PIL import Image

print(pytesseract.image_to_string(Image.open('imagen-0-Image21.png')))

RUTA_PDF = "prueba.pdf"

reader = PdfReader(RUTA_PDF)
page = reader.pages[0]

for i, image_file_object in enumerate(page.images):
    file_name = "imagen-" + str(i) + "-" + image_file_object.name
    image_file_object.image.save(file_name)

print(reader)
print(page.extract_text())