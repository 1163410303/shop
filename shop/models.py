from shop import db, login_manager


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    head_url = db.Column(db.String(512))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.head_url = 'https://raw.githubusercontent.com/1163410303/1163410303.github.io/master/images/insert_image3.jpg'

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
    name = db.Column(db.String(80), unique=True)
    quantity = db.Column(db.Integer)
    content = db.Column(db.String(512))
    type_name = db.Column(db.String(80), db.ForeignKey('good_type.name'))

    def __init__(self, name, quantity, content, type_name):
        self.name = name
        self.quantity = quantity
        self.content = content
        self.type_name = type_name

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
