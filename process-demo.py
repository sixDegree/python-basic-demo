from multiprocessing import Process
import multiprocessing
import os,time,random

# 法一
def task(name):
    print("子进程(%s) task %s start" % (os.getpid(),name))
    time.sleep(random.random()*2)
    print("子进程(%s) task %s end" % (os.getpid(),name))

# 法二
class MyProcess(Process):
    def __init__(self,name):
        Process.__init__(self)
        self.name=name

    def run(self):
        print("子进程(%s) task %s start" % (os.getpid(),self.name))
        time.sleep(random.random()*2) 
        print("子进程(%s) task %s end" % (os.getpid(),self.name))

if __name__=='__main__':
    print('CPU Count:',multiprocessing.cpu_count())
    print('父进程(%s) 开始' % os.getpid())

    # p = Process(target=task, args=('test',))   # 创建子进程，法一：创建一个Process实例
    p = MyProcess('test')                       # 创建子进程，法二：创建一个自定义的继承自Process类的实例

    p.start()   # 启动子进程
    p.join()    # 父进程阻塞等待子进程结束后再继续往下运行,非必需
    print('子进程(%s) 结束' % p.name)
    print('父进程(%s) 结束' % os.getpid())
