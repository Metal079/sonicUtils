from datasets import load_dataset, ClassLabel, Value, Image, Features, load_metric
import evaluate
from transformers import AutoImageProcessor, pipeline, DefaultDataCollator
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor, RandomHorizontalFlip, GaussianBlur, RandomSolarize, RandomApply

from transformers import TrainingArguments, Trainer, AutoImageProcessor, AutoModelForImageClassification
import torch

import numpy as np
from huggingface_hub import login

import warnings

print(torch.cuda.get_arch_list())

def collate_fn(batch):
    
    finalLabels = []
    for labels in batch:
        finalLabels.append(torch.tensor(labels['label']).float())
    finalLabels = finalLabels
    

    return {
        'pixel_values': torch.stack([x['pixel_values'] for x in batch]),
        'labels': torch.stack([x for x in finalLabels])
    }

_transforms = Compose([RandomHorizontalFlip(0.5)])

def transform(example_batch):
    inputs = feature_extractor([_transforms(x.convert('RGB')) for x in example_batch['image']], return_tensors='pt')

    # Don't forget to include the labels!
    inputs['label'] = example_batch['label']
    return inputs

train =load_dataset(path=r'/home/pablo/Documents/gallery-dl/aesthetic/goodbad', split="train", keep_in_memory=True)
train = train.cast_column('image', Image(decode=True))
train = train.shuffle(seed=123)
test = train.shuffle(seed=42).select(range(int(train.num_rows * .8), train.num_rows))
train = train.shuffle(seed=42).select(range(int(train.num_rows * .8)))

train.features['labels'] = ClassLabel(num_classes=2, names=['bad', 'good'])
test.features['labels'] = ClassLabel(num_classes=2, names=['bad', 'good'])

#model_name_or_path = 'facebook/convnext-xlarge-384-22k-1k'
#model_name_or_path = 'facebook/convnext-base-384-22k-1k'
#model_name_or_path = 'facebook/deit-base-distilled-patch16-384'
model_name_or_path = 'facebook/convnextv2-large-22k-384'
#model_name_or_path = 'facebook/convnextv2-base-22k-384'
feature_extractor = AutoImageProcessor.from_pretrained(model_name_or_path)

prepared_ds_test = test.with_transform(transform)
prepared_ds_train = train.with_transform(transform)

stats = []
metric = evaluate.combine(["accuracy","precision", "recall"])
def compute_metrics(p):
    warnings.filterwarnings('ignore')
    return metric.compute(predictions=np.argmax(p.predictions, axis=1), references=p.label_ids)

labels = test.features['label'].names

model = AutoModelForImageClassification.from_pretrained(
    model_name_or_path,
    num_labels=len(labels),
    id2label={str(i): c for i, c in enumerate(labels)},
    label2id={c: str(i) for i, c in enumerate(labels)},
    #problem_type="binary_classification",
    ignore_mismatched_sizes=True
)

training_args = TrainingArguments(
  output_dir="./SonicAestheticClassifier",
  per_device_train_batch_size =10,
  #auto_find_batch_size=True,
  evaluation_strategy="epoch",
  num_train_epochs=10,
  #fp16=True,
  save_steps=1,
  save_strategy="epoch",
  eval_steps=1,
  logging_steps=100,
  learning_rate=2.5e-6,
  save_total_limit=10,
  remove_unused_columns=False,
  push_to_hub=False,
  report_to='tensorboard',
  load_best_model_at_end=True,
  metric_for_best_model="accuracy",
  #torch_compile = True,
  #include_inputs_for_metrics=True,
  #optim='lion',
  lr_scheduler_type='cosine',
  #resume_from_checkpoint=""
  weight_decay=1e-8
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=DefaultDataCollator(),
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


