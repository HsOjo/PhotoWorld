# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from app import db, app
from app.portal.models import ArticleModel, AuthorModel, CategoryModel, TagModel, ThumbModel
from collector.photo_world.items import ArticleItem

app.app_context().push()


class ArticlePipeline(object):
    def process_item(self, item: ArticleItem, spider):
        url = item['url']
        if url is None or url == '':
            return item

        for k, v in item.items():
            if isinstance(v, str):
                item[k] = v.strip()

        time = item['time']
        time = None if time == '' else time
        item['time'] = time

        article = ArticleModel.query.filter_by(url=url).first()
        if article is None:
            author_name = item['author']
            author = AuthorModel.query.filter_by(name=author_name).first()
            if author is None:
                author = AuthorModel(name=author_name)

            category_name = item['category']
            category = CategoryModel.query.filter_by(name=category_name).first()
            if category is None:
                category = CategoryModel(name=category_name)

            tags = []
            for tag_name in item['tags']:
                if tag_name == '':
                    continue
                tag_name = tag_name.strip()
                tag = TagModel.query.filter_by(name=tag_name).first()
                if tag is None:
                    tag = TagModel(name=tag_name)
                tags.append(tag)

            thumbs = []
            for thumb_url in item['thumbs']:
                if thumb_url == '':
                    continue
                thumb = ThumbModel.query.filter_by(url=thumb_url).first()
                if thumb is None:
                    thumb = ThumbModel(url=thumb_url)
                thumbs.append(thumb)

            article = ArticleModel(
                url=item['url'],
                title=item['title'],
                description=item['description'],
                thumbs=thumbs,
                time=item['time'],
                author=author,
                category=category,
                tags=tags,
                type=item['type'],
            )

            db.session.add(article)
            db.session.commit()

        return item
