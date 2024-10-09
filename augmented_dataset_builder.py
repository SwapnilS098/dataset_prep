
import argparse
import os
import random
from PIL import Image
import torch
from torchvision import transforms
from tqdm import tqdm  # For progress bar

# Function to apply augmentations and save images
def augment_image(image, output_dir, augmentations, augment_factor=5):
    """
    Apply augmentations to an image and save the augmented images.

    :param image: PIL Image object
    :param output_dir: Directory where augmented images will be saved
    :param augmentations: List of transformations to apply
    :param augment_factor: Number of augmentations to create per image
    """
    for i in range(augment_factor):
        augmented_image = augmentations(image)
        augmented_image.save(os.path.join(output_dir, f"aug_{i}_{random.randint(0, 10000)}.png"))
        
def file_handling(dataset_path):
    files=os.listdir(dataset_path)
    
    images=[]
    
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append(file)
    print("Images in the dataset: ",len(images))
    print("images format is:",images[0].split('.')[-1])
    
    return images


# Function to generate augmented dataset
def generate_augmented_dataset(input_dir, output_dir, augment_factor=5):
    """
    Generate an augmented dataset from existing images.

    :param input_dir: Directory of the original images
    :param output_dir: Directory to save the augmented images
    :param augment_factor: Number of augmentations to create per image
    """
    # Define transformations for augmentations
    augmentations = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(degrees=15),         # Random rotation between -15 to 15 degrees
        transforms.ColorJitter(brightness=0.2,         # Random brightness changes
                               contrast=0.2, 
                               saturation=0.2, 
                               hue=0.1),
        transforms.RandomResizedCrop(size=(256, 256), scale=(0.8, 1.0))  # Random crop and resize
    ])
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    images=file_handling(input_dir)
    images=tqdm(images)
    
    for image in images:
        image_path=os.path.join(input_dir,image)
        image = Image.open(image_path)
        augment_image(image, output_dir, augmentations, augment_factor)
        #print("done for image:",image)
    
        
def main(args):
    generate_augmented_dataset(args.dataset_dir, args.output_dir, args.augment_factor)
    print(f"Augmented dataset created at {args.output_dir}")

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    
    parser.add_argument('--dataset_dir', type=str, required=True, help='Path to the existing dataset')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to save the augmented dataset')
    parser.add_argument('--augment_factor', type=int, default=5, help='Number of augmentations per image Eg. for factor 5, 5 new images will be created for each original image')

    args=parser.parse_args()
    main(args)