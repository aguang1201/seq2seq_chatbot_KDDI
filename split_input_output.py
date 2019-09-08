input = []
output = []
input_output_file_name = '/home/panotech/sharewithZhouLaoShi/20181101_learningdata/meidai_dataset/meidai_sequence_split.txt'
input_file_name = '/home/panotech/sharewithZhouLaoShi/20181101_learningdata/meidai_dataset/meidai_input.txt'
output_file_name = '/home/panotech/sharewithZhouLaoShi/20181101_learningdata/meidai_dataset/meidai_output.txt'
input_output_file = open(input_output_file_name, 'r')
tab = '\t'
def split_file():
    for i, line in enumerate(input_output_file.readlines()):
        if not tab in line:
            print(f'{i} line: {line}')
        else:
            input_output = line.split(tab)
            input.append(input_output[0])
            output.append(input_output[1])
    input_file = open(input_file_name, 'a')
    for i in input:
        input_file.write(i + "\n")
    output_file = open(output_file_name, 'a')
    for i in output:
        output_file.write(i)
    input_output_file.close()
    input_file.close()
    output_file.close()

def append_file(file_src,file_dst):
    file_src = open(file_src, 'r')
    file_dst = open(file_dst, 'w')
    lblSrcFLines = file_src.readlines()
    # for line in lblSrcFLines:
    #     srcLine = line.strip().split()  # space split
    #     sline = srcLine[0].strip()
    #     froi = open(sline, 'r')
    #     roilines = froi.readlines()
    #     for rline in roilines:
    #         file_dst.write(rline)
    #     froi.close()

    file_dst.close()
    file_src.close()

if __name__ == '__main__':
    split_file()