import MeCab
import os

mecab = MeCab.Tagger("-Owakati")
input = []
output = []
root_dir = '/home/ys1/dataset/20190828_TVシナリオ応答対'
input_output_file_name = os.path.join(root_dir, 'tv_scenario_corpus_all.txt')
input_file_name = os.path.join(root_dir, 'input_scenario.txt')
output_file_name = os.path.join(root_dir, 'output_scenario.txt')
input_output_file = open(input_output_file_name, 'r')

root_dir_nmt = '/home/ys1/dataset/KDDI_chatbot'
file_train_input = os.path.join(root_dir_nmt, 'train.ask')
file_train_output = os.path.join(root_dir_nmt, 'train.ans')
file_val_input = os.path.join(root_dir_nmt, 'val.ask')
file_val_output = os.path.join(root_dir_nmt, 'val.ans')
file_test_input = os.path.join(root_dir_nmt, 'test.ask')
file_test_output = os.path.join(root_dir_nmt, 'test.ans')

tab = '\t'
train_radio = 0.8
# val_radio = 0.2
# test_radio = 0.1
delete_words_list = ['そうなん', 'そうです']
lenth_threshold = 8

def check_line(input_output):
    for text in input_output:
        if len(text) < lenth_threshold:
            for delete_word in delete_words_list:
                if delete_word in text:
                    print(f'delete:{text}')
                    return False
    return True

def split_file():
    for line in input_output_file.readlines():
        if not tab in line:
            print(f'line: {line}')
        else:
            input_output = line.split(tab)
            if check_line(input_output):
                input.append(mecab.parse(input_output[0]))
                output.append(mecab.parse(input_output[1]))
    input_file = open(input_file_name, 'w')
    for i in input:
        input_file.write(i)
    output_file = open(output_file_name, 'w')
    for i in output:
        output_file.write(i)
    input_output_file.close()
    input_file.close()
    output_file.close()

    # len_all = len(input)
    # len_train = int(len_all * train_radio)

    # with open(file_train_input, 'a') as train_input:
    #     train_input.writelines(input[:len_train])
    # with open(file_train_output, 'a') as train_output:
    #     train_output.writelines(output[:len_train])
    #
    # with open(file_val_input, 'a') as val_input:
    #     val_input.writelines(input[len_train:])
    # with open(file_val_output, 'a') as val_output:
    #     val_output.writelines(output[len_train:])
    #
    # with open(file_test_input, 'a') as test_input:
    #     test_input.writelines(input[len_train:])
    # with open(file_test_output, 'a') as test_output:
    #     test_output.writelines(output[len_train:])


if __name__ == '__main__':
    split_file()