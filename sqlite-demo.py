import sqlite3
import os

# delte test.db
db_file = os.path.join(os.path.dirname(__file__), 'test.db')
if os.path.isfile(db_file):
    os.remove(db_file)


conn = sqlite3.connect('test.db')   # 建立连接（数据库文件不存在时，会创建）
cursor = conn.cursor()              # 创建并打开一个Cursor

try:
    # 执行SQL语句: create
    cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')

    # 执行SQL语句: insert
    cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
    print(cursor.rowcount)

    cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
    print(cursor.rowcount)

    cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
    print(cursor.rowcount)
    
    # 提交事务
    conn.commit()

    # 执行SQL语句: select
    cursor.execute('select * from user where id=?', ('A-001',))
    records = cursor.fetchall()
    print(records)

finally:
    cursor.close()                  # 关闭Cursor
    conn.close()                    # 关闭连接


    