from main import model_parameter
import numpy as np
import torch

from utils import convert_input_file_to_tensor_dataset, init_logger, get_intent_labels, get_slot_labels, predict
from model import JointBERT
from transformers import BertTokenizer



if __name__ == "__main__":
    parameter = model_parameter()
    command = 'can you change your language to english'
    keywords, intent = predict(command, parameter)
    print(keywords)
    print(intent)
