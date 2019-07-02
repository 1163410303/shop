from shop import db, login_manager


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    sex = db.Column(db.String(10))
    phone = db.Column(db.String(80))
    email = db.Column(db.String(80))
    remark = db.Column(db.String(200))
    address = db.Column(db.String(80))
    head_url = db.Column(db.String(512))

    def __init__(self, username, password, sex, phone, email, remark, address, head_url):
        self.username = username
        self.password = password
        self.sex = sex
        self.phone = phone
        self.email = email
        self.remark = remark
        self.address = address
        self.head_url = head_url

    def __repr__(self):
        return '<User %d %s>' % (self.id, self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    content = db.Column(db.String(512))
    type_name = db.Column(db.String(80), db.ForeignKey('good_type.name'))
    purchase_price = db.Column(db.Float)
    trade_price = db.Column(db.Float)
    retail_price = db.Column(db.Float)
    good_url = db.Column(db.String(512))
    warehouse_name = db.Column(db.String(80), db.ForeignKey('warehouse.name'))
    images = db.relationship('Image', backref='good', lazy='dynamic')

    def __init__(self, name, quantity, content, type_name, purchase_price, trade_price, retail_price,  good_url, warehouse_name):
        self.name = name
        self.quantity = quantity
        self.content = content
        self.type_name = type_name
        self.purchase_price = purchase_price
        self.trade_price = trade_price
        self.retail_price = retail_price
        self.good_url = good_url
        self.warehouse_name = warehouse_name

    def __repr__(self):
        return '<Good %s %d %s>' % (self.name, self.quantity, self.content)


class GoodType(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    remark = db.Column(db.String(512))
    description = db.Column(db.String(512))

    def __init__(self, name, remark, description):
        self.name = name
        self.remark = remark
        self.description = description


    def __repr__(self):
        return '<GoodType %d %s>' % (self.id, self.name)


class InboundLoad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    type_name = db.Column(db.String(80), db.ForeignKey('good_type.name'))
    purchase_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    warehouse_name = db.Column(db.String(80), db.ForeignKey('warehouse.name'))
    date = db.Column(db.String(100))
    remark = db.Column(db.String(512))

    def __init__(self, name, type_name, purchase_price, quantity, warehouse_name, date, remark):
        self.name = name
        self.type_name = type_name
        self.purchase_price = purchase_price
        self.quantity = quantity
        self.warehouse_name = warehouse_name
        self.date = date
        self.remark = remark

    def __repr__(self):
        return '<InboundLoad %d %s>' % (self.id, self.name)

class outboudLoad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    type_name = db.Column(db.String(80), db.ForeignKey('good_type.name'))
    quantity = db.Column(db.Integer)
    warehouse_name = db.Column(db.String(80), db.ForeignKey('warehouse.name'))
    date = db.Column(db.String(100))
    remark = db.Column(db.String(512))

    def __init__(self, name, type_name, quantity, warehouse_name, date, remark):
        self.name = name
        self.type_name = type_name
        self.quantity = quantity
        self.warehouse_name = warehouse_name
        self.date = date
        self.remark = remark

    def __repr__(self):
        return '<outboudLoad %d %s>' % (self.id, self.name)

class warningLoad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    type_name = db.Column(db.String(80), db.ForeignKey('good_type.name'))
    warehouse_name = db.Column(db.String(80), db.ForeignKey('warehouse.name'))
    quantity = db.Column(db.Integer)
    remark = db.Column(db.String(512))

    def __init__(self, name, type_name, warehouse_name, quantity, remark):
        self.name = name
        self.type_name = type_name
        self.warehouse_name = warehouse_name
        self.quantity = quantity
        self.remark = remark

    def __repr__(self):
        return '<warningLoad %d %s>' % (self.id, self.name)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good_name = db.Column(db.String(80), db.ForeignKey('good.name'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    address = db.Column(db.String(80), db.ForeignKey('user.address'))
    date = db.Column(db.String(80))
    remark = db.Column(db.String(512))
    state = db.Column(db.String(20))
    gross_profit = db.Column(db.Integer)

    def __init__(self, good_id, good_name, quantity, price, username, address, date, remark, state,gross_profit):
        self.good_id = good_id
        self.good_name = good_name
        self.quantity = quantity
        self.price = price
        self.username = username
        self.address = address
        self.date= date
        self.remark = remark
        self.state = state
        self.gross_profit = gross_profit

    def __repr__(self):
        return '<warningLoad %d %s>' % (self.id, self.state)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    remark = db.Column(db.String(512))

    def __init__(self, name, address, remark):
        self.name = name
        self.address = address
        self.remark = remark

    def __repr__(self):
        return '<Warehouse %d %s>' % (self.id, self.state)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    istitle = db.Column(db.Integer)

    def __init__(self, url, good_id, istitle):
        self.url = url
        self.good_id = good_id
        self.istitle = istitle

    def __repr__(self):
        return '<Image%d %s>' % (self.id, self.url)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    quantity = db.Column(db.Integer)

    def __init__(self, user_id, good_id, quantity):
        self.user_id = user_id
        self.good_id = good_id
        self.quantity = quantity

    def __repr__(self):
        return '<Cart 的用户id为%d 商品id为%d 数量为%d>' % (self.user_id, self.good_id, self.quantity)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
