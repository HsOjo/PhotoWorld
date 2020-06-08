from flask import render_template, request, redirect, url_for
from sqlalchemy import or_

from app.base import Controller
from .models import *


class PortalController(Controller):
    import_name = __name__
    name = 'portal'
    url_prefix = '/'

    def callback_add_routes(self):
        self.add_route('/', self.index)
        self.add_route('/search', self.search)

    def index(self):
        pagination = ArticleModel.query.order_by(ArticleModel.date.desc()).paginate(None, 5)
        return render_template('portal/index.html', pagination=pagination)

    def search(self):
        per_page = request.args.get('per_page', 20)
        if isinstance(per_page, str) and per_page.isnumeric():
            per_page = int(per_page)
        keyword = request.args.get('keyword', '').strip()
        if keyword == '':
            return redirect(url_for('portal.index'))

        tag = TagModel.query.filter_by(name=keyword).first()  # type: TagModel
        author = AuthorModel.query.filter_by(name=keyword).first()  # type: AuthorModel
        category = CategoryModel.query.filter_by(name=keyword).first()  # type: CategoryModel
        if tag is not None:
            prefix = '标签'
            pagination = tag.articles.order_by(ArticleModel.date.desc()).paginate(None, per_page)
        elif author is not None:
            prefix = '作者'
            pagination = author.articles.order_by(ArticleModel.date.desc()).paginate(None, per_page)
        elif category is not None:
            prefix = '分类'
            pagination = category.articles.order_by(ArticleModel.date.desc()).paginate(None, per_page)
        else:
            prefix = ''
            pagination = ArticleModel.query.order_by(ArticleModel.date.desc()).filter(or_(
                ArticleModel.title.contains(keyword),
                ArticleModel.description.contains(keyword),
            )).paginate(None, per_page)

        return render_template('article/list.html', pagination=pagination, title='%s "%s" 的搜索结果' % (prefix, keyword))
