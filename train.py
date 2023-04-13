#train.py
from datasets import load_dataset, ClassLabel, Value, Image, Features
from transformers import AutoImageProcessor
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor

from transformers import ViTFeatureExtractor


# %%
from huggingface_hub import notebook_login

notebook_login()

# %%
# Load dataset
#food = load_dataset(path=r"C:\Users\metal\Downloads\test\labels\json")
#test = load_dataset('csv', data_files=r'C:\Users\metal\Downloads\test\labels\sheet1.csv', split="train")
food = load_dataset("food101", split="train[:5000]")
food = food.train_test_split(test_size=0.2)
#print(food["train"][0])
#test = test.cast_column('image', Image(decode=True))
#test.features['label'] = ClassLabel(num_classes=2, names=['amy', 'blaze'])
#print(test['image'])

# %%
#preprocess
image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
print(image_processor)

labels = food.features["label"].names
label2id, id2label = dict(), dict()
for i, label in enumerate(labels):
    label2id[label] = str(i)
    id2label[str(i)] = label

image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")

from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor

normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)
size = (
    image_processor.size["shortest_edge"]
    if "shortest_edge" in image_processor.size
    else (image_processor.size["height"], image_processor.size["width"])
)
_transforms = Compose([RandomResizedCrop(size), ToTensor(), normalize])

def transforms(examples):
    examples["pixel_values"] = [_transforms(img.convert("RGB")) for img in examples["image"]]
    del examples["image"]
    return examples


food = food.with_transform(transforms)

from transformers import DefaultDataCollator

data_collator = DefaultDataCollator()

# %%
import evaluate

accuracy = evaluate.load("accuracy")

import numpy as np


def compute_metrics(eval_pred):
    predictions = np.argmax(eval_pred.predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=eval_pred.label_ids)

# %%
from transformers import AutoModelForImageClassification, TrainingArguments, Trainer

model = AutoModelForImageClassification.from_pretrained(
    "google/vit-base-patch16-224-in21k",
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
    problem_type="multi_label_classification"
)

training_args = TrainingArguments(
    output_dir="test",
    remove_unused_columns=False,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=4,
    per_device_eval_batch_size=16,
    num_train_epochs=1,
    warmup_ratio=0.1,
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    push_to_hub=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=food['train'],
    eval_dataset=food['test'],
    tokenizer=image_processor,
    compute_metrics=compute_metrics,
)

# %%
trainer.train()


