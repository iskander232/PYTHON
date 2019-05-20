from peewee import *
from datetime import *
from config_server import *

db = PostgresqlDatabase(database=database, user=user, password=password, host=host)


class Post(Model):
    post = CharField()
    date = DateField()
    name = CharField()
    number = AutoField()

    def to_dict(self):
        return {'post': self.post, 'date': self.date, 'name': self.name, 'number': self.number}

    class Meta:
        database = db


def create_tables():
    with db:
        Post.create_table()


def write_post(post, date, name):
    new_post = Post(post=post, date=date, name=name)
    new_post.save()


def search_with_date(date_min, date_max):
    result = []
    for post in Post.select().where((Post.date >= date_min) & (Post.date <= date_max)):
        result.append(post.to_dict())
    return result


def in_base():
    result = []
    for post in Post.select():
        result.append(post.to_dict())
    return result


def search_with_num(min_num, max_num):
    result = []
    for post in Post.select().where((Post.number >= min_num) & (Post.number <= max_num)):
        result.append(post.to_dict())
    return result


def search_with_name(name):
    result = []
    for post in Post.select().where(Post.name == name):
        result.append(post.to_dict())
    return result
