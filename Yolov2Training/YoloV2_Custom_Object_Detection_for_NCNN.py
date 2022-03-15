# -*- coding: utf-8 -*-
"""MaixDuino_Hedef_Tanıma.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UPYZnBF4UzQeZnGl_1TV6MeZ8aOw0dEH

181220027 - Şahin Emre ASLAN
#Son Gelişmeler:
* Oluşturulan veriler yüksek boyutlu olduğu için eğitim(model training) sürecinde sorun yaşandı.
* Yaşanan sorun çözüldü,model eğitildi.
  #fotoğrafın pixel değerleri modelin girdilerine uygun hale getirildi
* Config dosyası içerisinde düzenleme yapılmadan model direk eğitilemez.Lokal olarak upload ederek modeli kendi nesnemi tanıyacak şekilde eğittim.
* Modelin donanıma uygun hale getirilmesi gerekiyor.

* Model başarıyla donanıma "NCC" yazılımıyla donanıma uygun hale getirildi.Modelin başarımının arttırması yönünde çalışmalar yapılmaya çalışılıyor.

* Model eğitildi,beklenen başarım görülmedi.Belirlenen ve başarısız olan hiperparametreler:
  * epochs = 20, batch-size = 30, learn-rate = 1e-15
* Veriseti arttırılacak,Model tekrardan eğitilecektir..(16.05.21)
"""

!git clone https://github.com/sipeed/maix_train --recursive #kullanılan github reposu

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/maix_train

!pip3 install -r requirements.txt #kullanılan kütüphanelerin versiyon gereksinimleri

import shutil
import os
#githubdan çektiğimiz içinde yüklü olan verisetilerini siliyoruz
!rm -r /content/sample_data
!rm -r /content/maix_train/datasets/test-TFRecords-export.zip 
!rm -r /content/maix_train/datasets/test_classifier_datasets.zip 
!rm -r /content/maix_train/datasets/test_detector_xml_format.zip

#kendi verisetimi yüklüyorum
  #Transfer Learning = xml_format_TL.zip
  #default dataset = xml_format_dataset.zip
!gdown https://drive.google.com/uc?id=1kh1ZBc84WdKL6nSQckzpRpC6Js153nGn
#shutil.move("xml_format2.zip","datasets")

#transfer learning
!gdown https://drive.google.com/uc?id=1Ru_sAYgVQzHuPLYdEIzM3aCRTyZ12qAd
!gdown https://drive.google.com/uc?id=1Fg2zZK6kP9IYzavS1NAcvJmtK-lUbsn_
!rm -r /content/maix_train/train/classifier/__init__.py
shutil.move("__init__.py","/content/maix_train/train/classifier/__init__.py")

!python3 train.py init #config dosyası oluşturur

!gdown https://drive.google.com/uc?id=17QlZfTJq7t4QNXH0GTZcVnTM-tLODpqg #kendi config dosyamı yüklüyor
shutil.move("config.py","/content/maix_train/instance/config.py") #taşıma

# Commented out IPython magic to ensure Python compatibility.
#dönüştürücü yazılımı yüklenmesi .h5 to .kmodel
!wget -P /content/maix_train/tools/ncc/ncc_v0.1 https://github.com/kendryte/nncase/releases/download/v0.1.0-rc5/ncc-linux-x86_64.tar.xz
# %cd /content/maix_train/tools/ncc/ncc_v0.1
!tar xvf /content/maix_train/tools/ncc/ncc_v0.1/ncc-linux-x86_64.tar.xz

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/maix_train
!python3 train.py -t detector -z /content/maix_train/datasets/xml_format_HQ_tf.zip train

"""#Transfer Learning"""



"""#Test Section
This is section in OV2640 used camera images.


"""

import os, sys
import cv2
from collections import Iterable

from dataset import Dataset_Folder, Dataset_VOC
from dataloader import DataLoader
from logger import Logger
from augmentations import SSDAugmentationTest, DeNormalize
from draw import Draw

class Net_Test:
    def __init__(self, dataset, classes, net_type, saved_state_path, input_shape=(3, 240, 240), anchors = None, temp_dir=None, conf_thresh=0.3, nms_thresh=0.3, opt = {}, log = Logger(), device="cuda"):
        '''
            @input_layout only support default now, pytorch is chw, tensorflow is hwc
        '''
        self.classes = classes
        self.net_type = net_type
        self.log = log
        self.anchors = self.val_anchors(anchors)
        self.input_shape = input_shape
        if not temp_dir:
            temp_dir = os.path.join("out", net_type, "test_result")
        self.temp_dir = temp_dir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.root = os.path.abspath(os.path.dirname(__file__))
        detectors_path = os.path.join(self.root, "detectors")
        sys.path.insert(0, detectors_path)
        self.detector = __import__(net_type)
        try:
            self.framework = self.detector.framwork
        except Exception:
            self.framework = "torch"
        self.tester = self.detector.Test(
                            self.classes, self.anchors,
                            (self.input_shape[2], self.input_shape[1]),
                            saved_state_path,
                            self.log,
                            conf_thresh,
                            nms_thresh,
                            device
                        )
        self.dataset = dataset
        self.curr_idx = 0
        self.draw = Draw(self.classes)
    
    def detect(self, index = -1, get_img_path = False):
        if index >= 0:
            img = self.dataset[index]
            img_raw = self.dataset.pull_image(index, get_img_path=get_img_path)
        else:    
            if self.curr_idx >= len(self.dataset):
                return None
            img = self.dataset[self.curr_idx] # img or (img, target)
            if isinstance(img, Iterable):
                img = img[0]
            img_raw = self.dataset.pull_image(self.curr_idx, get_img_path=get_img_path)
            self.curr_idx += 1
        boxes, probs, inds = self.tester.detect(img)
        return img_raw, boxes, probs, inds

    def show(self, img, boxes, probs, inds, save_path = None, threshold = -1):
        img = self.draw.draw_img(img, boxes, inds, self.classes, probs, threshold)
        if save_path:
            cv2.imwrite(save_path, img)
        

    def reset(self):
        self.curr_idx = 0

    def val_anchors(self, anchors):
        '''
            convert [w, h, w, h, ...] to [[w, h], [w, h], ...]
        '''
        if type(anchors[0]) == list or type(anchors[0]) == tuple:
            return anchors
        final = []
        for i in range(0, len(anchors)//2):
            final.append([anchors[i * 2], anchors[i * 2 + 1]])
        return final

if __name__ == "__main__":
    # classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "mouse", "microbit", "ruler", "cat", "peer", "ship", "apple", "car", "pan", "dog", "umbrella", "airplane", "clock", "grape", "cup", "left", "right", "front", "stop", "back"]
    # anchors = [[2.44, 2.25], [5.03, 4.91], [3.5, 3.53], [4.16, 3.94], [2.97, 2.84]]
    # param_path = "out/yolov2_slim/weights/epoch_460.pth"
    # test_dir = "datasets/cards/cap/left"


    classes = ["hedef"]
    anchors = [[1.87, 5.32], [1.62, 3.28], [1.75, 3.78], [1.33, 3.66], [1.5, 4.51]]
    param_path = "out/lobster_5classes/yolov2_slim/weights/epoch_15.pth"
    test_dir = "datasets/lobster_5classes"
    is_val_data = True

    input_shape=(3, 224, 224)

    log = Logger()

    if is_val_data:
        dataset = Dataset_VOC(classes, test_dir, sets=["val"], log = log,
                            transform = SSDAugmentationTest(size=input_shape[1:][::-1], mean=(0.5, 0.5, 0.5), std=(128/255.0, 128/255.0, 128/255.0))
                            )
    else:
        dataset = Dataset_Folder(test_dir,
                    transform = SSDAugmentationTest(size=input_shape[1:][::-1], mean=(0.5, 0.5, 0.5), std=(128/255.0, 128/255.0, 128/255.0)),
                    log = log
                    )
    test = Net_Test(dataset,
                classes,
                "yolov2_slim",
                param_path,
                input_shape=input_shape,
                anchors=anchors,
                conf_thresh=0.2,
                nms_thresh=0.3,
                log = log,
                device="cpu"
                )
    count = 0
    while 1:
        result = test.detect()
        if not result:
            break
        img, boxes, probs, inds = result
        out_jpg = "out/test.jpg"
        test.show(img, boxes, probs, inds, save_path=out_jpg)
        input(f"[{count}] see {out_jpg}, press any key to continue")
        count += 1

"""# Bundan sonraki aşamalarda modelin başarımı(acc) arttırılmaya çalışılacaktır."""

import zipfile
string = 'epoch20_batc10_learn-5.zip'
newZip = zipfile.ZipFile(string, 'w')
newZip.write(os.listdir('/content/maix_train/epoch20_batc10_learn-5'), compress_type=zipfile.ZIP_DEFLATED)
newZip.close()

#modeli google drive a çekme
import os
COLAB_MODEL ='/content/maix_train/epoch20_batc10_learn-5'
DRIVE_DIR = '/content/gdrive/My Drive/model_proje/'
shutil.copytree(COLAB_MODEL, DRIVE_DIR)

#Modelin Başarımını Ölçme
import matplotlib.pyplot as plt
import cv2
plt.figure()
plt.axis("off")
foto = cv2.imread("/content/maix_train/out/result_root_dir/maixhub_detector_result_2021_10_22__12_06/report.jpg")
plt.imshow(foto)

# Commented out IPython magic to ensure Python compatibility.
# show images inline
# %matplotlib inline

# automatically reload modules when they have changed
# %reload_ext autoreload
# %autoreload 2

# import keras
import keras

# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf

model_path = os.path.join('snapshots', sorted(os.listdir('snapshots'), reverse=True)[0])
print(model_path)

# load retinanet model
model = models.load_model(model_path, backbone_name='resnet50')
model = models.convert_model(model)

# load label to names mapping for visualization purposes
labels_to_names = pandas.read_csv(CLASSES_FILE,header=None).T.loc[0].to_dict()

def img_inference(img_path):
  image = read_image_bgr(img_infer)

  # copy to draw on
  draw = image.copy()
  draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

  # preprocess image for network
  image = preprocess_image(image)
  image, scale = resize_image(image)

  # process image
  start = time.time()
  boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
  print("processing time: ", time.time() - start)

  # correct for image scale
  boxes /= scale

  # visualize detections
  for box, score, label in zip(boxes[0], scores[0], labels[0]):
      # scores are sorted so we can break
      if score < THRES_SCORE
      {}
          break

      color = label_color(label)

      b = box.astype(int)
      draw_box(draw, b, color=color)

      caption = "{} {:.3f}".format(labels_to_names[label], score)
      print(caption)
      draw_caption(draw, b, caption)

  plt.figure(figsize=(10, 10))
  plt.axis('off')
  plt.imshow(draw)
  plt.show()

uploaded = files.upload()
img_infer = list(uploaded)[0]

print('Running inference on: ' + img_infer)
img_inference(img_infer)