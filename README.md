# PhotoWorld

* 目标网站：https://www.photoworld.com.cn/
* 实现爬取文章（url，标题，标签，示例图片，作者，描述）。
* 支持翻页爬取，支持多标签数据整理

~~这是一个大作业项目。~~
 
## 查询功能

* 支持按标题关键字查询，显示文章列表
* 支持按标签查询，显示文章列表
* 支持按作者查询，显示文章列表

## 技术介绍

* 使用**Scrapy**进行数据爬取，通过BeautifulSoup4进行数据解析。
* 使用**Flask**完成Web后端查询程序的开发，前端页面基于Bootstrap实现。
* 支持使用**MySQL**/**Sqlite**数据库存储数据。
* 支持通过**uWSGI**以及**systemd**进行生产环境部署。

## 使用方法

* 安装依赖包。

```bash
pip install -r requirements.txt
```

* 同步数据。

```bash
python manage.py sync_articles
```

* 启动数据查询服务器。

```bash
python manage.py runserver
```

* 打开浏览器，访问Web界面

## 项目亮点

使用MySQL数据库存储数据，确保了数据的稳定性、可维护性（建立了各类数据的关联）；同时提供了极高的查询性能。

使用Flask轻量级Web框架开发用户界面，提供了Python环境无缝衔接的操作体验。

## 心得

Scrapy真不愧是工程化的爬虫框架，数据处理相当规范。

相较于直接使用requests进行编写爬虫来说，更为复杂。
