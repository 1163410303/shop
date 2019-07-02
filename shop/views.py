from shop import app, db
from flask import render_template, redirect, request, flash, get_flashed_messages, jsonify
from shop.models import User, GoodType, Good, InboundLoad, outboudLoad, warningLoad, Order, Warehouse, Cart
from flask_login import login_user, logout_user, login_required,current_user
import hashlib
import datetime

# 路由管理

#默认主页
@app.route('/')
@login_required
def index():
    return render_template("shop.html")

# 商城用户页
@app.route('/shop/')
@login_required
def shop():
    return render_template("shop.html")


# 商城购物车页
@app.route('/cart/')
@login_required
def cart():
    goodsInCart = Cart.query.filter_by(user_id=current_user.id).all()
    cartLength = len(goodsInCart)
    goods = []
    quantitys = []
    images = []
    cartids = []
    for i in range(cartLength):
        cartids.append(goodsInCart[i].id)
        good = Good.query.filter_by(id=goodsInCart[i].good_id).all()[0]
        goods.append(good)
        quantitys.append(goodsInCart[i].quantity)
        images.append(good.images.filter_by(istitle=1).all()[0].url)
    return render_template("cart.html", cartLength = cartLength, goods=goods, quantitys = quantitys, images=images, cartids=cartids)


@app.route('/delete_cart/<cid>',methods={'post', 'get'})
def delete_cart(cid):
    Cart.query.filter_by(id=cid).delete()
    db.session.commit()
    return redirect('/cart')

# 我的订单页
@app.route('/myorder')
@login_required
def myorder():
    orders = Order.query.filter_by(username=current_user.username).all()
    return render_template('myorder.html', orders = orders)

# 个人信息页
@app.route('/contact/')
@login_required
def contact():
    # user_contact = User.query.filter_by(id=current_user.id).all()[0]
    return render_template("contact.html", current_user=current_user)


# 商品详情页
@app.route('/detail/<gid>')
@login_required
def detail(gid):
    good = Good.query.filter_by(id=gid).all()[0]
    content = good.content
    images = good.images.filter_by(istitle=0)
    trade_price = good.trade_price
    retail_price = good.retail_price
    return render_template("detail.html", content=content, images=images, trade_price=trade_price, retail_price=retail_price, gid = gid)


@app.route('/detail/<gid>/<msg>')
@login_required
def detail_1(gid, msg):
    good = Good.query.filter_by(id=gid).all()[0]
    content = good.content
    images = good.images.filter_by(istitle=0)
    trade_price = good.trade_price
    retail_price = good.retail_price
    print(msg)
    return render_template("detail.html", content=content, images=images, trade_price=trade_price, retail_price=retail_price, gid=gid, msg=msg)


#商品种类管理页
@app.route('/type/')
def type():
    types = GoodType.query.all()
    return render_template('type.html',types = types)

#仓库管理页
@app.route('/warehouse/')
def warehouse():
    warehouses = Warehouse.query.all()
    return render_template('warehouse.html',warehouses = warehouses)


@app.route('/inventory/')
def inventory():
    inventorys = Good.query.all()
    return render_template('inventory.html',inventorys = inventorys)


@app.route('/inbound/')
def inbound():
    inbounds = InboundLoad.query.all()
    return render_template('inbound.html',inbounds = inbounds)


@app.route('/warning/')
def warning():
    warnings = warningLoad.query.all()
    return render_template('warning.html',warnings = warnings)


@app.route('/outBoud/')
def outboud():
    outbouds = outboudLoad.query.all()
    return render_template('outBoud.html',outbouds = outbouds)


@app.route('/user/')
def user():
    users = User.query.all()
    return render_template('user.html',users = users)


@app.route('/updatePwd/')
def updatePwd():
    return render_template('updatePwd.html')


@app.route('/order/')
def order():
    orders = Order.query.all()
    return render_template('order.html',orders = orders)


@app.route('/admin/')
@login_required
def admin():
    if current_user.username != 'admin':
        return render_template("shop.html", msg = '您的权限不足，请联系管理员提升权限')
    return render_template('admin.html')


@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template("login.html", msg=msg)


# 业务逻辑
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

@app.route('/addgood/', methods={'get', 'post'})
def addgood():
    name = request.values.get('name').strip()
    quantity = request.values.get('quantity').strip()
    content = request.values.get('content').strip()
    type_name = request.values.get('type_name').strip()
    purchase_price = request.values.get('purchase_price').strip()
    trade_price = request.values.get('trade_price').strip()
    retail_price = request.values.get('retail_price').strip()
    warehouse_name = request.values.get('warehouse_name').strip()
    if GoodType.query.filter_by(name=type_name).all() == []:
        return redirect('/inventory/')
    elif Warehouse.query.filter_by(name=warehouse_name).all() == []:
         return redirect('/inventory/')
    db.session.add(Good(name, int(quantity), content, type_name, float(purchase_price), float(trade_price), float(retail_price), '', warehouse_name))
    db.session.commit()
    return redirect('/inventory/')

@app.route('/delete_good/', methods={'get', 'post'})
def delete_good():
    tid = request.form['id']
    Good.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })

@app.route('/edit_good/', methods={'get', 'post'})
def edit_good():
    id = request.form['id']
    name = request.form['name']
    quantity = request.form['quantity']
    content = request.form['content']
    type_name = request.form['type_name']
    purchase_price = request.form['purchase_price']
    trade_price = request.form['trade_price']
    retail_price = request.form['retail_price']
    Good.query.filter_by(id=id).update({'name' : name, 'quantity' : quantity, 'content': content, 'type_name' : type_name, 'purchase_price' : purchase_price, 'trade_price' : trade_price, 'retail_price' : retail_price})
    db.session.commit()
    return jsonify({'msg' : 'OK'})

@app.route('/addinbound/', methods={'get', 'post'})
def addinbound():
    name = request.values.get('name').strip()
    type_name = request.values.get('type_name').strip()
    purchase_price = request.values.get('purchase_price').strip()
    quantity = request.values.get('quantity').strip()
    warehouse_name = request.values.get('warehouse_name').strip()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    remark = request.values.get('remark').strip()
    db.session.add(InboundLoad(name, type_name, float(purchase_price), int(quantity), warehouse_name, date, remark))
    if Good.query.filter_by(name=name,warehouse_name=warehouse_name).all() == []:
        db.session.add(Good(name, int(quantity), None, type_name, float(purchase_price), 0, 0, '', warehouse_name))
    else :
        a = int(Good.query.filter_by(name=name,warehouse_name=warehouse_name).all()[0].quantity)
        b = a + int(quantity)
        Good.query.filter_by(name=name,warehouse_name=warehouse_name).update({'quantity' : b})
    db.session.commit()
    return redirect('/inbound/')

@app.route('/delete_inbound/', methods={'get', 'post'})
def delete_inbound():
    tid = request.form['id']
    InboundLoad.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })

@app.route('/edit_inbound/', methods={'get', 'post'})
def edit_inbound():
    id = request.form['id']
    name = request.form['name']
    type_name = request.form['type_name']
    purchase_price = request.form['purchase_price']
    quantity = request.form['quantity']
    date = request.form['date']
    remark = request.form['remark']
    a = int(Good.query.filter_by(name=name,warehouse_name=InboundLoad.query.filter_by(id=id).all()[0].warehouse_name).all()[0].quantity) + int(quantity) - int(InboundLoad.query.filter_by(id=id).all()[0].quantity)
    InboundLoad.query.filter_by(id=id).update({'name': name, 'type_name': type_name, 'purchase_price' : float(purchase_price), 'quantity': int(quantity), 'date': date, 'remark' : remark})
    Good.query.filter_by(name=name,warehouse_name=InboundLoad.query.filter_by(id=id).all()[0].warehouse_name).update({'quantity': a})
    db.session.commit()
    return jsonify({'msg' : 'OK'})

@app.route('/addoutboud/', methods={'get', 'post'})
def addoutboud():
    name = request.values.get('name').strip()
    type_name = request.values.get('type_name').strip()
    quantity = request.values.get('quantity').strip()
    warehouse_name = request.values.get('warehouse_name').strip()
    remark = request.values.get('remark').strip()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    if Good.query.filter_by(name=name,type_name=type_name,warehouse_name=warehouse_name).all() == [] :
     return redirect('/outBoud/')
    elif int(Good.query.filter_by(name=name,type_name=type_name,warehouse_name=warehouse_name).all()[0].quantity)<int(quantity) :
        return redirect('/outBoud/')
    db.session.add(outboudLoad(name, type_name, int(quantity), warehouse_name, date, remark))
    a = int(Good.query.filter_by(name=name,warehouse_name=warehouse_name).all()[0].quantity)
    b = a - int(quantity)
    Good.query.filter_by(name=name,warehouse_name=warehouse_name).update({'quantity' : b})
    db.session.commit()
    return redirect('/outBoud/')

@app.route('/delete_outboud/', methods={'get', 'post'})
def delete_outboud():
    tid = request.form['id']
    outboudLoad.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })

@app.route('/edit_outboud/', methods={'get', 'post'})
def edit_outboud():
    id = request.form['id']
    name = request.form['name']
    type_name = request.form['type_name']
    quantity = request.form['quantity']
    date = request.form['date']
    remark = request.form['remark']
    if Good.query.filter_by(name=name,type_name=type_name,warehouse_name=outboudLoad.query.filter_by(id=id).all()[0].warehouse_name).all() == [] :
     return jsonify({'msg' : 'null'})
    elif int(Good.query.filter_by(name=name,type_name=type_name,warehouse_name=outboudLoad.query.filter_by(id=id).all()[0].warehouse_name).all()[0].quantity)<int(quantity)-int(outboudLoad.query.filter_by(id=id).all()[0].quantity) :
        return jsonify({'msg' : 'less'})
    a = int(Good.query.filter_by(name=name,warehouse_name=outboudLoad.query.filter_by(id=id).all()[0].warehouse_name).all()[0].quantity)-int(quantity)+int(outboudLoad.query.filter_by(id=id).all()[0].quantity)
    outboudLoad.query.filter_by(id=id).update({'name': name, 'type_name': type_name, 'quantity': int(quantity), 'date': date, 'remark': remark})
    Good.query.filter_by(name=name,warehouse_name=outboudLoad.query.filter_by(id=id).all()[0].warehouse_name).update({'quantity' : a})
    db.session.commit()
    return jsonify({'msg' : 'OK'})

@app.route('/adduser/', methods={'get', 'post'})
def adduser():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    sex = request.values.get('sex').strip()
    phone = request.values.get('phone').strip()
    email = request.values.get('email').strip()
    remark = request.values.get('remark').strip()
    address = request.values.get('address').strip()
    m = hashlib.md5()
    m.update(password.encode("utf8"))
    password = m.hexdigest()
    db.session.add(User(username, password, sex, phone, email, remark, address, ''))
    db.session.commit()
    return redirect('/user/')

@app.route('/delete_user/', methods={'get', 'post'})
def delete_user():
    tid = request.form['id']
    User.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })

@app.route('/edit_user/', methods={'get', 'post'})
def edit_user():
    id = request.form['id']
    username = request.form['username']
    password = request.form['password']
    sex = request.form['sex']
    remark = request.form['remark']
    User.query.filter_by(id=id).update({'username' : username, 'password' : password, 'sex' : sex, 'remark' : remark})
    db.session.commit()
    return jsonify({'msg' : 'OK'})

@app.route('/addwarning/', methods={'get', 'post'})
def addwarning():
    name = request.values.get('name').strip()
    type_name = request.values.get('type_name').strip()
    warehouse_name = request.values.get('warehouse_name').strip()
    quantity = request.values.get('quantity').strip()
    remark = request.values.get('remark').strip()
    db.session.add(warningLoad(name, type_name, warehouse_name, quantity, remark))
    db.session.commit()
    return redirect('/warning/')

@app.route('/delete_warning/', methods={'get', 'post'})
def delete_warning():
    tid = request.form['id']
    warningLoad.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })

@app.route('/edit_warning/', methods={'get', 'post'})
def edit_warning():
    id = request.form['id']
    name = request.form['name']
    type_name = request.form['type_name']
    quantity = request.form['quantity']
    remark = request.form['remark']
    warningLoad.query.filter_by(id=id).update({'name' : name, 'type_name' : type_name, 'quantity': quantity, 'remark' : remark})
    db.session.commit()
    return jsonify({'msg' : 'OK'})

@app.route('/FBI_warning/', methods={'get', 'post'})
def FBI_warning():
    hello = request.values.get('hello').strip()
    warning_list = warningLoad.query.all()
    for a in warning_list:
        if int(a.quantity) > int(Good.query.filter_by(name=a.name,warehouse_name=a.warehouse_name).all()[0].quantity):
            return jsonify({'msg' : 'warning'})
    return jsonify({'msg' : hello})

@app.route('/changepassword/', methods={'get', 'post'})
def changepassword():
    password1 = request.values.get('password1').strip()
    password2 = request.values.get('password2').strip()
    m = hashlib.md5()
    m.update(password1.encode("utf8"))
    password1 = m.hexdigest()
    n = hashlib.md5()
    n.update(password2.encode("utf8"))
    password2 = n.hexdigest()
    if User.query.filter_by(id=current_user.id).all()[0].password == password1 :
        User.query.filter_by(id=current_user.id).update({'password' : password2})
    db.session.commit()
    return redirect('/updatePwd/')

@app.route('/addorder/', methods={'get', 'post'})
def addorder():
    good_id = request.values.get('good_id').strip()
    good_name = request.values.get('good_name').strip()
    quantity = request.values.get('quantity').strip()
    price = request.values.get('price').strip()
    username = request.values.get('username').strip()
    address = request.values.get('address').strip()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    remark = request.values.get('remark').strip()
    db.session.add(Order(good_id, good_name, quantity, price, username, address, date, remark, '待审核',0))
    db.session.commit()
    return redirect('/order/')

@app.route('/delete_order/', methods={'get', 'post'})
def delete_order():
    tid = request.form['id']
    Order.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })


@app.route('/edit_order/', methods={'get', 'post'})
def edit_order():
    id = request.form['id']
    good_id = request.form['good_id']
    good_name = request.form['good_name']
    quantity = request.form['quantity']
    price = request.form['price']
    username = request.form['username']
    address = request.form['address']
    date = request.form['date']
    remark = request.form['remark']
    Order.query.filter_by(id=id).update({'good_id' : good_id, 'good_name' : good_name, 'quantity': quantity, 'price' : price, 'username' : username, 'address' : address, 'date' : date, 'remark' : remark})
    db.session.commit()
    return jsonify({'msg' : 'OK'})

@app.route('/confirm_order/', methods={'get', 'post'})
def confirm_order():
    tid = request.form['id']
    Order.query.filter_by(id = tid).update({'state' : '已审核'})
    db.session.commit()
    return jsonify({"msg": 'success' })


@app.route('/trans_order/', methods={'get', 'post'})
def trans_order():
    tid = request.form['id']
    Order.query.filter_by(id = tid).update({'state' : '已发货'})
    db.session.commit()
    return jsonify({"msg": 'success' })


@app.route('/cancel_order/', methods={'get', 'post'})
def cancel_order():
    tid = request.form['id']
    Order.query.filter_by(id = tid).update({'state' : '退货中'})
    db.session.commit()
    return jsonify({"msg": 'success' })


@app.route('/addwarehouse/', methods={'get', 'post'})
def addwarehouse():
    name = request.values.get('name').strip()
    address = request.values.get('address').strip()
    remark = request.values.get('remark').strip()
    db.session.add(Warehouse(name, address, remark))
    db.session.commit()
    return redirect('/warehouse/')

@app.route('/delete_warehouse/', methods={'get', 'post'})
def delete_warehouse():
    tid = request.form['id']
    Warehouse.query.filter_by(id = tid).delete()
    db.session.commit()
    return jsonify({"msg": 'success' })

@app.route('/edit_warehouse/', methods={'get', 'post'})
def edit_warehouse():
    id = request.form['id']
    name = request.form['name']
    address = request.form['address']
    remark = request.form['remark']
    Warehouse.query.filter_by(id=id).update({'name' : name, 'address' : address, 'remark' : remark})
    db.session.commit()
    return jsonify({'msg' : 'OK'})


@app.route('/add_cart/<gid>', methods={'get', 'post'})
def add_cart(gid):
    quantity = request.values.get('quantity')
    db.session.add(Cart(current_user.id, gid, quantity))
    db.session.commit()
    msg = '添加成功'
    return redirect('/detail/'+str(gid)+'/'+msg)


@app.route('/add_myorder/<gid>', methods={'get', 'post'})
def add_myorder(gid):
    quantity = request.values.get('quantity')
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    good = Good.query.filter_by(id=gid).all()[0]
    good_name = good.name
    username = current_user.username
    if int(quantity) < 20:
        price = good.retail_price
    else:
        price = good.trade_price
    address = current_user.address
    gross_profit = price - good.purchase_price
    db.session.add(Order(gid, good_name, quantity, price, username, address, date, '暂无', '待审核', gross_profit))
    db.session.commit()
    return redirect('/myorder')


@app.route('/confirm_myorder/<cid>', methods={'get', 'post'})
def confirm_myorder(cid):
    cart = Cart.query.get(cid)
    quantity = cart.quantity
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    good = Good.query.filter_by(id=cart.good_id).all()[0]
    good_name = good.name
    username = current_user.username
    if int(quantity) < 20:
        price = good.retail_price
    else:
        price = good.trade_price
    address = current_user.address
    gross_profit = price - good.purchase_price
    db.session.add(Order(cart.good_id, good_name, quantity, price, username, address, date, '暂无', '待审核', gross_profit))
    Cart.query.filter_by(id=cid).delete()
    db.session.commit()
    return redirect('/myorder')


@app.route('/edit_username/', methods={'get', 'post'})
def edit_username():
    username = request.values.get('username').strip()
    User.query.filter_by(id=current_user.id).update({'username': username})
    db.session.commit()
    return redirect('/contact')


@app.route('/edit_password/', methods={'get', 'post'})
def edit_password():
    old_password = request.values.get('old_password').strip()
    new_password = request.values.get('new_password').strip()
    m = hashlib.md5()
    m.update(old_password.encode("utf8"))
    old_password = m.hexdigest()
    if old_password == current_user.password:
        n = hashlib.md5()
        n.update(new_password.encode("utf8"))
        new_password = n.hexdigest()
        User.query.filter_by(id=current_user.id).update({'password': new_password})
    else :
        flash('你的密码输入错误','edit_password')
    db.session.commit()
    return redirect('/contact')


@app.route('/edit_email/', methods={'get', 'post'})
def edit_email():
    email = request.values.get('email').strip()
    User.query.filter_by(id=current_user.id).update({'email': email})
    db.session.commit()
    return redirect('/contact')


@app.route('/edit_phone/', methods={'get', 'post'})
def edit_phone():
    phone = request.values.get('phone').strip()
    User.query.filter_by(id=current_user.id).update({'phone': phone})
    db.session.commit()
    return redirect('/contact')


@app.route('/edit_address/', methods={'get', 'post'})
def edit_address():
    address = request.values.get('address').strip()
    User.query.filter_by(id=current_user.id).update({'address': address})
    db.session.commit()
    return redirect('/contact')


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
    user = User(username, password, '男', '暂无电话', '暂无邮箱', '暂无收货地址，订单无效', '暂无收货地址，订单无效', '无')
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
