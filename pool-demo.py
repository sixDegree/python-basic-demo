from multiprocessing import Pool
import os,time,random
import sys

def task(name):
    print("子进程(%s): task %s => start" % (os.getpid(),name))
    t=random.random()*2
    time.sleep(t) 
    print("子进程(%s): task %s => end(sleep:%.2f)" % (os.getpid(),name,t))
    return os.getpid(),name

def task_callback(arg):         # 父进程中执行，以元组方式获取task return值
    print("父进程(%s): 获取子进程(%s) task %s => callback" % (os.getpid(),arg[0],arg[1]))

if __name__=='__main__':
    print('父进程(%s): => 开始' % os.getpid())

    p=Pool(3)
    for i in range(0,5):
        #p.apply(task,(i,))      # 阻塞方式发配任务(等一个任务完成后，再发布下一个)
        p.apply_async(task,(i,),callback=task_callback)  # 非阻塞方式发配任务（一次性发布3个，等空出进程后，再发布下一）
   
    p.close()   # 关闭进程池，是以不再接收新的请求
    p.join()    # 父进程阻塞等待所有子进程执行完成，必须放在close语句之后（不加join的话可能子进程还未完成就整个退出了）
    print('所有子进程结束')
    print('父进程(%s): => 结束' % os.getpid())