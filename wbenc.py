#!/usr/bin/python3
# -*- encoding:utf-8 -*-

from collections import defaultdict
from functools import reduce
import argparse
import sys
import pickle

VER = '0.0.2'
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

def main():
    parser = argparse.ArgumentParser(description='Encode Chinese characters')
    parser.add_argument('-i', '--input', action='store', nargs=1,
            default=['input.txt'], help='specify the input filename')
    parser.add_argument('-o', '--output', action='store', nargs=1,
            default=['output.txt'], help='specify the output filename')
    parser.add_argument('-d', '--dict', action='store', nargs=1,
            default=['dict.pkl'], help='specify the dict file')
    parser.add_argument('-D', '--decode', action='store_const', const=True,
            help='use decode mode')
    parser.add_argument('-E', '--encode', action='store_const', const=True,
            help='use encode mode')
    parser.add_argument('-G', '--generate', action='store_const', const=True,
            help='use generate dict mode')
    args = parser.parse_args()

    input_file = args.input[0]
    output_file = args.output[0]
    dict_file = args.dict[0]

    if args.generate:
        my_dict = init(input_file)
        with open(dict_file, 'wb') as f:
            pickle.dump(my_dict, f)
    elif args.encode:
        with open(dict_file, 'rb') as f:
            encoding_dict, _= pickle.load(f)

        with open(input_file, encoding='utf-8') as f:
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

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(out)
    elif args.decode:
        with open(dict_file, 'rb') as f:
            _, decoding_dict = pickle.load(f)

        with open(input_file, encoding='utf-8') as f:
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

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(out)

if __name__ == '__main__':
    main()
