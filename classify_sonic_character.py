
from datasets import load_dataset, ClassLabel, Value, Image, Features, load_metric
import evaluate
from transformers import AutoImageProcessor, pipeline
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor

from transformers import ViTFeatureExtractor, ViTForImageClassification, TrainingArguments, Trainer, ConvNextFeatureExtractor, DeiTImageProcessor, DeiTForImageClassification, ImageClassificationPipeline
import torch

import numpy as np

import os

class MultiClassLabel(ImageClassificationPipeline):
    def postprocess(self, model_outputs, top_k=5):
        if top_k > self.model.config.num_labels:
            top_k = self.model.config.num_labels

        if self.framework == "pt":
            probs = model_outputs.logits.sigmoid()[0]
            scores, ids = probs.topk(top_k)
        elif self.framework == "tf":
            probs = stable_softmax(model_outputs.logits, axis=-1)[0]
            topk = tf.math.top_k(probs, k=top_k)
            scores, ids = topk.values.numpy(), topk.indices.numpy()
        else:
            raise ValueError(f"Unsupported framework: {self.framework}")

        scores = scores.tolist()
        ids = ids.tolist()
        return [{"score": score, "label": self.model.config.id2label[_id]} for score, _id in zip(scores, ids)]


#folder_path = r'C:\Users\metal\Documents\programming\sonic_image classifier\SonicCharacterClassifier\latest'
folder_path = r'C:\Users\metal\Documents\programming\sonic_image classifier\SonicCharacterClassifier\checkpoint-8740'
#folder_path = r'C:\Users\metal\Documents\programming\sonic_image classifier\SonicCharacterClassifier\best_32_cleaned'
file_paths = []

for root, dirs, files in os.walk(r"C:\Users\metal\gallery-dl\deviantart\Tags\sonic_the_hedgehog\deviantart_495976863_Sonic's Winter Dream.jpg"):
    for file in files:
        if file.endswith('.txt'):
            continue
        else:
            file_paths.append(os.path.join(root, file))

vision_classifier = pipeline(task="image-classification", model=folder_path, config=r"C:\Users\metal\Documents\programming\sonic_image classifier\SonicCharacterClassifier\checkpoint-8740\config.json", pipeline_class=MultiClassLabel, top_k=5)
image_predictions = {}
'''
for image in file_paths:
    image_predictions[image] = vision_classifier(images=image)
'''
preds = vision_classifier(images=r"C:\Users\metal\Downloads\FlFrxbgWIAAem9e.jfif")

preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
print(preds)