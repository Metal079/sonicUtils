
import shutil
import timeit

from datasets import load_dataset, ClassLabel, Value, Image, Features, load_metric
import evaluate
from transformers import AutoImageProcessor, pipeline
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor

from transformers import ConvNextFeatureExtractor, DeiTImageProcessor, DeiTForImageClassification, ImageClassificationPipeline, DeiTPreTrainedModel, PreTrainedModel, AutoModelForImageClassification
import torch
#from optimum.pipelines import pipeline
from optimum.bettertransformer import BetterTransformer

from optimum.onnxruntime.configuration import AutoQuantizationConfig

import numpy as np

import os

#folder_path = r'C:\Users\metal\Documents\programming\sonic_image classifier\SonicAestheticClassifier\onnx_model'
folder_path = r'C:\Users\metal\Documents\programming\sonic_image classifier\SonicAestheticClassifier\deit_best_87_5'
file_paths = []

#model = AutoModelForImageClassification.from_pretrained(folder_path)
#model = AutoModelForImageClassification.from_pretrained(folder_path)
#model = model.to(0)
#model = BetterTransformer.transform(model)


# create ORTOptimizer and define optimization configuration
#optimizer = ORTQuantizer.from_pretrained(model)
#quantization_config = AutoQuantizationConfig.tensorrt(is_static=False)

#onnx_path = r"C:\Users\metal\Documents\programming\sonic_image classifier\SonicAestheticClassifier\onnx_model"
# apply the optimization configuration to the model
#optimizer.quantize(save_dir=onnx_path, quantization_config=quantization_config)

#model = ORTModelForImageClassification.from_pretrained(onnx_path)


for root, dirs, files in os.walk(r"C:\Users\metal\gallery-dl\deviantart\Tags"):
    for file in files:
        if file.endswith('.txt') or file.endswith('.json') or file.endswith('.bat'):
            continue
        else:
            file_paths.append(os.path.join(root, file))

vision_classifier = pipeline(task="image-classification", 
                            model=folder_path, 
                            config=r"C:\Users\metal\Documents\programming\sonic_image classifier\SonicAestheticClassifier\deit_best_87_5\config.json", 
                            #accelerator="bettertransformer",
                            device=0,
                            )
image_predictions = {}


def classify_images():
    for image in file_paths:
        try:
            image_predictions[image] = vision_classifier(images=image)
        except:
            print('Error with image: ' + image)
            continue
        for char in image_predictions[image]:
            if char['label'] == 'idw' and char['score'] > 0.6:
                dest_dir_path = r"C:\Users\metal\gallery-dl\aesthetic_test\charlie_train_set"
                shutil.copy(image, dest_dir_path)
                # Check if label file exists
                #if os.path.exists(os.path.splitext(image)[0] + '.txt'):
                    #shutil.copy(os.path.splitext(image)[0] + '.txt', dest_dir_path)
                    #pass
                #else:
                    #print('No txt file for ' + image)
                    #pass
                break
            
            else:
                dest_dir_path = r"C:\Users\metal\gallery-dl\aesthetic_test\bad"
                shutil.copy(image, dest_dir_path)
                break

starttime = timeit.default_timer()
print("The start time is :",starttime)
classify_images()
print("The time difference is :", timeit.default_timer() - starttime)

#preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
#print(preds)