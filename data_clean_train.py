import os
from multiprocessing import Pool
from tqdm import tqdm

root_dir_nmt = 'data'
delete_words_list = ['そう な ん', 'そう なん', 'そう です', 'そうです']

def write_file(file):
    delete_index_list_copy = delete_index_list.copy()
    if os.path.splitext(file)[-1] == '.ans':
        lines_list = lines_ans_list
    elif os.path.splitext(file)[-1] == '.ask':
        lines_list = lines_ask_list
    print(f'开始生成文件')
    with open(file, 'w') as cleaned_file:
        for index, line in enumerate(tqdm(lines_list)):
            if index not in delete_index_list_copy:
                cleaned_file.write(line)
            elif index == delete_index_list_copy[0]:
                del delete_index_list_copy[0]
    print(f'{file}文件生成完毕')

if __name__ == '__main__':
    file_mode_list = ['train', 'val']
    # file_mode_list = ['val']
    for file_mode in file_mode_list:
        delete_index_list = []
        line_num_ask = -1
        line_num_ans = -1
        file_ask = os.path.join(root_dir_nmt, file_mode + '.ask')
        file_ans = os.path.join(root_dir_nmt, file_mode + '.ans')
        file_deleted_ask = os.path.join(root_dir_nmt, file_mode + '_cleaned' + '.ask')
        file_deleted_ans = os.path.join(root_dir_nmt, file_mode + '_cleaned' + '.ans')
        with open(file_ask, 'r') as ask:
            lines_ask_list = ask.readlines()
            print(f'{file_ask}句子总数为:{len(lines_ask_list)}')
            for line in lines_ask_list:
                line_num_ask = line_num_ask + 1
                if len(line) < 21:
                    for delete_word in delete_words_list:
                        if delete_word in line:
                            delete_index_list.append(line_num_ask)

        with open(file_ans, 'r') as ans:
            lines_ans_list = ans.readlines()
            print(f'{file_ans}句子总数为:{len(lines_ans_list)}')
            for line in lines_ans_list:
                line_num_ans = line_num_ans + 1
                # 参照"そう な ん です よ ね 〜 。\n"的长度为18
                if len(line) < 21:
                    for delete_word in delete_words_list:
                        if delete_word in line:
                            delete_index_list.append(line_num_ans)
        delete_index_list = sorted(list(set(delete_index_list)))
        print(f'{file_mode}含有{delete_words_list}的句子数为:{len(delete_index_list)}')
        p = Pool(2)
        file_list = [file_deleted_ask, file_deleted_ans]
        for file in file_list:
            p.apply_async(write_file, args=(file,))
            # clean_data(file_mode)
        p.close()
        p.join()