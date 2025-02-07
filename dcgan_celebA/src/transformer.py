import torchvision.transforms as transforms
from PySide2 import QtGui, QtCore
import sys
sys.modules['PyQt5.QtGui'] = QtGui
from PIL import Image, ImageQt
import numpy as np
import torch

class Transformer():
    def __init__(self, crop=128):
        self.to_tensor = transforms.ToTensor()
        #self.to_grey = transforms.Grayscale()
        self.to_pil_image = transforms.ToPILImage()
        self.center_crop = transforms.CenterCrop(crop)
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    def pil2pixmap1(self, im):
        if im.mode == "RGB":
            im = im.convert("RGBA")
        elif im.mode == "L":
            im = im.convert("RGBA")
        data = im.convert("RGBA").tobytes("raw", "RGBA")
        qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)
        return pixmap

    def pil2pixmap(self, im):
        im = ImageQt.ImageQt(im)
        return QtGui.QPixmap.fromImage(im)

    def tensor2im(self, input_image, imtype=np.uint8):
        if isinstance(input_image, torch.Tensor):
            image_tensor = input_image.data
        else:
            return input_image
        image_numpy = image_tensor[0].cpu().float().numpy()
        if image_numpy.shape[0] == 1:
            image_numpy = np.tile(image_numpy, (3, 1, 1))
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
        return image_numpy.astype(imtype)

