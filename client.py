import requests
import json
from datetime import datetime
from config_client import path

help_of_all = '''Напиши /post, чтобы создать новую запись,
напиши /find чтобы посмотреть старые записи,
напиши help, чтобы увидеть это сообщение,
напиши /quit чтобы выйти из программы.
'''


def post():
    help_post = '''Начни печатать сообщение.
    Чтобы закончить печатать напиши /exit с новой строки,
     если ты передумал отправлять сообщение и /done,
     если это все твое сообщение.
    '''
    print(help_post)
    s = input()
    text = []
    while s != '/exit' and s != '/done':
        text.append('\n' + s)
        s = input()
    if (s == '/exit'):
        print(help_of_all)
    elif s == '/done':
        print('''Напиши название для твоего поста, или нажми ENTER, тогда он назовется untitled.''')
        name = input()
        if name == '':
            name = 'untitled'
        requests.post(path + 'post', params={'post': ''.join(text), 'name': name})
    else:
        post()


print('Hello, user')
print(help_of_all)
s = input()


def print_posts(posts):
    if len(posts) == 0:
        print('Ничего не найдено')
    else:
        posts_2 = []
        for post in posts:
            posts_2.append(post['post'] + '\n' +
                           '''name : {}, date : {}, number : {} '''.format
                           (post['name'], post['date'], post['number']) + '\n\n')
        print(''.join(posts_2))


def find():
    help_find = '''Напиши 1, если хочешь увидеть все записи, 
2, если хочешь увидеть записи с номерами в определенном промежутке,
3, усли хочешь увидеть записи в определенном времянном промежутке,
4, если хочешь увидеть записи с определенным именем
/quit, если хочешь закончить'''
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
    elif x == '/quit':
        return
    else:
        print('Плохая команда' + '\n\n\n')
        find()


def find_all():
    posts = json.loads(requests.get(path).text)
    print_posts(posts)


def processing_num(str_num, text):
    print(text)
    if str_num == '/quit':
        return True
    try:
        return int(str_num)
    except ValueError:
        return False


def find_with_num():
    template = '''Напиши, {} какого номера ты хочешь увидеть посты или /quit, если передумал'''
    min_num = processing_num(input(), template.format('начиная с'))
    if not isinstance(min_num, bool):
        max_num = processing_num(input(), template.format('до'))
    else:
        max_num = min_num
    if min_num is True or max_num is True:
        return
    elif min_num is False or max_num is False:
        print('Неудача, попытайся снова')
        find_with_num()
    else:
        posts = json.loads(requests.get(path + 'num', params={'min_num': min_num, 'max_num': max_num}).text)
        print_posts(posts)


def processing_date(text):
    print(text)
    str_date = input()
    if (str_date == '/quit'):
        return True
    if len(str_date.split(' ')) != 3:
        return False
    else:
        try:
            return str_date
        except TypeError:
            return False


def find_with_date():
    template = '''Напиши, {} какой даты ты хочешь увидеть посты,
с новой строки введи год,  месяц, число, и все это разделенное пробелом, или /quit, если передумал.'''
    min_date = processing_date(template.format('начиная с'))
    if not isinstance(min_date, bool):
        max_date = processing_date(template.format('до'))
    else:
        max_date = min_date
    if max_date is True or min_date is True:
        return
    elif min_date is False or max_date is False:
        print('Неудача, попытайся снова')
        find_with_date()
    else:
        posts = json.loads(requests.get(path + 'time', params={'min_date': min_date, 'max_date': max_date}).text)
        print_posts(posts)


def find_with_name():
    print('''Введи название, посты с каким именем ты хочешь видеть или /quit, если хочешь вернуться''')
    name = input()
    if name == '/quit':
        return
    posts = json.loads(requests.get(path + 'name', params={'name': name}).text)
    print_posts(posts)


while s != '/quit':
    if s == '/post':
        post()
    elif s == '/find':
        find()
    print(help_of_all)
    s = input()
