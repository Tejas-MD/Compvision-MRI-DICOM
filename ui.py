import tkinter as tk
from tkinter import filedialog

import pydicom
import numpy as np
from PIL import Image


import cv2

selectedPath = False 


def dicom_to_image(input_path, output_path):
    try:
        # Read the DICOM file
        dcm = pydicom.dcmread(input_path)
        
        # Get the pixel data as a NumPy array
        pixel_array = dcm.pixel_array

        # Normalize pixel values to the 0-255 range (assuming 16-bit DICOM)
        normalized_array = (pixel_array / np.max(pixel_array) * 255).astype(np.uint8)

        # Create a PIL Image from the NumPy array
        image = Image.fromarray(normalized_array)
        
        # Save the image as a PNG file (you can use other formats like JPEG as needed)
        image.save(output_path, format="PNG")
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    


# Function to open a file dialog
def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        selectedPath = True
        file_label.config(text=f"Selected File: {file_path}")
    dicom_to_image(file_path,"output.png")


# Function to perform some action when Button 1 is clicked
def threshold():
        image1 = cv2.imread('output.png')
        ret, thresh4 = cv2.threshold(image1, 120, 255, cv2.THRESH_TOZERO)
        ret, thresh1 = cv2.threshold(image1, 120, 255, cv2.THRESH_BINARY)
        image1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
        ret, thresh2 = cv2.threshold(image1, 120, 255, cv2.THRESH_BINARY + 
                                            cv2.THRESH_OTSU)     
        
        # Pixel intensity is set to 0, for all the pixels intensity, less than the threshold value.
        cv2.imshow("Set to 0 Threshold",thresh4)
        
        # If pixel intensity is greater than the set threshold, value set to 255, else set to 0 (black).
        cv2.imshow("Set to Binary Threshold",thresh1)
        
        cv2.imshow("Adaptive Thershold",thresh2)
        
        result_label.config(text="Displaying threshold modification")
        
def hsv():
        img = cv2.imread('output.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        cv2.imshow("HSV",img)
        

# Function to perform some action when Button 2 is clicked
def erode_dilate():
    image1 = cv2.imread('output.png')
    kernel = np.ones((6, 6), np.uint8)
      # Using cv2.erode() method 
    image = cv2.erode(image1, kernel, cv2.BORDER_REFLECT)    
    image2 = cv2.dilate(image1,kernel)
    cv2.imshow("Erode Demo",image)
    cv2.imshow("Dilate Demo",image2)
    result_label.config(text="Function 2 executed")

# Create the main window
root = tk.Tk()
root.title("DICOM Image Processing Examples")

# Create a heading label
heading_label = tk.Label(root, text="Interesting Image Processing", font=("Helvetica", 16))
heading_label.pack()

# Create a label for the selected file
file_label = tk.Label(root, text="Selected File: None")
file_label.pack()

# Create a button to open a file dialog
open_file_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_file_button.pack()

# Create a heading for custom functions
functions_heading = tk.Label(root, text="Custom Functions", font=("Helvetica", 12))
functions_heading.pack()

# Create Buttons for custom functions
button_1 = tk.Button(root, text="Threshold", command=threshold)
button_1.pack()

button_2 = tk.Button(root, text="Erode/Dilate", command=erode_dilate)
button_2.pack()


button_3 = tk.Button(root, text="HSV", command=hsv)
button_3.pack()


# Create a label to display function results
result_label = tk.Label(root, text="")
result_label.pack()

# Start the GUI main loop
root.mainloop()
