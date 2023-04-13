
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


folder_path = r"/home/pablo/Downloads/programming/sonic_image classifier/SonicCharacterClassifier/checkpoint-3423"
file_paths = []

for root, dirs, files in os.walk(r"/media/pablo/6ED0B21ED0B1EC89/Users/metal/Downloads/sonic_training/datasets/delta_train_set"):
    for file in files:
        if file.endswith('.txt'):
            continue
        else:
            file_paths.append(os.path.join(root, file))

vision_classifier = pipeline(task="image-classification", 
                            model=folder_path, 
                            #config=r"C:\Users\metal\Documents\programming\sonic_image classifier\SonicCharacterClassifier\new_best_32\config.json", 
                            pipeline_class=MultiClassLabel, 
                            top_k=5,
                            device=0)
image_predictions = {}

for image in file_paths:
    try:
        image_predictions[image] = vision_classifier(images=image)
    except:
        print('Error with image: ' + image)
        continue

    for char in image_predictions[image]:
        current_text_file = os.path.splitext(image)[0] + '.txt'
        if char['label'] == 'mobian' and char['score'] > 0.5:
            with open(os.path.splitext(image)[0] + '.txt', "a") as outfile:
                outfile.write(f" {char['label']},")
                print(f"wrote to file: {image}")
        elif char['score'] > 0.7:
            with open(os.path.splitext(image)[0] + '.txt', "a") as outfile:
                outfile.write(f" {char['label']},")
                print(f"wrote to file: {image}")

    # Write to tag file
    '''
    with open(current_text_file, 'w', encoding="utf8") as file:
        tag_string = file.read()
        tag_string = tag_string[:-1]
        file.write(tag_string)

    '''
    

#preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
#print(preds)