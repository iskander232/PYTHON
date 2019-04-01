#! /usr/bin/python3
import argparse
import sys
import string
import collections
import time

alf = string.ascii_lowercase * 2 + string.ascii_uppercase * 2


def find(code, symbol):
    if code == 'encode':
        return alf.find(symbol)
    else:
        return string.ascii_lowercase.__len__() - alf.find(symbol)


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


def model_to_statistic(file):
    """
    This function returns symbol statistics by modul file
    :param file:
    :return:
    """
    d = dict()
    with open(file, 'r') as f:
        for i in range(string.ascii_letters.__len__()):
            line = f.readline()
            d[string.ascii_letters[i]] = float(line[:-1])
    return d


def statistic(s):
    d = collections.Counter()
    sum = 0
    for i in s:
        if i in alf:
            sum += 1
            d[i] += 1
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
    local_min = float("inf")
    d = model_to_statistic(args.model_file)
    res = ''
    for i in string.ascii_lowercase:
        s1 = give_caesar('decode', s, alf.find(i))
        d1 = statistic(s1)
        dist = 0
        for c in string.ascii_letters:
            dist += abs(d[c] - d1[c])
        if dist < local_min:
            local_min = dist
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
