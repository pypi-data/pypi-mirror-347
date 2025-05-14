import unittest
from PIL import Image
import numpy
import os
from img_to_vec import Img2Vec

test_image = os.path.join("..","example", 'test_images', 'cat.jpg')
class TestImg2Vec(unittest.TestCase):
    def test_default(self):
        img2vec = Img2Vec()
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(512, vec.size)
        
    def test_resnet18(self):
        img2vec = Img2Vec(model='resnet18')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(512, vec.size)
        
    def test_resnet34(self):
        img2vec = Img2Vec(model='resnet34')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(512, vec.size)
        
    def test_resnet50(self):
        img2vec = Img2Vec(model='resnet50')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(2048, vec.size)
        
    def test_resnet101(self):
        img2vec = Img2Vec(model='resnet101')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(2048, vec.size)
    
    def test_resnet152(self):
        img2vec = Img2Vec(model='resnet152')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(2048, vec.size)

    def test_alexnet(self):
        img2vec = Img2Vec(model='alexnet')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(4096, vec.size)

    def test_vgg(self):
        img2vec = Img2Vec(model='vgg')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(4096, vec.size)
    
    def test_vgg11(self):
        img2vec = Img2Vec(model='vgg11')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(4096, vec.size)
    
    def test_vgg13(self):
        img2vec = Img2Vec(model='vgg13')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(4096, vec.size)
        
    def test_vgg16(self):
        img2vec = Img2Vec(model='vgg16')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(4096, vec.size)
    
    def test_vgg19(self):
        img2vec = Img2Vec(model='vgg19')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(4096, vec.size)

    def test_densenet(self):
        img2vec = Img2Vec(model='densenet')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1024, vec.size)
    
    def test_densenet121(self):
        img2vec = Img2Vec(model='densenet121')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1024, vec.size)
        
    def test_densenet161(self):
        img2vec = Img2Vec(model='densenet161')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(2208, vec.size)
    
    def test_densenet169(self):
        img2vec = Img2Vec(model='densenet169')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1664, vec.size)
    
    def test_densenet201(self):
        img2vec = Img2Vec(model='densenet201')
        img = Image.open(test_image).convert('RGB')
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1920, vec.size)

    def test_efficientnet_b0(self):
        img2vec = Img2Vec(model='efficientnet_b0')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1280, vec.size)

    def test_efficientnet_b1(self):
        img2vec = Img2Vec(model='efficientnet_b1')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1280, vec.size)

    def test_efficientnet_b2(self):
        img2vec = Img2Vec(model='efficientnet_b2')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1408, vec.size)

    def test_efficientnet_b3(self):
        img2vec = Img2Vec(model='efficientnet_b3')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1536, vec.size)

    def test_efficientnet_b4(self):
        img2vec = Img2Vec(model='efficientnet_b4')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(1792, vec.size)

    def test_efficientnet_b5(self):
        img2vec = Img2Vec(model='efficientnet_b5')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(2048, vec.size)

    def test_efficientnet_b6(self):
        img2vec = Img2Vec(model='efficientnet_b6')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(2304, vec.size)

    def test_efficientnet_b7(self):
        img2vec = Img2Vec(model='efficientnet_b7')
        img = Image.open(test_image)
        vec = img2vec.get_vec(img)
        self.assertEqual(True, isinstance(vec, numpy.ndarray))
        self.assertEqual(1, vec.ndim)
        self.assertEqual(2560, vec.size)

if __name__ == "__main__":
    unittest.main()