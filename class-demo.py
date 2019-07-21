# -*- coding:utf-8 -*-

class Cat:
    name='cls_cat'

    def __init__(self):
        self.name='self_cat'

    def eat(self):                      # 实例方法
        print('%s is eating' % self.name)

    @classmethod
    def from_setting(cls):              # 类方法
        # 修改类属性
        cls.name='cls_cat_fresh'
        
        # 添加类方法（第一个参数代表类）
        @classmethod
        def say_cls(x,y):
            return "%s say %s" % (x.name,y)
        cls.say_cls=say_cls
        
        # 添加实例方法（第一个参数代表实例）
        cls.say_self=lambda x,y:"%s say %s" % (x.name,y)

    @staticmethod                       # 静态方法
    def play():
        print("%s is playing" % Cat.name)


c=Cat()

Cat.name    # 'cls_cat'
c.name      # 'self_cat'

Cat.play()  # cls_cat is playing
c.play()    # cls_cat is playing

Cat.from_setting()  # or use: c.from_setting()

Cat.name    # 'cls_cat_fresh'
c.name      # 'self_cat'


Cat.say_cls('Hello')    # or use: c.say_cls('Hello') => 'cls_cat_fresh say Hello'
c.say_self('Hello')   # 'self_cat say Hello'


