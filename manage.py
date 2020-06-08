from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

from app import app, db
from app.portal.models import AuthorModel, CategoryModel, TagModel, ArticleModel

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(
    make_context=lambda: dict(
        db=db,
        AuthorModel=AuthorModel,
        CategoryModel=CategoryModel,
        TagModel=TagModel,
        ArticleModel=ArticleModel,
    )))

if __name__ == '__main__':
    manager.run()