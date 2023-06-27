import os,io,re

from flask import Blueprint,abort,request,render_template,current_app
from werkzeug.utils import secure_filename
from py.ArticleManager import Article
from cryptography.fernet import Fernet

f = Fernet(os.getenv("FERNET_KEY").encode())
module_blog = Blueprint('module_blog', __name__, url_prefix='/blog')
current_app.config['BLOG_PER_PAGE'] = 5

@module_blog.route('/index')
def index():
    if not Article.load():
        return '<h1>load articles failed</h1>'

    articles = Article.getPageList(0, current_app.config['BLOG_PER_PAGE'])
    return render_template('listpage.html',view_func='module_blog.article',itemList=articles)

@module_blog.route('/<name>')
def article(name):
    article = Article.get(name)
    if not article:
        return abort(404)
    return render_template('article.html',article=article)

@module_blog.route('/publish', methods=['POST'])
def publish():
    try:
        token=request.args["token"].encode()
        data = f.decrypt(token,ttl=100)
        if os.getenv("SECRET_KEY").encode() != data:
            return abort(403)
    except:
        return abort(403)

    if 'file' not in request.files:
        return abort(406)
        
    file = request.files['file']
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'html':
        filename = secure_filename(file.filename)
        content = str(file.read(), encoding='utf8').replace('{{','{ {').replace('}}','} }').replace('{%','{ %').replace('%}','% }').replace('\r\n','\n')
        with open(os.path.join(current_app.root_path, 'templates', 'posts', filename),'w',encoding='utf8') as fp:
            fp.write(content)
            
        content = io.StringIO(content)
        while True:
            line = content.readline().strip()
            print(line)
            if line[0] == '<' and line[1] == 'h' and line[2] == '1':
                title = re.search('>.*<',line).group()[1:-1]
            elif line[0] == '<' and line[1] == 'p':
                multiline = line
            elif line[0] == '<' and line[1] == 'h' and line[2] == '2':
                abstract = re.search('>.*<',multiline).group()[1:-1]
                break
            else:
                multiline = multiline + ' ' + line
                
        #print(filename)
        #print(title)
        #print(abstract)
        Article.add(filename,title,abstract)                
        return 'OK'
    return abort(406)
