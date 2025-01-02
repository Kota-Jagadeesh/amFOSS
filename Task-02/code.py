import pytesseract
from PIL import Image

# Load the image
image_path = "pic.png"  # Replace with your image file
try:
    img = Image.open(image_path)
except FileNotFoundError:
    print("Image not found. Check the file path.")
    exit()

# Extract text and process
text = pytesseract.image_to_string(img, config='--psm 7').strip()
print("OCR Output:", text)

# Simplify and validate
expression = text.replace('O', '0').replace('l', '1').replace(' ', '')

try:
    result = eval(expression)
    print("Expression:", expression)
    print("Result:", result)
except:
    print("Invalid or non-arithmetic expression.")
