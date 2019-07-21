from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. 创建对象的基类:
Base = declarative_base()

# 2. 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    score = Column(Integer)

# 3. 连接数据库:
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3316/demo1')
DBSession = sessionmaker(bind=engine)

# 4. 创建session
session = DBSession()

# 5. 操作

# delete:
print('1. delete...')
session.execute('delete from user')
session.commit()


# insert:
print('2. insert...')
session.add(User(id='A-001', name='Adam', score=95))
session.add(User(id='A-002', name='Bart', score=62))
session.add(User(id='A-003', name='Lisa', score=78))
session.commit()

# select
print("3. select...")
user = session.query(User).filter(User.id=='A-002').one()
print('type:', type(user))
print('name:', user.name)
print('score:',user.score)

# 6. 关闭session
session.close()

print('Done!')


