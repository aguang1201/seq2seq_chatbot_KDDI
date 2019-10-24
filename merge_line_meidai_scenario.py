import os
import glob


train = []
val = []
root_dir = '/home/ys1/dataset/KDDI_chatbot/line_meidai_scenario'
file_name_line = 'line20141031_split.jpn.txt'
file_name_meidai = 'meidai_sequence_split.txt'
file_name_input_scenario = 'input_scenario.txt'
file_name_output_scenario = 'output_scenario.txt'
file_path_line = os.path.join(root_dir, file_name_line)
file_path_meidai = os.path.join(root_dir, file_name_meidai)
files_path_list = [file_path_line, file_path_meidai]
input_file_name_all = os.path.join(root_dir, 'input.txt')
output_file_name_all = os.path.join(root_dir, 'output.txt')

file_train_input = os.path.join(root_dir, 'train.ask')
file_train_output = os.path.join(root_dir, 'train.ans')
file_val_input = os.path.join(root_dir, 'val.ask')
file_val_output = os.path.join(root_dir, 'val.ans')
file_test_input = os.path.join(root_dir, 'test.ask')
file_test_output = os.path.join(root_dir, 'test.ans')
tab = '\t'
train_radio = 0.8
delete_words_list = ['そう な ん', 'そう なん', 'そう です', 'そうです']
lenth_threshold = 15

def check_line(input_output):
    for text in input_output:
        if len(text) < lenth_threshold:
            for delete_word in delete_words_list:
                if delete_word in text:
                    print(f'delete:{text}')
                    return False
    return True

def split_file():
    for file_path in files_path_list:
        input = []
        output = []
        file_name = os.path.basename(file_path)[:4]
        file = open(file_path, 'r')
        for line in file.readlines():
            if not tab in line:
                print(f'line: {line}')
            else:
                input_output = line.split(tab)
                if check_line(input_output):
                    input.append(input_output[0] + '\n')
                    output.append(input_output[1])
        input_file_name = f'input_{file_name}.txt'
        input_file = open(os.path.join(root_dir, input_file_name), 'w')
        for i in input:
            input_file.write(i)
        output_file_name = f'output_{file_name}.txt'
        output_file = open(os.path.join(root_dir, output_file_name), 'w')
        for i in output:
            output_file.write(i)
        file.close()
        input_file.close()
        output_file.close()


def merge_files():
    file_name_list = ['meid', 'line', 'scenario']
    file_input_list = [os.path.join(root_dir, f'input_{name}.txt') for name in file_name_list]
    file_output_list = [os.path.join(root_dir, f'output_{name}.txt') for name in file_name_list]
    for file_input in file_input_list:
        file = open(file_input, 'r')
        input = file.readlines()
        len_all = len(input)
        len_train = int(len_all * train_radio)
        with open(file_train_input, 'a') as train_input:
            train_input.writelines(input[:len_train])
        with open(file_val_input, 'a') as val_input:
            val_input.writelines(input[len_train:])

    for file_output in file_output_list:
        file = open(file_output, 'r')
        output = file.readlines()
        len_all = len(output)
        len_train = int(len_all * train_radio)
        with open(file_train_output, 'a') as train_output:
            train_output.writelines(output[:len_train])
        with open(file_val_output, 'a') as val_output:
            val_output.writelines(output[len_train:])

if __name__ == '__main__':
    # split_file()
    merge_files()