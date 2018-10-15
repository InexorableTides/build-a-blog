from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:thisisapassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    entry = db.Column(db.String(5000))
    

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry

@app.route('/')
def go_away():

    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    return render_template('index1.html', title="Blog", blogs=blogs)

@app.route('/add', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'POST':
        blog_name = request.form['blog_title']
        blog_body = request.form['blog_entry']

        error = ''
        
        if len(blog_name) == 0 or len(blog_body) == 0:
            error = "Text is required in both fields."
            return render_template('form.html', error=error, title='Add Blog')

        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()


        return render_template('blog-uno.html', blog_name=blog_name, blog_body=blog_body, title='Blog')
    
    return render_template('form.html', title='Add blog')  


@app.route('/blog-post')
def goto_blog():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    blog_name = blog.title
    blog_body = blog.entry


    return render_template('blog-uno.html', title='Blog', blog_name = blog_name, blog_body = blog_body )

if __name__ == '__main__':
    app.run()