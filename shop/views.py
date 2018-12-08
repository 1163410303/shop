from shop import app, db
from flask import render_template, redirect, request, flash, get_flashed_messages, jsonify
from shop.models import User, GoodType, Good
from flask_login import login_user, logout_user, login_required,current_user
import hashlib


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/type/')
def type():
    types = GoodType.query.all()
    return render_template('type.html',types = types)


@app.route('/inventory/')
def inventory():
    return render_template('inventory.html')


@app.route('/inbound/')
def inboud():
    return render_template('inbound.html')


@app.route('/warning/')
def warning():
    return render_template('warning.html')


@app.route('/outBoud/')
def outboud():
    return render_template('outBoud.html')


@app.route('/user/')
def user():
    return render_template('user.html')


@app.route('/updatePwd/')
def updatePwd():
    return render_template('updatePwd.html')


@app.route('/admin/')
@login_required
def admin():
    if current_user.username != 'admin':
        return render_template("index.html",msg = '您没有访问权限')
    return render_template('admin.html')


@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template("login.html", msg=msg)


@app.route('/addtype/', methods={'get', 'post'})
def addtype():
    name = request.values.get('name').strip()
    remark = request.values.get('remark').strip()
    description = request.values.get('description').strip()
    db.session.add(GoodType(name, remark, description))
    db.session.commit()
    return redirect('/type/')


@app.route('/delete_type/', methods={'get', 'post'})
def delete_type():
    tid = request.form['id']
    GoodType.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })


@app.route('/edit_type/', methods={'get', 'post'})
def edit_type():
    id = request.form['id']
    name = request.form['type_name']
    remark = request.form['remark']
    description = request.form['description']
    GoodType.query.filter_by(id=id).update({'name' : name, 'remark' : remark , 'description': description})
    db.session.commit()
    return jsonify({'msg' : 'OK'})


@app.route('/reg/', methods={'get', 'post'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    user = User.query.filter_by(username=username).first()
    if username == '' or password == '':
        flash('用户名和密码不能为空', 'reglogin')
        return redirect('/regloginpage/')
    if user != None:
        flash('用户名已经存在', 'reglogin')
        return redirect('/regloginpage/')

    m = hashlib.md5()
    m.update(password.encode("utf8"))
    password = m.hexdigest()
    user = User(username, password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    if user.username == 'admin':
        return redirect('/admin/')
    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    user = User.query.filter_by(username=username).first()
    if username == '' or password == '':
        flash('用户名和密码不能为空', 'reglogin')
        return redirect('/regloginpage/')
    if user == None:
        flash('该用户不存在', 'reglogin')
        return redirect('/regloginpage/')
    m = hashlib.md5()
    m.update(password.encode("utf8"))
    password = m.hexdigest()
    if password == user.password:
        login_user(user)
        if user.username == 'admin':
            return redirect('/admin/')
        return redirect('/')
    else:
        flash('密码错误，请重新输入', 'reglogin')
        return redirect('/regloginpage/')
