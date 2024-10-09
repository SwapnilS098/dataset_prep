-dataset_builder.py is a script to 
        -combine the dataset and the augmented dataset into a single directory
        - we can make the combined dataset as grayscale also

        -split the dataset into test and train with the desired ratio
        -we can make the split dataset in the grayscale also


-augmented_dataset_builder.py

        -this script makes the augmented dataset form the original dataset
        -performs random rotation and birghtness and scaling etc
        -generates the images in the HD resolution only for now does not allow to change the resolution
        -Requires PyTorch for running the script


-create_dataset.py
        -script for the just picking some images from the the dataset path and
        exporting them to different path to make a subset of the main dataset
        -input the dataset path
        -number of images to be picked
        -export directory where the images are to be exported