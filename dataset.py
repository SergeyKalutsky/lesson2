import numpy as np
import torch
import os
from torch.utils.data import Dataset
import cv2


class CatDogDataset(Dataset):

    def __init__(self, mode, transforms=None, img_size=(224, 224)):

        super().__init__()
        self.class_to_int = {'cat': 0, 'dog': 1}
        self.mode = mode
        self.dir = 'train' if self.mode == 'train' else 'test'
        self.imgs = self._get_filenames()
        self.transforms = transforms
        self.img_size = img_size

    def _get_filenames(self):
        return os.listdir(self.dir)

    def __getitem__(self, idx):

        image_name = self.imgs[idx]

        # Reading, converting and normalizing image
        img = cv2.imread(self.dir + '/' + image_name, cv2.IMREAD_COLOR)
        img = cv2.resize(img, self.img_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
        img /= 255.
        img = torch.from_numpy(img).permute(2, 0, 1)

        if self.mode == "train" or self.mode == "val":

            label = self.class_to_int[image_name.split(".")[0]]
            label = torch.tensor(label, dtype=torch.float32)

            if self.transforms:
                img = self.transforms(img)

            return img, label

        elif self.mode == "test":
            # Apply Transforms on image
            if self.transforms:
                img = self.transforms(img)
            return img

    def __len__(self):
        return len(self.imgs)


def read_img_test(path, device):
    # Reading, converting and normalizing image
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
    img /= 255.
    img = img[..., np.newaxis]
    img = torch.from_numpy(img).permute(3, 2, 0, 1)
    img.to(device)
    return img
