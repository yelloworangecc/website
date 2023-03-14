import os

from flask import Blueprint,abort,request,render_template,current_app

from py.ArticleManager import Article

module_blog = Blueprint('module_blog', __name__, url_prefix='/blog')
current_app.config['BLOG_PER_PAGE'] = 5

@module_blog.route('/index')
def index():
    if not Article.load():
        return '<h1>load articles failed</h1>'

    articles = Article.getPageList(0, current_app.config['BLOG_PER_PAGE'])
    return render_template('blog.html',articles=articles)

@module_blog.route('/<name>')
def article(name):    
    return render_template(f'posts/{name}')

