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
    close_count = 0

    def process_item(self, item: ArticleItem, spider):
        # 数据处理部分
        url = item['url']
        if url is None or url == '':
            return item

        for k, v in item.items():
            if isinstance(v, str):
                item[k] = v.strip()

        date = item['date']
        date = None if date == '' else date
        item['date'] = date

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

            # 数据导入部分
            article = ArticleModel(
                url=item['url'],
                title=item['title'],
                description=item['description'],
                thumbs=thumbs,
                date=item['date'],
                author=author,
                category=category,
                tags=tags,
                type=item['type'],
            )

            db.session.add(article)
            db.session.commit()
        else:
            if self.close_count >= 20:
                spider.crawler.engine.close_spider(spider, "当前页已爬取，关闭爬虫。")
            else:
                self.close_count += 1

        return item
