from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import nltk
import numpy as np
import pickle
import random
from tensorflow.python.platform import gfile
from data_utils import basic_tokenizer
import tensorflow as tf
from half2full import convert, HF_ASCII

padToken, goToken, eosToken, unknownToken = 0, 1, 2, 3

class Batch:
    #batch类，里面包含了encoder输入，decoder输入，decoder标签，decoder样本长度mask
    def __init__(self):
        self.encoder_inputs = []
        self.encoder_inputs_length = []
        self.decoder_targets = []
        self.decoder_targets_length = []

def loadDataset(data_path):
    '''
    读取样本数据
    :param filename: 文件路径
    :return: word2id, trainingSamples
    '''
    input_file = os.path.join(data_path, 'input.txt.ids50000.en')
    output_file = os.path.join(data_path, 'output.txt.ids50000.fr')
    #vocabulary_file = os.path.join(data_path, 'input.vocab50000.en')
    vocabulary_file = os.path.join(data_path, 'output.vocab50000.fr')
    if gfile.Exists(vocabulary_file):
        rev_vocab = []
        with gfile.GFile(vocabulary_file, mode="r") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [line.strip() for line in rev_vocab]
        # rev_vocab = [str(line.strip(), encoding='UTF-8') for line in rev_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_file)

    if gfile.Exists(input_file) and gfile.Exists(output_file):
        inputs = []
        with gfile.GFile(input_file, mode="rb") as f:
            inputs.extend(f.readlines())
        inputs_int_list = [list(map(int, line.split())) for line in inputs]
        outputs = []
        with gfile.GFile(output_file, mode="rb") as f:
            outputs.extend(f.readlines())
        outputs_int_list = [list(map(int, line.split())) for line in outputs]
        inputs_outputs = list(map(list, zip(inputs_int_list, outputs_int_list)))
    else:
        raise ValueError("Vocabulary file %s or %s not found.", (input_file, output_file))
    return vocab, inputs_outputs

def loadDataset_id_word(data_path):
    '''
    读取样本数据
    :param filename: 文件路径
    :return: word2id, id2word
    '''
    vocabulary_file = os.path.join(data_path, 'output.vocab50000.fr')
    if gfile.Exists(vocabulary_file):
        rev_vocab = []
        with gfile.GFile(vocabulary_file, mode="rb") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [line.strip() for line in rev_vocab]
        # rev_vocab = [str(line.strip(), encoding='UTF-8') for line in rev_vocab]
        word2id = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        id2word = dict([(y, x) for (y, x) in enumerate(rev_vocab)])
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_file)

    return word2id, id2word

def createBatch(samples):
    '''
    根据给出的samples（就是一个batch的数据），进行padding并构造成placeholder所需要的数据形式
    :param samples: 一个batch的样本数据，列表，每个元素都是[question， answer]的形式，id
    :return: 处理完之后可以直接传入feed_dict的数据格式
    '''
    batch = Batch()
    batch.encoder_inputs_length = [len(sample[0]) for sample in samples]
    batch.decoder_targets_length = [len(sample[1]) for sample in samples]
    max_source_length = max(batch.encoder_inputs_length)
    max_target_length = max(batch.decoder_targets_length)

    for sample in samples:
        #将source进行反序并PAD值本batch的最大长度
        source = list(reversed(sample[0]))
        # source = sample[0]
        pad = [padToken] * (max_source_length - len(source))
        batch.encoder_inputs.append(pad + source)

        #将target进行PAD，并添加END符号
        target = sample[1]
        pad = [padToken] * (max_target_length - len(target))
        # target = sample[1] + [eosToken]
        # pad = [padToken] * (max_target_length - len(target) + 1)
        batch.decoder_targets.append(target + pad)
        #batch.target_inputs.append([goToken] + target + pad[:-1])

    return batch

def getBatches(data, batch_size):
    '''
    根据读取出来的所有数据和batch_size将原始数据分成不同的小batch。对每个batch索引的样本调用createBatch函数进行处理
    :param data: loadDataset函数读取之后的trainingSamples，就是QA对的列表
    :param batch_size: batch大小
    :param en_de_seq_len: 列表，第一个元素表示source端序列的最大长度，第二个元素表示target端序列的最大长度
    :return: 列表，每个元素都是一个batch的样本数据，可直接传入feed_dict进行训练
    '''
    #每个epoch之前都要进行样本的shuffle
    random.shuffle(data)
    batches = []
    data_len = len(data)
    def genNextSamples():
        for i in range(0, data_len, batch_size):
            yield data[i:min(i + batch_size, data_len)]

    for samples in genNextSamples():
        batch = createBatch(samples)
        batches.append(batch)
    return batches

def sentence2enco(sentence, word2id):
    '''
    测试的时候将用户输入的句子转化为可以直接feed进模型的数据，现将句子转化成id，然后调用createBatch处理
    :param sentence: 用户输入的句子
    :param word2id: 单词与id之间的对应关系字典
    :return: 处理之后的数据，可直接feed进模型进行预测
    '''
    if sentence == '':
        return None
    #分词
    # tokens = nltk.word_tokenize(sentence)
    sentence_byte = tf.compat.as_bytes(sentence)
    tokens = basic_tokenizer(sentence_byte)
    if len(tokens) > 20:
        return None
    #将每个单词转化为id
    wordIds = []
    tokens = list(map(lambda vocab: convert(str(vocab, encoding="utf-8"), HF_ASCII), tokens))
    tokens_bytes = list(map(lambda vocab: bytes(vocab, encoding="utf-8"), tokens))
    for token in tokens_bytes:
        wordIds.append(word2id.get(token, unknownToken))
    #调用createBatch构造batch
    batch = createBatch([[wordIds, []]])
    return batch

# def check_data(data_path):
#     input_file = os.path.join(data_path, 'input.txt.ids50000.en')
#     output_file = os.path.join(data_path, 'output.txt.ids50000.fr')
#     vocabulary_output_file = os.path.join(data_path, 'output.vocab50000.fr')
#     vocabulary_input_file = os.path.join(data_path, 'input.vocab50000.en')
#
#     files = [input_file, output_file, vocabulary_output_file, vocabulary_input_file]
#     for file in files:
#         if gfile.Exists(file):
#             lines = []
#             with gfile.GFile(file, mode="r") as f:
#                 lines.extend(f.readlines())
#             lines = [line.strip() for line in lines]
#             if lines.count('') > 0:
#                 none_index = lines.index('')
#                 print(f'{file} line {none_index} has None!!!')

def check_data(data_path):
    input_file = os.path.join(data_path, 'input.txt.ids50000.en')
    output_file = os.path.join(data_path, 'output.txt.ids50000.fr')
    vocabulary_file = os.path.join(data_path, 'output.vocab50000.fr')
    if gfile.Exists(vocabulary_file):
        rev_vocab = []
        with gfile.GFile(vocabulary_file, mode="r") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [line.strip() for line in rev_vocab]
        if '' in rev_vocab:
            none_index = rev_vocab.index('')
            print(f'{none_index}rev_vocab has None!!!')
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_file)

    if gfile.Exists(input_file) and gfile.Exists(output_file):
        inputs = []
        with gfile.GFile(input_file, mode="r") as f:
            inputs.extend(f.readlines())
        inputs_int_list = [list(map(int, line.split())) for line in inputs]
        for i, int_in_list in enumerate(inputs_int_list):
            if len(int_in_list) == 0:
                print(f'inputs_int_list index:{i} is None!!!')
            elif len(int_in_list) == 1:
                if int_in_list[0] == '':
                    print(f'inputs_int_list index:{i} has None value!!!')
        outputs = []
        with gfile.GFile(output_file, mode="r") as f:
            outputs.extend(f.readlines())
        outputs_int_list = [list(map(int, line.split())) for line in outputs]
        for i, int_out_list in enumerate(outputs_int_list):
            if len(int_out_list) == 0:
                print(f'outputs_int_list index:{i} is None!!!')
            elif len(int_out_list) == 1:
                if int_out_list[0] == '':
                    print(f'outputs_int_list index:{i} has None value!!!')
    else:
        raise ValueError("Vocabulary file %s or %s not found.", (input_file, output_file))

if __name__ == '__main__':
    check_data('data')
