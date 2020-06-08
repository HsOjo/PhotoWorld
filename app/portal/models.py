from typing import List

from app import db


class CategoryModel(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(32))


class AuthorModel(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(32))


class ArticleModel(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    url = db.Column(db.VARCHAR(256))
    title = db.Column(db.VARCHAR(256))
    description = db.Column(db.VARCHAR(512))
    thumb_url = db.Column(db.VARCHAR(256))
    time = db.Column(db.DATETIME, index=True)

    author_id = db.Column(db.INTEGER, db.ForeignKey(AuthorModel.id))
    category_id = db.Column(db.INTEGER, db.ForeignKey(CategoryModel.id))

    author = db.relationship('AuthorModel', uselist=False)  # type: AuthorModel
    category = db.relationship('CategoryModel', uselist=False)  # type: CategoryModel
    tags = db.relationship('TagModel', secondary='tag_connect', uselist=True)  # type: List[TagModel]


class TagModel(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(32))

    articles = db.relationship('ArticleModel', secondary='tag_connect', uselist=True)  # type: List[ArticleModel]


class TagConnectModel(db.Model):
    __tablename__ = 'tag_connect'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    article_id = db.Column(db.INTEGER, db.ForeignKey(ArticleModel.id), index=True)
    tag_id = db.Column(db.INTEGER, db.ForeignKey(TagModel.id), index=True)
