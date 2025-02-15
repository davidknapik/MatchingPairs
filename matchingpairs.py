import pyautogui
import easyocr
import numpy as np
from PIL import Image

def capture_and_ocr():
   # Capture a specific region of the screen (adjust coordinates as needed)
   # x, y is top left corner, width and height define the region
   x, y, width, height = 690, 410, 575, 390
   screenshot = pyautogui.screenshot(region=(x, y, width, height))
   img = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())

   # Initialize EasyOCR reader (specify languages)
   reader = easyocr.Reader(['en', 'fr'])  # English and French

   # Perform OCR using EasyOCR
   results = reader.readtext(np.array(img))

   # Print the detected text and bounding boxes
   for (bbox, text, prob) in results:
      (top_left, top_right, bottom_right, bottom_left) = bbox
      tl=(int(top_left[0]), int(top_left[1]))

      # print(f"Text: {text}, Confidence: {prob}, Coordinates: {tl}")
      print(f"Text: {text}, Coordinates: {tl}")

   return results


def detect_columns(results):
   english_words = []
   french_words = []

   # 1. Calculate the average X-coordinate to find a separation point
   x_coords = [bbox[0][0] for bbox, text, prob in results] # Get top-left x coordinate of each bbox
   if not x_coords:
      return [], [] # Return empty lists if no words detected

   average_x = sum(x_coords) / len(x_coords)

   # 2. Iterate through the results and assign words to columns
   for bbox, text, prob in results:
       x_coord = bbox[0][0] # Top-left x coordinate
       if x_coord < average_x:
           english_words.append((text, bbox))
       else:
           french_words.append((text, bbox))

   return english_words, french_words




if __name__ == "__main__":
   results = capture_and_ocr()
   english_col, french_col = detect_columns(results)

   print("English Column:")
   for word, bbox in english_col:
       print(f"  {word} - Bounding Box: {bbox}")

   print("\nFrench Column:")
   for word, bbox in french_col:
       print(f"  {word} - Bounding Box: {bbox}")
