
from datasets import load_dataset, ClassLabel, Value, Image, Features, load_metric

from transformers import (
    Blip2VisionConfig,
    Blip2QFormerConfig,
    OPTConfig,
    Blip2Config,
    Blip2ForConditionalGeneration,
    BlipImageProcessor,
    AutoFeatureExtractor,
    Blip2Processor,
    Trainer,
    TrainingArguments,
    DefaultDataCollator
)

train = load_dataset('json', data_files=r"C:\Users\metal\Documents\programming\sonic_image classifier\captions.json", split="train")


# Initializing a Blip2Config with Salesforce/blip2-opt-2.7b style configuration
configuration = Blip2Config()

model_name_or_path = 'Salesforce/blip2-opt-2.7b'
image_processor = BlipImageProcessor.from_pretrained(model_name_or_path)

# Initializing a Blip2ForConditionalGeneration (with random weights) from the Salesforce/blip2-opt-2.7b style configuration
#model = Blip2ForConditionalGeneration(configuration)

model = Blip2Processor.from_pretrained(
    model_name_or_path,
    #num_labels=len(labels),
    #id2label={str(i): c for i, c in enumerate(labels)},
    #label2id={c: str(i) for i, c in enumerate(labels)},
    #problem_type="binary_classification",
    #ignore_mismatched_sizes=True
)

# Accessing the model configuration
#configuration = model.config

# We can also initialize a Blip2Config from a Blip2VisionConfig, Blip2QFormerConfig and any PretrainedConfig

# Initializing BLIP-2 vision, BLIP-2 Q-Former and language model configurations
vision_config = Blip2VisionConfig()
qformer_config = Blip2QFormerConfig()
text_config = OPTConfig()


training_args = TrainingArguments(
  output_dir="./blip2",
  per_device_train_batch_size =10,
  evaluation_strategy="epoch",
  num_train_epochs=10,
  fp16=False,
  save_steps=1,
  save_strategy="epoch",
  eval_steps=1,
  logging_steps=100,
  learning_rate=1e-4,
  save_total_limit=10,
  remove_unused_columns=False,
  push_to_hub=False,
  report_to='tensorboard',
  load_best_model_at_end=True,
  metric_for_best_model="accuracy",
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=DefaultDataCollator(),
    compute_metrics=compute_metrics,
    train_dataset=prepared_ds_train,
    eval_dataset=prepared_ds_test,
    tokenizer=image_processor,
)