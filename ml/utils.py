import os
import random
import logging
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
import torch
import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score

from transformers import BertConfig
from transformers import BertTokenizer

from model import JointBERT

MODEL_CLASSES = {
    'bert': (BertConfig, JointBERT, BertTokenizer),
}

MODEL_PATH_MAP = {
    'bert': 'bert-base-uncased',
}

def convert_input_file_to_tensor_dataset(words,pred_config,args,pad_token_label_id):
    # Setting based on the current model type
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    pad_token_id = tokenizer.pad_token_id

    #for words in lines:
    tokens = []
    slot_label_mask = []
    for word in words:
        word_tokens = tokenizer.tokenize(word)
        if not word_tokens:
            word_tokens = [tokenizer.unk_token]  # For handling the bad-encoded word
        tokens.extend(word_tokens)
        # Use the real label id for the first token of the word, and padding ids for the remaining tokens
        slot_label_mask.extend([pad_token_label_id + 1] + [pad_token_label_id] * (len(word_tokens) - 1))

    # Account for [CLS] and [SEP]
    special_tokens_count = 2
    if len(tokens) > args.max_seq_len - special_tokens_count:
        tokens = tokens[: (args.max_seq_len - special_tokens_count)]
        slot_label_mask = slot_label_mask[:(args.max_seq_len - special_tokens_count)]

    # Add [SEP] token
    tokens += [tokenizer.sep_token]
    token_type_ids = [0] * len(tokens)
    slot_label_mask += [pad_token_label_id]
    # Add [CLS] token
    tokens = [tokenizer.cls_token] + tokens
    token_type_ids = [0] + token_type_ids
    slot_label_mask = [pad_token_label_id] + slot_label_mask
    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    # The mask has 1 for real tokens and 0 for padding tokens. Only real tokens are attended to.
    attention_mask = [1] * len(input_ids)

    # Zero-pad up to the sequence length.
    padding_length = args.max_seq_len - len(input_ids)
    input_ids = input_ids + ([pad_token_id] * padding_length)
    attention_mask = attention_mask + ([0] * padding_length)
    token_type_ids = token_type_ids + ([0] * padding_length)
    slot_label_mask = slot_label_mask + ([pad_token_label_id] * padding_length)

    # Change to Tensor
    all_input_ids = torch.as_tensor([input_ids], dtype=torch.long)
    all_attention_mask = torch.as_tensor([attention_mask], dtype=torch.long)
    all_token_type_ids = torch.as_tensor([token_type_ids], dtype=torch.long)
    all_slot_label_mask = torch.as_tensor([slot_label_mask], dtype=torch.long)

    dataset = TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids, all_slot_label_mask)

    return dataset


def predict(command, pred_config):
    # load model and args
    args = torch.load('trained_model/training_args.bin')
    intent_label_lst = get_intent_labels(args)
    slot_label_lst = get_slot_labels(args) 
    model = JointBERT.from_pretrained("./trained_model",args=args,intent_label_lst=intent_label_lst,slot_label_lst=slot_label_lst)
    model.to("cpu")
    model.eval()

    # Convert input command to TensorDataset
    pad_token_label_id = args.ignore_index
    
    words = command.strip().split()
    dataset = convert_input_file_to_tensor_dataset(words, pred_config, args, pad_token_label_id)

    # Predict
    sampler = SequentialSampler(dataset)
    data_loader = DataLoader(dataset, sampler=sampler, batch_size=pred_config.batch_size)
    batch = next(iter(data_loader))
    batch = tuple(t.to("cpu") for t in batch)
    with torch.no_grad():
        inputs = {"input_ids": batch[0],"attention_mask": batch[1],"intent_label_ids": None,"slot_labels_ids": None}
        inputs["token_type_ids"] = batch[2]
        outputs = model(**inputs)
        _, (intent_logits, slot_logits) = outputs[:2]

        # Intent Prediction
        intent_pred = intent_logits.detach().cpu().numpy()
        # Slot prediction
        slot_preds = slot_logits.detach().cpu().numpy()
        all_slot_label_mask = batch[3].detach().cpu().numpy()

    intent_pred = int(np.argmax(intent_pred, axis=1))
    slot_preds = (np.argmax(slot_preds, axis=2))[0]
    slot_label_dict = {i: label for i, label in enumerate(slot_label_lst)}
    slot_preds_list = []

    for i in range(len(slot_preds)):
        if all_slot_label_mask[0, i] != pad_token_label_id:
            slot_preds_list.append(slot_label_dict[slot_preds[i]])
            
    keywords = []
    for word, slot in zip(words, slot_preds_list):
        if slot != 'O':
            keywords.append(word)
    return (keywords, intent_label_lst[intent_pred])


def get_intent_labels(args):
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.intent_label_file), 'r', encoding='utf-8')]


def get_slot_labels(args):
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.slot_label_file), 'r', encoding='utf-8')]


def load_tokenizer(args):
    return MODEL_CLASSES[args.model_type][2].from_pretrained(args.model_name_or_path)


def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def set_seed():
    random.seed(10)
    np.random.seed(10)
    torch.manual_seed(10)


def compute_metrics(intent_preds, intent_labels, slot_preds, slot_labels):
    assert len(intent_preds) == len(intent_labels) == len(slot_preds) == len(slot_labels)
    results = {}
    intent_result = get_intent_acc(intent_preds, intent_labels)
    slot_result = get_slot_metrics(slot_preds, slot_labels)
    sementic_result = get_sentence_frame_acc(intent_preds, intent_labels, slot_preds, slot_labels)

    results.update(intent_result)
    results.update(slot_result)
    results.update(sementic_result)

    return results


def get_slot_metrics(preds, labels):
    assert len(preds) == len(labels)
    return {
        "slot_precision": precision_score(labels, preds),
        "slot_recall": recall_score(labels, preds),
        "slot_f1": f1_score(labels, preds)
    }


def get_intent_acc(preds, labels):
    acc = (preds == labels).mean()
    return {
        "intent_acc": acc
    }


def read_prediction_text(args):
    return [text.strip() for text in open(os.path.join(args.pred_dir, args.pred_input_file), 'r', encoding='utf-8')]


def get_sentence_frame_acc(intent_preds, intent_labels, slot_preds, slot_labels):
    """For the cases that intent and all the slots are correct (in one sentence)"""
    # Get the intent comparison result
    intent_result = (intent_preds == intent_labels)

    # Get the slot comparision result
    slot_result = []
    for preds, labels in zip(slot_preds, slot_labels):
        assert len(preds) == len(labels)
        one_sent_result = True
        for p, l in zip(preds, labels):
            if p != l:
                one_sent_result = False
                break
        slot_result.append(one_sent_result)
    slot_result = np.array(slot_result)

    sementic_acc = np.multiply(intent_result, slot_result).mean()
    return {
        "sementic_frame_acc": sementic_acc
    }
