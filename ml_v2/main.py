from trainer import Trainer
from utils import init_logger, set_seed
from data_loader import load_data
from transformers import BertTokenizer


class model_parameter:
  def __init__(self):
    self.task = 'museum'
    self.model_dir = 'trained_model'
    self.data_dir = "./data"
    self.intent_label_file = "intent_label.txt"
    self.slot_label_file = "slot_label.txt"
    self.model_type = "bert"
    self.train_batch_size = 32
    self.eval_batch_size = 64
    self.max_seq_len = 50
    self.learning_rate = 5e-5
    self.num_train_epochs = 20.0
    self.weight_decay = 0.0
    self.gradient_accumulation_steps = 1
    self.adam_epsilon = 1e-8
    self.max_grad_norm = 1.0
    self.max_steps = -1
    self.warmup_steps = 0
    self.dropout_rate = 0.1
    self.logging_steps = 20
    self.save_steps = 20
    self.ignore_index = 0
    self.slot_loss_coef = 1.0
    self.model_name_or_path = 'bert-base-uncased'
    self.batch_size = 32
    self.intents = ['UNK', 'greeting', 'ask_name', 'introduce_item', 'change_language', 'navigation', 'retreat']
    self.slots = ['PAD', 'UNK', 'O', 'B-language', 'I-language', 'B-location', 'I-location']



def main(parameter):
    init_logger()
    set_seed()
    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    train_dataset = load_data(parameter, tokenizer, mode="train")
    dev_dataset = load_data(parameter, tokenizer, mode="dev")
    test_dataset = load_data(parameter, tokenizer, mode="test")
    trainer = Trainer(parameter, train_dataset, dev_dataset, test_dataset)

    trainer.train()
    print('finished training, running test set')
    trainer.load_model()
    trainer.evaluate("test")


if __name__ == '__main__':
  parameter = model_parameter()
  main(parameter)
