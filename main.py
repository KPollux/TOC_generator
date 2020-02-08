CONTENT_FILE = "content.txt"
RESULT_FILE = "result.txt"
REPLACE_STR = "~!@#$%^&*()+`-={[}]|\\:;"'<,>? '
ERASE_STR = "./，"


# 找到最右边的一个字符，没有则返回-1
def findr(in_str, char):
    index = -1
    temp_index = 0
    while True:
        temp_index = in_str[temp_index:].find(char)
        if temp_index == -1:
            break
        else:
            index = temp_index
            temp_index += 1

    return index


def count_sharp(in_str):
    # 找最右手边的一个#
    i = len(in_str)
    while i > 0:
        last_index = in_str[0: i].rindex('#')
        i = last_index
        # 判断它之前是否全是#
        while i > 0:
            if in_str[i - 1] == '#':  # 看这个#前面还是#时，i前移，到i=0循环完全终止
                i -= 1
            else:  # 当#前发现了其他字符，则说明标题中含有#，从这个位置开始重新判断#位置
                break  # 若前一个字符不是#，跳转到外层循环，重新分析前半段子串
    # 如果循环正常结束，则说明标题中不含#，所有#连续，last_index标注了最后一个#的位置
    return last_index


def deal_str(in_str):
    if in_str[0] != '#':
        print("传入值错误，字符串开头必须为'#'")
        return -1
    # 数一下有几个#号，则为第几级标题
    last_index = count_sharp(in_str)

    _ = ''
    for i in range(last_index):
        _ += '  '
    _ += "- ["
    head_str = _

    # TODO() 文字部分删除超链接
    body_str = in_str[last_index + 2:-1]

    b_ri = findr(body_str, ']')
    if b_ri > 0:
        body_str = body_str[0:b_ri]
    # print(b_ri)
    body_str = body_str.replace('[', '')
    # print(body_str)

    # 后半部分转换完毕
    body_str2 = "](#"
    for _ in body_str:
        if REPLACE_STR.find(_) >= 0:
            _ = '-'
        elif ERASE_STR.find(_) >= 0:
            _ = ''
        elif _.isalpha():
            _ = _.lower()
        body_str2 += _

    tail_str = ")\n"

    out_str = f'{head_str}{body_str}{body_str2}{tail_str}'

    return out_str


def main():
    in_str = []
    temp_str = []
    out_str = []

    # 读入文件
    with open(CONTENT_FILE, 'r', encoding='UTF-8', errors='ignore') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            in_str.append(lines)
            # print(lines, end='')
            if not lines:
                break

    # 去掉开头不带#的内容行
    for s in in_str:
        if s and s[0] == '#':
            temp_str.append(s)

    # 按句处理，并加入到输出字符串里准备输出
    for _ in temp_str:
        out_str.append(deal_str(_))
    # print(out_str)

    # 输出到文件
    with open(RESULT_FILE, 'w') as file_to_write:
        for _ in out_str:
            file_to_write.write(_)


if __name__ == "__main__":
    main()
'''
.消失，全变小写，符号变-
# Paste Your Document In Here
## And a table of contents
### On the right

- [Paste Your Document In Here](#paste-your-document-in-here)
  * [And a table of contents](#and-a-table-of-contents)
    + [On the right](#on-the-right)
'''
