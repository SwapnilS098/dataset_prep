"""
    Pyhton program for the COLMAP 10 docker container for
    loading the images and then performing some operation
    and then exporting them to the export path.

    Need the pass the path as the string for this program to work
"""
import shutil
import os
import argparse


def images_handling(images_path):

    print("Images import path is:",images_path)

    lst=os.listdir(images_path)

    images=[] #empty list for th images only

    for image in lst:
        if image.lower().endswith('.png') or image.lower().endswith('.jpeg') or image.lower().endswith('.jpg') or image.lower().endswith('.webp'):
            images.append(image)
    print("Number of images in the directory are:",len(images),"type:",images[0].split('.')[1])
    
    #sort the images list
    if len(images)!=0:
        images.sort()

    return images, images_path
    
def make_dataset(images,dataset_size,export_path=None):
    """
    Program to make the dataset of dataset_size given in the function at the export path

    
    """

    print("dataset_size_received:",dataset_size)
    #check if the dataset size is valid
    if dataset_size>len(images):
        print("Error , the dataset size must be smaller or equal to the images dataset")
        return

    #check if the path exists
    if export_path is not None:
        if os.path.exists(export_path):
            print("Export path is fine",export_path)
        else:
            #make the given export_path
            os.makedirs(export_path)
            print("Given export path created")
    else:
        #make the export path in the images path directory only
        export_path=os.path.join(images_path,"export_path")
        try:
            os.makedirs(export_path)
        except:
            print("Default export already exists")
        print("Export_path directory is created")

    for idx,image in enumerate(images):
        if idx>dataset_size:
            break
        export_path_image=os.path.join(export_path,image)
        source_path=os.path.join(images_path,image)
        #os.copy(source_path,export_path_image)
        shutil.copy(source_path,export_path_image)
    print("Dataset is exported")
    


if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Load and optionally export the image dataset")
    parser.add_argument('images_path',help="Path to the input directory where the images exists")
    parser.add_argument('dataset_size',help="number of images to be copied from the source to the destination")
    parser.add_argument('--export_path',help="Path to the output or the export directory where the dataset will be exported")
    
    args=parser.parse_args()

    images,images_path=images_handling(args.images_path)
    images=make_dataset(images,int(args.dataset_size),args.export_path)
    if args.export_path:
        print(f'Exported images to {args.export_path}')
