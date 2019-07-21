#import mysql.connector as pymysql
import pymysql

conn=pymysql.connect(host="localhost",port=3316,user='root',password='123456',database='demo1')
cursor=conn.cursor()

try:
    # 执行SQL语句: drop
    cursor.execute('drop table if exists user')

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
    # 注：这里占位符是'%'，不是'?'
    cursor.execute('select * from user where id=%s', ('A-001',))
    records = cursor.fetchall()
    print(records)

finally:
    cursor.close()
    conn.close()


