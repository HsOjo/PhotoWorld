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
        pagination = ArticleModel.query.order_by(ArticleModel.id.asc()).paginate(None, 5)
        return render_template('portal/index.html', pagination=pagination)

    def search(self):
        keyword = request.args.get('keyword', '')
        if keyword == '':
            return redirect(url_for('portal.index'))

        pagination = ArticleModel.query.order_by(ArticleModel.id.desc()).filter(
            or_(ArticleModel.title.contains(keyword), ArticleModel.content.contains(keyword))
        ).paginate(None, 20)

        return render_template('portal/search.html', pagination=pagination, title='"%s" 的搜索结果' % keyword)
