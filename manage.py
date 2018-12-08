

from shop import app, db
from flask_script import Manager
from shop.models import User, Good, GoodType

manager = Manager(app)


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('切格瓦拉' + str(i), 'password' + str(i)))
    db.session.add(GoodType('肉类', '来自西藏', '西藏的牛肉，可好吃了'))
    db.session.add(GoodType('手工礼品', '刚到货', '精美手工礼品，新颖，好玩'))
    db.session.add(GoodType('成人用品', '杜蕾斯', '用不破的杜蕾斯哦'))
    db.session.add(GoodType('电子产品', '索尼大法好', '索尼新款ps 为你的信仰充值'))

    db.session.add(Good('山羊肉', 888, '进口山羊肉，吃屎长大的山羊', '肉类'))
    db.session.add(Good('杜蕾斯', 9999, '用不破的杜蕾斯，干不坏的女朋友', '成人用品'))

    db.session.commit()


if __name__ == '__main__':
    manager.run()
