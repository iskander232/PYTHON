#! /usr/bin/python3
import argparse
import sys
import string

alf = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'


def find(code, symvol):
    if code == 'encode':
        return alf.find(symvol)
    else:
        return 26 - alf.find(symvol)


def read(file):
    if file == 'sys.stdin':
        return input()
    else:
        with open(file, 'r') as f:
            return f.read()


def write(file, res):
    if file == 'sys.stdout':
        print(res)
    else:
        with open(file, 'w') as f:
            f.write(res)


def give_dict(file):
    d = dict()
    with open(file, 'r') as f:
        for i in range(52):
            line = f.readline()
            d[string.ascii_letters[i]] = float(line[:-1])
    return d


def statistic(s):
    d = dict()
    sum = 0
    for x in alf:
        d[x] = 0
    for i in s:
        if i in alf:
            sum += 1
            d[i] = d[i] + 1
    for i in string.ascii_letters:
        d[i] /= sum
    return d


def give_caesar(code, str1, key):
    res = ""
    for i in range(str1.__len__()):
        if alf.find(str1[i]) != -1:
            res += (alf[alf.find(str1[i]) + find(code, alf[key])])
        else:
            res += str1[i]
    return res


def caesar(code, args):
    res = give_caesar(code, read(args.input_file), int(args.key))
    write(args.output_file, res)


def vigenere(code, args):
    str1 = read(args.input_file)
    key1 = ""
    while key1.__len__() < str1.__len__():
        key1 += args.key
    res = ""
    for i in range(str1.__len__()):
        if alf.find(str1[i]) != -1:
            res += alf[alf.find(str1[i]) + find(code, key1[i])]
        else:
            res += str1[i]
    write(args.output_file, res)


def encode(args):
    if args.cipher == 'caesar':
        caesar('encode', args)
    else:
        vigenere('encode', args)


def decode(args):
    if args.cipher == 'caesar':
        caesar('decode', args)
    else:
        vigenere('decode', args)


def train(args):
    d = statistic(read(args.input_file))
    res = ''
    for i in string.ascii_letters:
        res += str(d[i]) + "\n"
    write(args.model_file, res)


def hack(args):
    s = read(args.input_file)
    min = 100
    d = give_dict(args.model_file)
    res = ''
    for i in range(26):
        s1 = give_caesar('decode', s, i)
        d1 = statistic(s1)
        dist = 0
        for j in range(52):
            c = string.ascii_letters[j]
            dist += abs(d[c] - d1[c])
        if dist < min:
            min = dist
            res = s1
    write(args.output_file, res)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# create parser_encode
parser_encode = subparsers.add_parser('encode')
parser_encode.add_argument('--cipher', type=str, required=True)
parser_encode.add_argument('--key', type=str, required=True)
parser_encode.add_argument('--input-file', default='sys.stdin')
parser_encode.add_argument('--output-file', default='sys.stdout')
parser_encode.set_defaults(func=encode)
# create parser decode
parser_decode = subparsers.add_parser('decode')
parser_decode.add_argument('--cipher', type=str, required=True)
parser_decode.add_argument('--key', type=str, required=True)
parser_decode.add_argument('--input-file', type=str, default='sys.stdin')
parser_decode.add_argument('--output-file', default='sys.stdout')
parser_decode.set_defaults(func=decode)
# create parser train
parser_train = subparsers.add_parser('train')
parser_train.add_argument('--text-file', dest='input_file', default='sys.stdin')
parser_train.add_argument('--model-file', required=True)
parser_train.set_defaults(func=train)
# create parser hack
parser_hack = subparsers.add_parser('hack')
parser_hack.add_argument('--input-file', default='sys.stdin')
parser_hack.add_argument('--output-file', default='sys.stdout')
parser_hack.add_argument('--model-file', required=True)
parser_hack.set_defaults(func=hack)
args = parser.parse_args()
args.func(args)
