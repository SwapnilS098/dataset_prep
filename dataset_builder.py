import os
from PIL import Image
import argparse
from tqdm import tqdm

"""
    Code generated using the COPILOT in the VS Code
    -takes the images from two different directories
    -rename the images and export those image from both directories to the
    third directory.
"""


def file_handling(path):
    
    """
    Returns the list of the images in the directory path 
    given as input.
    
    """
    files=os.listdir(path)
    images=[]
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            images.append(file)
    print("Images: ",len(images))
    if len(images)==0:
        print("No images found in the directory")
        
    return images

def combine_dataset(org_dataset,aug_dataset,fine_tuning_image_dataset_path,gray=False):
    fine_tuning_dataset=[]
    org_images=file_handling(org_dataset)
    aug_images=file_handling(aug_dataset)
    print("Original Images: ",len(org_images))
    print("Augmented Images: ",len(aug_images))
    for image in aug_images:
        fine_tuning_dataset.append(image)
    for image in org_images:
        fine_tuning_dataset.append(image)
        
    print("Total Images: ",len(fine_tuning_dataset))
    
    #checking the fine tuning dataset path
    if not os.path.exists(fine_tuning_image_dataset_path):
        os.makedirs(fine_tuning_image_dataset_path)
        print("Fine tuning dataset path created at: ",fine_tuning_image_dataset_path)
    
    if gray==False:
    #exporting the fine tuning dataset to the disc
        count=0
        for image in org_images:
            img=Image.open(os.path.join(org_dataset,image))
            image_name="image_"+str(count)+".png"
            img.save(os.path.join(fine_tuning_image_dataset_path,image_name),format="PNG")
            print("Done for image: ",image)
            count+=1
        count+=1
        for image in aug_images:
            img=Image.open(os.path.join(aug_dataset,image))
            image_name="image_"+str(count)+".png"
            img.save(os.path.join(fine_tuning_image_dataset_path,image_name),format="PNG")
            print("Done for image: ",image)
            count+=1
    else:  #making the gray dataset
        count=0
        for image in org_images:
            img=Image.open(os.path.join(org_dataset,image)).convert("L")
            image_name="image_"+str(count)+".png"
            img.save(os.path.join(fine_tuning_image_dataset_path,image_name),format="PNG")
            print("Done for image: ",image)
            count+=1
        count+=1
        for image in aug_images:
            img=Image.open(os.path.join(aug_dataset,image)).convert("L")
            image_name="image_"+str(count)+".png"
            img.save(os.path.join(fine_tuning_image_dataset_path,image_name),format="PNG")
            print("Done for image: ",image)
            count+=1
        
def test_train_builder(dataset_path,gray,ratio):
    """
    Makes the test and the train split of the in the same directory as the dataset path
    
    ratio is the ratio of the number of images in the test and the train dataset 
    by default it is taken as 0.2
    
    """
    
    #checking if the dataset path is valid
    if not os.path.exists(dataset_path):
        print("Dataset path does not exists")
        return 
    
    #get the images list
    images=file_handling(dataset_path)
    if len(images)<10:
        print("Not enough images to make the test and train split")
        return
    
    #checking the ratio
    if ratio<0.1 or ratio>=1:
        print("Invalid ratio value, HENCE using ratio=0.2")
        ratio=0.2
    
    #deciding the number of images in the test and the train dataset
    test_count=int((ratio)*len(images))
    print("Test Count: ",test_count)
    train_count=len(images)-test_count
    print("Train Count: ",train_count)
    
    
    #Making the test and train directories in the dataset path directory
    if not os.path.exists(os.path.join(dataset_path,"train")):
        os.makedirs(os.path.join(dataset_path,"train"))
        train_path=os.path.join(dataset_path,"train")
    else :
        train_path=os.path.join(dataset_path,"train")
    
    if not os.path.exists(os.path.join(dataset_path,"test")):
        os.makedirs(os.path.join(dataset_path,"test"))
        test_path=os.path.join(dataset_path,"test")
    else:
        test_path=os.path.join(dataset_path,"test")
        
    if gray==False:
        #not required to open the file if simple moving from 1 dir to another
        
        #destination_path=os.path.join(test_path,image)
        #os.rename(source_path,destination_path)
        for image in tqdm(images):
            #img=Image.open(os.path.join(dataset_path,image))
            source_path=os.path.join(dataset_path,image)
            
            if test_count>0:
                #img.save(os.path.join(test_path,image)) #saving the images in the original format
                destination_path=os.path.join(test_path,image)
                if os.path.exists(destination_path):
                    print(image,"File already exists")
                    continue
                else:
                    os.rename(source_path,destination_path)
                test_count-=1
                
            else: #saving the images in the train directory
                destination_path=os.path.join(train_path,image)
                #img.save(os.path.join(train_path,image))
                if os.path.exists(destination_path):
                    print(image,"File already exists")
                    continue
                else:
                    os.rename(source_path,destination_path)
                
    else: #make the gray dataset
        #here it is necessary to open the file and convert it to gray scale
        for image in tqdm(images):
            img=Image.open(os.path.join(dataset_path,image)).convert("L")
            if test_count>0:
                img.save(os.path.join(test_path,image)) #saving the images in the original format
                test_count-=1
            else: #saving the images in the train directory
                img.save(os.path.join(train_path,image))
                
    print("Test and Train dataset created at: ",dataset_path)
    
def reverse_test_train_builder(dataset_path):
    """
    function to reverse the test and train split and create the directory
    containing all the test and train images in the same directory.
    """
    if os.path.exists(os.path.join(dataset_path,"train")) and os.path.exists(os.path.join(dataset_path,"test")):
        train_path=os.path.join(dataset_path,"train")        
        test_path=os.path.join(dataset_path,"test")
        
    print("Train and test path exists in the directory")
    
    #get the list of images in the test and the train direcotry
    test_images=file_handling(test_path)
    train_images=file_handling(train_path)
    
    for image in test_images:
        source_path=os.path.join(test_path,image)
        destination_path=os.path.join(dataset_path,image)
        os.rename(source_path,destination_path)
    
    for image in train_images:
        source_path=os.path.join(train_path,image)
        destination_path=os.path.join(dataset_path,image)
        os.rename(source_path,destination_path)
        
    #remove the test and train directory
    os.rmdir(test_path)
    os.rmdir(train_path)
    
def make_gray_dataset(dataset_path,gray_dataset_path):
    """
    Function to make a gray dataset from the original dataset at the 
    gray dataset path.
    
    """
    print("Making the gray dataset")
    #check if the dataset path exists
    if not os.path.exists(dataset_path):
        print("Dataset path does not exists")
        return
    
    #get the images list
    images=file_handling(dataset_path)
    if len(images)==0:
        print("No images found in the dataset")
        return
    
    #checking if the gray dataset path exists
    if not os.path.exists(gray_dataset_path):
        os.makedirs(gray_dataset_path)
        print("Gray dataset path created at: ",gray_dataset_path)
        
    #converting the images to gray scale
    for image in tqdm(images):
        img=Image.open(os.path.join(dataset_path,image)).convert("L")
        img.save(os.path.join(gray_dataset_path,image))
        
    print("Gray dataset created at: ",gray_dataset_path)
    
def main(args):
    print(args.combine,args.test_train_builder,args.gray)
    
    if args.combine==True and args.gray==True:
        
        combine_dataset(args.image_dataset_path,args.augmented_dataset_path,args.fine_tuning_dataset_path,gray=True)
    elif args.combine==True and args.gray==False:
        combine_dataset(args.image_dataset_path,args.augmented_dataset_path,args.fine_tuning_dataset_path)
        
    if args.test_train_builder==True and args.gray==True:
        test_train_builder(args.image_dataset_path,args.gray,args.ratio)
    elif args.test_train_builder==True and args.gray==False:
        test_train_builder(args.image_dataset_path,args.gray,args.ratio)
        
    if args.reverse_test_train_builder==True:
        reverse_test_train_builder(args.image_dataset_path)
        
    if args.gray_dataset_path!=None:
        make_gray_dataset(args.image_dataset_path,args.gray_dataset_path)

    
    

if __name__ == "__main__":
        
    parser=argparse.ArgumentParser()
    
    parser.add_argument("--image_dataset_path",type=str,help="Path to the original image dataset")
    parser.add_argument("--augmented_dataset_path",type=str,help="Path to the augmented image dataset")
    parser.add_argument("--fine_tuning_dataset_path",type=str,help="Path to save the fine tuning dataset")
    parser.add_argument("--gray_dataset_path",type=str,help="Path to save the gray dataset")
    parser.add_argument("--combine",action='store_true',help="Combine the original and the augmented dataset")
    parser.add_argument("--test_train_builder",action="store_true",help="Make the test and train split of the dataset")
    parser.add_argument("--gray",action="store_true",default=False,help="Convert the images to gray scale")
    parser.add_argument("--ratio",type=float,default=0.2,help="Ratio of the test and the train split between 0.1 to 1")
    parser.add_argument("--reverse_test_train_builder",action="store_true",help="Reverse the test and the train split")
    
    args=parser.parse_args()
    main(args)
    
    

