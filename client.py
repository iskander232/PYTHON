from datetime import *
import requests
import json
from datetime import datetime

path = 'http://127.0.0.1:5000/'

help_of_all = '''Напиши post, чтобы создать новую запись,
напиши find чтобы посмотреть старые записи,
напиши help, чтобы увидеть это сообщение,
напиши quit() чтобы выйти из программы.
'''


def post():
    help_post = '''Начни печатать сообщение.
    Чтобы закончить печатать напиши exit() с новой строки,
     если ты передумал отправлять сообщение и done(),
     если это все твое сообщение.
    '''
    print (help_post)
    s = input()
    text = []
    while s != 'exit()' and s != 'done()':
        text.append('\n')
        text.append(s)
        s = input()
    if (s == 'exit()'):
        print (help_of_all)
    elif s == 'done()':
        print('''Напиши название для твоего поста, или 'zzz', тогда он назовется untitled.''')
        name = input()
        if name == 'zzz':
            name = 'untitled'
        requests.post(path + 'post', params={'post': ''.join(text), 'name': name})
    else:
        post()


print ('Hello, user')
print (help_of_all)
s = input()


def print_posts(posts):
    if posts == []:
        print('Ничего не найдено')
    else:
        for post in posts:
            print(post['post'])
            print('''name : {},
date : {},
number : {} '''.format(post['name'], post['date'], post['number']))
            print('\n\n')


def find():
    help_find = '''Напиши 1, если хочешь увидеть все записи, 
    2, если хочешь увидеть записи с номерами в определенном промежутке,
    3, усли хочешь увидеть записи в определенном времянном промежутке,
    4, если хочешь увидеть записи с определенным именем
    quit(), если хочешь закончить'''
    print(help_find)
    x = input()
    if x == '1':
        find_all()
    elif x == '2':
        find_with_num()
    elif x == '3':
        find_with_date()
    elif x == '4':
        find_with_name()
    elif x == 'quit()':
        return
    else:
        print ('Плохая команда' + '\n\n\n')
        find()


def find_all():
    posts = json.loads(requests.get(path).text)
    print_posts(posts)


def find_with_num():
    print('''Напиши, начиная с какого номера ты хочешь увидеть посты или quit(), если передумал''')
    min_num = input()
    if min_num == 'quit':
        return
    no_errors = True
    try:
        min_num = int(min_num)
    except BaseException:
        no_errors = False
    if no_errors:
        print('''Напиши, до какого номера ты хочешь увидеть посты, или quit(), если передумал''')
        max_num = input()
        if max_num == 'quit':
            return
        try:
            max_num = int(min_num)
        except BaseException:
            no_errors = False
    if no_errors:
        posts = json.loads(requests.get(path + 'num', params={'min_num': min_num, 'max_num': max_num}).text)
        print_posts(posts)
    else:
        print ('Неудача')


def find_with_date():
    print('''Напиши, начиная с какой даты ты хочешь увидеть посты,
с новой строки введи год,  месяц, число, и все это разделенное пробелом, или quit(), если передумал.''')
    no_errors = True
    min_date = input()
    x_from = min_date.split(' ')
    if min_date == 'quit()':
        return
    if len(x_from) != 3:
        no_errors = False
    else:
        try:
            max_date = datetime(int(x_from[0]), int(x_from[1]), int(x_from[2]))
        except BaseException:
            no_errors = False
    if not no_errors:
        print('Неверные данные.')
        find_with_date()
    if no_errors:
        print('''Напиши, до какой даты ты хочешь увидеть посты,
с новой строки введи год,  месяц, число, и все это разделенное пробелом, или quit(), если передумал.''')
        max_date = input()
        x_to = max_date.split(' ')
        if max_date == 'quit()':
            return
        if len(x_to) != 3:
            no_errors = False
        else:
            try:
                datetime(int(x_to[0]), int(x_to[1]), int(x_to[2]))
            except BaseException:
                no_errors = False
    if no_errors:
        posts = json.loads(requests.get(path + 'time', params={'min_date': min_date, 'max_date': max_date}).text)
        print_posts(posts)
    else:
        print('Неверные данные.')
        find_with_date()


def find_with_name():
    print('''Введи название, посты с каким именем ты хочешь видеть или quit(), если хочешь вернуться''')
    name = input()
    if name == 'quit()':
        return
    posts = json.loads(requests.get(path + 'name', params={'name': name}).text)
    print_posts(posts)


while s != 'quit()':
    if s == 'post':
        post()
    elif s == 'find':
        find()
    print(help_of_all)
    s = input()
