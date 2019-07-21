import os,time

num=1
ret = os.fork()
if ret==0:      # sub-process do:
    num=num-1   # should be 0
    print("sub-process:%s,pid:%s,ppid:%s num:%s" % (ret,os.getpid(),os.getppid(),num))
else:           # main-process do:
    num=num+1   # should be 2
    print("main-process:%s,pid:%s,ppid:%s num:%s" % (ret,os.getpid(),os.getppid(),num))

time.sleep(3)

print('End')