import glob
import numpy as np
from PIL import Image
import os
import argparse
import sys

def process_images(directory):
    """Process all PNG images in the given directory."""
    # Verify directory exists and is a directory
    if not os.path.exists(directory):
        print(f"Error: {directory} does not exist.", file=sys.stderr)
        return 1
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory.", file=sys.stderr)
        return 1
    
    # Find all PNG images
    image_files = glob.glob(os.path.join(directory, "*.png"))
    if not image_files:
        print(f"Warning: No PNG files found in {directory}")
        return 0
    
    # Create save directory
    save_dir = f"{directory}_processed"
    os.makedirs(save_dir, exist_ok=True)
    
    # Process and save images
    for image_file in image_files:
        try:
            # Open the image and convert to grayscale
            img = Image.open(image_file)
            img_gray = img.convert('L')  # Convert image to grayscale
            img_array = np.array(img_gray)  # Convert grayscale image to numpy array
            
            # Convert to binary based on the cutoff of 100
            img_binary = np.where(img_array > 100, 1, 0)
            
            # Check if the image contains only binary values
            unique_values = np.unique(img_binary)
            valid_binary = (np.array_equal(unique_values, np.array([0, 1])) or 
                           np.array_equal(unique_values, np.array([0])) or 
                           np.array_equal(unique_values, np.array([1])))
            
            if not valid_binary:
                print(f"Error: {image_file} contains values other than 0 and 1 after binarization.")
                continue
                
            # Convert the binary array to uint8 for image saving
            img_binary_uint8 = (img_binary * 255).astype(np.uint8)
            
            # Create an image from the array
            img_binary_pil = Image.fromarray(img_binary_uint8, mode='L')
            
            # Get filename without path
            filename = os.path.basename(image_file)
            new_filepath = os.path.join(save_dir, filename)
            
            # Save the binary image as a PNG file with maximum compression
            img_binary_pil.save(new_filepath, format='PNG', compress_level=9, optimize=True)
            
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}", file=sys.stderr)
    
    print(f"All images saved as PNG in {save_dir}")
    return 0

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process images to binary format.')
    parser.add_argument('directory', type=str, help='Directory containing the PNG images to process')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process the images
    return process_images(args.directory)

if __name__ == "__main__":
    sys.exit(main())