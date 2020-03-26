#!/usr/bin/python3
# -*- encoding:utf-8 -*-

from collections import defaultdict
from functools import reduce
import sys
import pickle

DICT = 'dict.pkl'
INPUT = 'input.txt'
OUTPUT = 'output.txt'
MODE = 'ENCODE'
VER = '0.0.1'
DELIMITERS = ('', ';', "'", '4', '5', '6', '7', '8', '9', '0')

class identitydict(dict):
    def __missing__(self, key):
        return key

def init(dict_file: str) -> tuple:
    typing_dict = defaultdict(lambda:[])
    encoding_dict = identitydict()
    decoding_dict = identitydict()
    with open(dict_file, encoding='utf-8') as f:
        for line in f.readlines():
            data = line.rstrip().split('\t')
            if data[2] != '0':
                typing_dict[data[1]].append((int(data[2]), data[0]))
# print(list(filter(lambda x: x[1]>9, map(lambda x: (x[0],len(x[1])), typing_dict.items()))))
    for k, v in typing_dict.items():
        candidates = sorted(v, reverse=True)
        for d, c in zip(DELIMITERS, candidates):
            encoding_dict.setdefault(c[1], k+d)
            decoding_dict[k+d] = c[1]
    return encoding_dict, decoding_dict

def print_help():
    print('WBENC v{}:'.format(VER))
    print('SYNOPSIS')
    print(
    '''\twbenc\
    [-i input_file (default: input.txt)]\
    [-o output_file (default: output.txt)]\
    [-d dict_file (pickle format, default: dict.pkl)])\
    [OPTIONS]''')
    print('OPTIONS')
    print('\t-D: decode input_file into output_file using dict_file.')
    print('\t-E: encode input_file into output_file using dict_file.')
    print('\t-G: generate pickle-format dict_file with raw_dict-format input_file')
    print('\t\traw_dict: a UTF-8 text file where each line follows the format below.')
    print('\t\t\tWORD:str \\t ENCODE_INTO:str \\t FREQUENCY:num')

def set_input(it: iter):
    global INPUT
    INPUT = next(it)

def set_output(it: iter):
    global OUTPUT
    OUTPUT = next(it)

def set_dict(it: iter):
    global DICT
    DICT = next(it)

def set_decode_mode(it: iter):
    global MODE
    MODE = 'DECODE'

def set_encode_mode(it: iter):
    global MODE
    MODE = 'ENCODE'

def set_generate_dict_mode(it: iter):
    global MODE
    MODE = 'GENERATE'

def main():
    if len(sys.argv) == 1:
        print_help()
        return
    argi = iter(sys.argv)
    next(argi)
    arg_list = {
            '-i': set_input,
            '-o': set_output,
            '-d': set_dict,
            '-D': set_decode_mode,
            '-E': set_encode_mode,
            '-G': set_generate_dict_mode,
            }
    while True:
        try:
            arg = next(argi)
        except StopIteration:
            break
        if arg in arg_list:
            try:
                arg_list[arg](argi)
            except StopIteration:
                print_help()
                return

    if MODE == 'GENERATE':
        my_dict = init(INPUT)
        with open(DICT, 'wb') as f:
            pickle.dump(my_dict, f)
    elif MODE == 'ENCODE':
        with open(DICT, 'rb') as f:
            encoding_dict, _= pickle.load(f)

        with open(INPUT, encoding='utf-8') as f:
            raw = f.read()

        def sqeeze(a, x):
            w = encoding_dict[x]
            if not a:
                return [w]
            if w[0].isalnum() and a[-1].isalpha() and len(a[-1]) < 4:
                a[-1] += ' '
            a.append(w)
            return a

        out = ''.join(reduce(sqeeze, raw, None))

        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write(out)
    elif MODE == 'DECODE':
        with open(DICT, 'rb') as f:
            _, decoding_dict = pickle.load(f)

        with open(INPUT, encoding='utf-8') as f:
            raw = f.read()

        rawi = iter(raw)
        word = ''
        out = []
        ll = set(map(chr, range(97, 123)))
        for ch in rawi:
            if ch in ll:
                if len(word) < 4:
                    word += ch
                elif len(word) == 4:
                    out.append(decoding_dict[word])
                    word = ch
            elif ch == ' ':
                if word == '':
                    out.append(' ')
                else:
                    out.append(decoding_dict[word])
                    word = ''
            elif ch in DELIMITERS:
                word += ch
                out.append(decoding_dict[word])
                word = ''
            else:
                out.append(decoding_dict[word])
                word = ch
                out.append(decoding_dict[word])
                word = ''

        out = ''.join(out)

        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write(out)

if __name__ == '__main__':
    main()
