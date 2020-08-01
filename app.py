from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

import os 
app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
db=SQLAlchemy(app)

class PostModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    image=db.Column(db.String,nullable=False)
    postContent=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(100),nullable=False,default='N/A')
    createdAt=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return 'Posts '+ str(self.name)


@app.route("/")
def index():
	return render_template("index.html",posts=posts)

@app.route("/post", methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title=request.form['title']
        image=request.files['inputFile']
        content=request.form['content']
        author=request.form['author']
        imgAllowtype=["png","jpeg","jpg"]
        imgext=image.filename.split('.')[1]
        for ext in imgAllowtype: 
         if ext==imgext:
             if image:
                  image.save(os.path.join(app.config['UPLOAD_FOLDER'],image.filename))
                  new_post=PostModel(name=title,image=image.filename,postContent=content,author=author)
                  db.session.add(new_post)
                  db.session.commit()
                  return redirect('/posts')
         else:
             return render_template("post.html",msg="Please upload image file")      
    else:
        return render_template("post.html")

@app.route('/posts')
def posts():
    all_posts=PostModel.query.order_by(PostModel.createdAt).all()
    return render_template("posts.html",posts=all_posts)

@app.route('/posts/<int:id>')
def getpost(id):
    getPost=PostModel.query.get_or_404(id)
    return render_template("posts.html",post=getPost)
   
@app.route('/post/edit/<int:id>',methods=['GET','POST'] )
def edit(id):
    if request.method == 'POST':
        getPost=PostModel.query.get_or_404(id)
        getPost.name=request.form['title']
        imgName=request.files['inputFile']
        getPost.image=imgName.filename
        getPost.Postcontent=request.form['content']
        getPost.author=request.form['author']
        imgAllowtype=["png","jpeg","jpg"]
        imgext=imgName.filename.split('.')[1]
        for ext in imgAllowtype: 
         if ext==imgext:
             if imgName:
                  imgName.save(os.path.join(app.config['UPLOAD_FOLDER'],imgName.filename))
                  db.session.commit()
                  return redirect('/posts')
         else:
             return render_template("post.html",msg="Please upload image file")      
             
    else:
        getPost=PostModel.query.get_or_404(id)
        return render_template("edit.html",post=getPost)
   


@app.route('/post/delete/<int:id>')
def delete(id):
    getId=PostModel.query.get_or_404(id)
    db.session.delete(getId)
    db.session.commit()
    return redirect('/posts')


if __name__ == '__main__':
	app.run(debug=True)