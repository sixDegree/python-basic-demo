from twisted.internet import reactor    # 事件循环（自动终止条件：所有socket都已移除）
from twisted.internet import defer      # defer.Deferred 特殊的socket对象（需手动调用执行，手动移除）
from twisted.internet import task

import treq  # 用于发送异步Request，返回Deferred对象
import time


# 延迟机制：
# Deferred 延迟对象，代表的是一个无法立即获取的值

def demo_defer1():
    d = defer.Deferred()
    print("called:", d.called)  # False

    print("call...")
    d.callback("Hello")
    print("called:", d.called)  # True
    print("result:", d.result)  # Hello


def demo_defer2():
    def done(v):
        print("done called")
        return "Hello " + v

    d = defer.Deferred()
    d.addCallback(done)
    print("called:", d.called)  # False

    print("call...")
    d.callback("Tom")
    print("called:", d.called)  # True
    print("result:", d.result)  # Hello Tom


def demo_defer3():
    def status(*ds):
        return [(getattr(d, 'result', 'N/A'), len(d.callbacks)) for d in ds]

    def b_callback(arg):
        print("b_callback called with arg =", arg)
        return b

    def on_done(arg):
        print("on_done called with arg =", arg)
        return arg

    a = defer.Deferred()
    b = defer.Deferred()

    a.addCallback(b_callback).addCallback(on_done)
    print(status(a, b))  # [('N/A', 2), ('N/A', 0)]

    a.callback(3)  # b_callback called with arg = 3
    print(status(a, b))  # [(<Deferred at 0x1047a0da0>, 1), ('N/A', 1)]

    b.callback(4)  # on_done called with arg = 4
    print(status(a, b))  # [(4, 0), (None, 0)]


def demo_defer4():
    def status(*ds):
        return [(getattr(d, 'result', 'N/A'), len(d.callbacks)) for d in ds]

    def b_callback(arg):
        print("b_callback called with arg =", arg)
        return b

    def on_done(arg):
        print("on_done called with arg =", arg)
        return arg

    a = defer.Deferred()
    b = defer.Deferred()

    a.addCallback(b_callback).addCallback(on_done)
    print(status(a, b))  # [('N/A', 2), ('N/A', 0)]

    b.callback(4)
    print(status(a, b))  # [('N/A', 2), (4, 0)]

    a.callback(3)  # b_callback called with arg = 3
    # on_done called with arg = 4
    print(status(a, b))  # [(4, 0), (None, 0)]


def demo_defer5():
    def on_done(arg):
        print("on_done called with arg =", arg)
        return arg

    dfds = [defer.Deferred() for i in range(5)]
    defer.DeferredList(dfds).addCallback(on_done)
    for i in range(5):
        dfds[i].callback(i)
    # on_done called with arg = [(True, 0), (True, 1), (True, 2), (True, 3), (True, 4)]
    # on_done 要等到列表中所有延迟都触发(调用`callback(...)`)后调用


def demo_reactor1():
    def done(arg):
        print("Done", arg)

    def defer_task():
        print("Start")
        d = defer.Deferred()
        time.sleep(3)
        d.callback("123")
        return d

    def stop():
        reactor.stop()

    defer_task().addCallback(done)
    reactor.callLater(0, stop)
    reactor.run()


def demo_reactor2():
    def done(arg):
        print("Done", arg)

    def all_done(arg):
        print("All done", arg)

    def defer_task(i):
        print("Start", i)
        d = defer.Deferred()
        d.addCallback(done)
        time.sleep(2)
        d.callback(i)
        return d

    def stop():
        print("Stop reactor")
        reactor.stop()

    dfds = defer.DeferredList([defer_task(i) for i in range(5)])

    dfds.addCallback(all_done)
    reactor.callLater(0, stop)

    reactor.run()


def demo_reactor3():
    def done(arg):
        print("Done", arg)

    def all_done(arg):
        print("All done", arg)
        print("Stop reactor")
        reactor.stop()

    def defer_task(i):
        print("Start", i)
        return task.deferLater(reactor, 2, done, i)

    dfds = defer.DeferredList([defer_task(i) for i in range(5)])
    dfds.addBoth(all_done)

    # dfds.addCallback(all_done)
    # reactor.callLater(5, stop)

    reactor.run()


def demo_treq_get(url):
    def get_done(response):
        print("get response:", response)
        reactor.stop()

    treq.get(url).addCallback(get_done)
    reactor.run()


def main():
    @defer.inlineCallbacks
    def my_task1():
        print("Start task1")
        url = "http://www.baidu.com"
        d = treq.get(url.encode('utf-8'))
        d.addCallback(parse)
        yield d

    def my_task2():
        print("Start task2")
        return task.deferLater(reactor, 2, parse, "200")

    @defer.inlineCallbacks  # need use `yield`
    def my_task3():
        print("Start task3")
        yield task.deferLater(reactor, 2, parse, "400")

    def parse(response):
        print("parse response:", response)

    def all_done(arg):
        print("All done", arg)
        reactor.stop()

    dfds = defer.DeferredList([my_task1(), my_task2(), my_task3(), ])
    dfds.addBoth(all_done)
    reactor.run()


if __name__ == "__main__":
    # demo_defer1()
    # demo_defer2()
    # demo_defer3()
    # demo_defer4()
    # demo_defer5()

    # demo_reactor1()
    # demo_reactor2()
    # demo_reactor3()

    # demo_treq_get('http://www.baidu.com')
    
    main()
