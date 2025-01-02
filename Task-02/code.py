from PIL import Image
import pytesseract
#this loads the image
img = Image.open("expression.png")
# here , we extract the text from the image
extracted_text = pytesseract.image_to_string(img)
#cleaning and removing the unwanted text from the image
expression = extracted_text.strip()
#Evaluating the expression
try:
    result = eval(expression)
    print(f"The result of '{expression}' is: {result}")
except Exception as e:
    print(f"Error: {e}")
