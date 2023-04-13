from datasets import load_dataset, ClassLabel, Value, Image, Features, load_metric
import evaluate
from transformers import AutoImageProcessor, DefaultDataCollator
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor, RandomHorizontalFlip

from transformers import TrainingArguments, Trainer, ConvNextForImageClassification, BeitFeatureExtractor, BeitForImageClassification, ConvNextConfig, ConvNextModel, ConvNextImageProcessor
import torch

import numpy as np
from huggingface_hub import login

import warnings

login("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")

def collate_fn(batch):
    
    finalLabels = []
    for labels in batch:
        finalLabels.append(torch.tensor(labels['labels']).float())
    finalLabels = finalLabels
    

    return {
        'pixel_values': torch.stack([x['pixel_values'] for x in batch]),
        'labels': torch.stack([x for x in finalLabels])
    }

_transforms = Compose([RandomHorizontalFlip(0.5)])

def transform(example_batch):
    # Take a list of PIL images and turn them to pixel values
    #for image in example_batch['image']:
        #if example_batch['image'][0].format == 'PNG' or example_batch['image'][0] == 'L':
            #example_batch['image'][0] = example_batch['image'][0].convert('RGB')
    inputs = feature_extractor([_transforms(x.convert('RGB')) for x in example_batch['image']], return_tensors='pt')

    # Don't forget to include the labels!
    inputs['labels'] = example_batch['labels']
    return inputs

train =load_dataset('json', data_files=r'/media/pablo/6ED0B21ED0B1EC89/Users/metal/Downloads/sonic_training/deviantart/Tags_labeled_archive/train.json', split="train")
train = train.cast_column('image', Image(decode=True))
train = train.shuffle(seed=123)
test = train.shuffle(seed=42).select(range(int(train.num_rows * .8), train.num_rows))
train = train.shuffle(seed=42).select(range(int(train.num_rows * .8)))

train.features['labels'] = ClassLabel(num_classes=36, names=["Tails the fox",
                                                            "Amy Rose",
                                                            "Knuckles the echidna",
                                                            "Whisper the wolf",
                                                            "Rogue the bat",
                                                            "Silver the hedgehog",
                                                            "Blaze the cat",
                                                            "Vanilla the rabbit",
                                                            "Cream the rabbit",
                                                            "Shadow the hedgehog",
                                                            "Sonic the hedgehog",
                                                            "Sally Acorn",
                                                            "Tangle the lemur",
                                                            "mobian",
                                                            "Cosmo the seedrian",
                                                            "Big the cat",
                                                            "Sticks the badger",
                                                            "Tikal the echidna",
                                                            "Wave the swallow",
                                                            "Jet the hawk",
                                                            "Honey the cat",
                                                            "Surge the tenrec",
                                                            "Starline the platypus",
                                                            "Mighty the armadillo",
                                                            "Vector the crocodile",
                                                            "Charmy the bee",
                                                            "Espio the chameleon",
                                                            "eggman",
                                                            "Bunnie Rabbot",
                                                            "Marine the Raccoon",
                                                            "Storm the albatross",
                                                            "Maria Robotnik",
                                                            "Nicole the Lynx",
                                                            "Lanolin the sheep",
                                                            "Metal Sonic",
                                                            "Shard the metal Sonic"])
test.features['labels'] = ClassLabel(num_classes=36, names=["Tails the fox",
                                                            "Amy Rose",
                                                            "Knuckles the echidna",
                                                            "Whisper the wolf",
                                                            "Rogue the bat",
                                                            "Silver the hedgehog",
                                                            "Blaze the cat",
                                                            "Vanilla the rabbit",
                                                            "Cream the rabbit",
                                                            "Shadow the hedgehog",
                                                            "Sonic the hedgehog",
                                                            "Sally Acorn",
                                                            "Tangle the lemur",
                                                            "mobian",
                                                            "Cosmo the seedrian",
                                                            "Big the cat",
                                                            "Sticks the badger",
                                                            "Tikal the echidna",
                                                            "Wave the swallow",
                                                            "Jet the hawk",
                                                            "Honey the cat",
                                                            "Surge the tenrec",
                                                            "Starline the platypus",
                                                            "Mighty the armadillo",
                                                            "Vector the crocodile",
                                                            "Charmy the bee",
                                                            "Espio the chameleon",
                                                            "eggman",
                                                            "Bunnie Rabbot",
                                                            "Marine the Raccoon",
                                                            "Storm the albatross",
                                                            "Maria Robotnik",
                                                            "Nicole the Lynx",
                                                            "Lanolin the sheep",
                                                            "Metal Sonic",
                                                            "Shard the metal Sonic"])


model_name_or_path = 'facebook/convnext-xlarge-384-22k-1k'
feature_extractor = ConvNextImageProcessor.from_pretrained(model_name_or_path)

prepared_ds_test = test.with_transform(transform)
prepared_ds_train = train.with_transform(transform )

#metric = evaluate.load("accuracy")
stats = []
metric = evaluate.combine(["accuracy","precision", "recall"])
def compute_metrics(p):
    warnings.filterwarnings('ignore')
    accuracies = []
    for i, label in enumerate(p.label_ids):   
        prediction = []
        #for predict in p.predictions[i]:
        predict = torch.sigmoid(torch.tensor(p.predictions[i]).float())
        for pizza in predict:
            if pizza > 0.5:
                prediction.append(1.0)
            else:
                prediction.append(0.0)
        accuracies.append(metric.compute(references=label, predictions=prediction))
        
    accuracy = 0
    precision = 0
    recall = 0
    for number in accuracies:
        accuracy += number['accuracy']
        precision += number['precision']
        recall += number['recall']

    accuracy = accuracy / len(accuracies)
    precision =  precision / len(accuracies)
    recall = recall / len(accuracies)
    stats.append({'accuracy': accuracy, 'precision': precision, 'recall': recall})
    return {'accuracy': accuracy, 'precision': precision, 'recall': recall}

labels = test.features['labels'].names

model = ConvNextForImageClassification.from_pretrained(
    model_name_or_path,
    num_labels=len(labels),
    id2label={str(i): c for i, c in enumerate(labels)},
    label2id={c: str(i) for i, c in enumerate(labels)},
    problem_type="multi_label_classification",
    ignore_mismatched_sizes=True
)

training_args = TrainingArguments(
  output_dir="./SonicCharacterClassifier",
  per_device_train_batch_size =20,
  evaluation_strategy="epoch",
  num_train_epochs=10,
  fp16=True,
  save_steps=1,
  save_strategy="epoch",
  eval_steps=1,
  logging_steps=500,
  learning_rate=1e-4,
  save_total_limit=10,
  remove_unused_columns=False,
  push_to_hub=False,
  report_to='tensorboard',
  load_best_model_at_end=True,
  metric_for_best_model="precision",
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=collate_fn,
    compute_metrics=compute_metrics,
    train_dataset=prepared_ds_train,
    eval_dataset=prepared_ds_test,
    tokenizer=feature_extractor,
)

train_results = trainer.train()
trainer.save_model()
trainer.log_metrics("train", train_results.metrics)
trainer.save_metrics("train", train_results.metrics)
trainer.save_state()

metrics = trainer.evaluate(prepared_ds_test)
trainer.log_metrics("eval", metrics)
trainer.save_metrics("eval", metrics)

print(stats)

if training_args.push_to_hub:
    trainer.push_to_hub('🍻 cheers')
else:
    trainer.create_model_card()


