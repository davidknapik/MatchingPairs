import csv
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
   reader = easyocr.Reader(['en', 'fr'], gpu=False)  # English and French

   # Perform OCR using EasyOCR
   results = reader.readtext(np.array(img), min_size=0, ycenter_ths=0.9,height_ths=0.9, width_ths=0.9, decoder='greedy' )

   # Print the detected text and bounding boxes
   for (bbox, text, prob) in results:
      (top_left, top_right, bottom_right, bottom_left) = bbox
      tl=(int(top_left[0]), int(top_left[1]))

      # print(f"Text: {text}, Confidence: {prob}, Coordinates: {tl}")
      # print(f"Text: {text}, Coordinates: {tl}")

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
      pos = -1
      x_coord = bbox[0][0] # Top-left x coordinate
      y_coord = bbox[0][1] 

      # print(f"{text} : ({x_coord} , {y_coord})")

      if x_coord < average_x:
         if 1 <= y_coord <= 60:
            pos = 1
         elif 60 <= y_coord <= 120:
            pos = 2
         elif 120 <= y_coord <= 180:
            pos = 3
         elif 180 <= y_coord <= 240:
            pos = 4
         elif 240 <= y_coord <= 300:
            pos = 5

         english_words.append((text, pos))

      else:
         if 1 <= y_coord <= 60:
            pos = 6
         elif 60 <= y_coord <= 120:
            pos = 7
         elif 120 <= y_coord <= 180:
            pos = 8
         elif 180 <= y_coord <= 240:
            pos = 9
         elif 240 <= y_coord <= 300:
            pos = 0
           
         french_words.append((text, pos))

   return english_words, french_words


def load_translation_library(filename):
   #Example loading from a CSV file
   translation_dict = {}
   with open(filename, 'r', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
         if len(row) == 2: #Ensure each row has two columns
            english_word = row[0].strip().lower() #Normalize the words
            french_word = row[1].strip().lower()
            if english_word in translation_dict:
               translation_dict[english_word].append(french_word)
            else:
               translation_dict[english_word] = [french_word] # Initialize as a list   
   return translation_dict


# def translate_and_match(english_col, french_col, translation_library):
#    matched_translations = []
#    missing_translations = []
#    mismatched_translations = []

#    for english_word, english_pos in english_col:
#       english_word_lower = english_word.strip().lower()  # Normalize to lowercase
#       if english_word_lower in translation_library:
#          expected_french_word = translation_library[english_word_lower]
#          # Find if expected_french_word exists in french_col
#          found_match = False
#          for french_word, french_pos in french_col:
#             french_word_lower = french_word.strip().lower()
#             if expected_french_word == french_word_lower:
#                matched_translations.append((english_pos, french_pos, english_word, french_word))
#                found_match = True
#                break # Stop searching once a match is found
#          if not found_match:
#             mismatched_translations.append((english_word, expected_french_word))
#       else:
#          missing_translations.append(english_word)

#    return matched_translations, missing_translations, mismatched_translations



def translate_and_match(english_col, french_col, translation_library):
   matched_translations = []
   missing_translations = []
   mismatched_translations = []

   for english_word, english_pos in english_col:
       english_word_lower = english_word.strip().lower()
       if english_word_lower in translation_library:
           possible_french_words = translation_library[english_word_lower] # List of translations

           found_match = False
           for expected_french_word in possible_french_words:
               for french_word, french_pos in french_col:
                   french_word_lower = french_word.strip().lower()
                   if expected_french_word == french_word_lower:
                       matched_translations.append((english_pos, french_pos, english_word, french_word))
                       found_match = True
                       break # Stop searching french_col once a match is found
               if found_match:
                   break # Stop searching possible_french_words once a match is found

           if not found_match:
               mismatched_translations.append((english_word, possible_french_words)) #Store the list

       else:
           missing_translations.append(english_word)

   return matched_translations, missing_translations, mismatched_translations

if __name__ == "__main__":

   translation_library_file = "fr_en_dictionary.csv"  # Replace with your file
   translation_library = load_translation_library(translation_library_file)

   results = capture_and_ocr()
   english_col, french_col = detect_columns(results)

   print("English Column:")
   for word, pos in english_col:
       print(f"  {word} - {pos}")

   print("\nFrench Column:")
   for word, pos in french_col:
       print(f"  {word} - {pos}")

   matched, missing, mismatched = translate_and_match(english_col, french_col, translation_library)

   print("")
   print("Matched Translations")
   for match in matched:
      print(f"{match}")

   print("")
   print("Missing Translations:")
   for miss in missing:
      print(f"{miss}")

   print("")
   print("Mismatched Translations:", mismatched)

   # for word1, word2 in matched:
   #     print(f"{english_col.index(word1)[0]} {word1}, {french_col.index(word2)[0]} {word2}")

