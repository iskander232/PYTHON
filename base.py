from peewee import *
from datetime import *
from config import *

db = PostgresqlDatabase(database=database, user=user, password=password, host=host)
db.post_number = 1


class Post(Model):
    post = CharField()
    date = DateField()
    name = CharField()
    number = IntegerField()

    class Meta:
        database = db


def create_tables():
    with db:
        Post.create_table()


def write_post(post, date, name, number):
    new_post = Post(post=post, date=date, name=name, number=number)
    new_post.save()


def search_with_date(date_min, date_max):
    result = []
    for post in Post.select().where((Post.date >= date_min) & (Post.date <= date_max)):
        result.append({'post': post.post, 'date': post.date, 'name': post.name, 'number': post.number})
    return result


def in_base():
    result = []
    for post in Post.select():
        result.append({'post': post.post, 'date': post.date, 'name': post.name, 'number': post.number})
    return result


def search_with_num(min_num, max_num):
    result = []
    for post in Post.select().where((Post.number >= min_num) & (Post.number <= max_num)):
        result.append({'post': post.post, 'date': post.date, 'name': post.name, 'number': post.number})
    return result


def search_with_name(name):
    result = []
    for post in Post.select().where(Post.name == name):
        result.append({'post': post.post, 'date': post.date, 'name': post.name, 'number': post.number})
    return result
