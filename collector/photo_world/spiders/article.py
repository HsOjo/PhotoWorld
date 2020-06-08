from typing import List

from bs4 import BeautifulSoup, Tag, ResultSet
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ArticleItem


class ArticleSpider(CrawlSpider):
    name = 'photo_world'
    allowed_domains = ['www.photoworld.com.cn']
    start_urls = ['http://www.photoworld.com.cn']
    rules = [Rule(LinkExtractor(allow=['/page/\d+']), 'parse_article', follow=True)]

    def parse_article(self, response: Response):
        bs = BeautifulSoup(response.text, 'html.parser')

        articles = bs.find('div', 'main').find_all('article')
        for article in articles:
            article: Tag
            article_cls = article['class']

            tag_title = article.find('a', attrs={'rel': 'bookmark'})  # type: Tag

            tag_thumb = None
            tags_thumb = None
            type = 0
            if 'single-thumb-article' in article_cls:
                tag_thumb = article.find('img', class_='wp-post-image')  # type: Tag
                type = 1
            elif 'triple-thumb-article' in article_cls:
                tags_thumb = article.find_all('img', class_='triple-thumb-thumbnail-img')  # type: ResultSet
                type = 2
            elif 'no-thumb-article' in article_cls:
                type = 3
            else:
                raise Exception('Unsupport Type.')

            tag_description = article.find('p', class_='excerpt')  # type: Tag
            tag_time = article.find('time', class_='recent-time')  # type: Tag

            tag_category = article.find('span', class_='recent-cat')  # type: Tag
            tag_category = tag_category.find('a') if tag_category is not None else None

            tag_author = article.find('a', attrs={'rel': 'author'})  # type: Tag
            tags_tags = article.find_all('a', {'rel': 'tag'})  # type: ResultSet

            title = tag_title.text if tag_title is not None else ''
            url = tag_title['href'] if tag_title is not None else ''
            description = tag_description.text if tag_description is not None else ''

            if type == 1:
                thumbs = [tag_thumb['src'] if tag_thumb is not None else '']
            elif type == 2:
                thumbs = []
                for tag_thumb in tags_thumb:
                    thumbs.append(tag_thumb['src'] if tag_thumb is not None else '')
            elif type == 3:
                thumbs = []

            time = tag_time['datetime'] if tag_time is not None else ''
            category = tag_category.text if tag_category is not None else ''
            author = tag_author.text if tag_author is not None else ''
            tags = [tag.text for tag in tags_tags]  # type: List[Tag]

            item = ArticleItem()
            params = locals()
            for k in item.fields:
                item[k] = params.get(k)

            yield item
