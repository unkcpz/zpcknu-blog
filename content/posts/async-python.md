+++
title = "AsyncIO实现Python异步并发"
Description = "用asyncio库实现python中的IO并发"
Tags = ["asyncio", "python", "concurrency"]
Categories = ["python"]
date = 2019-04-24
+++

Python在3.6中正式将`async/await`作为关键字引入，文中代码均在python3.6中运行.

## 并行≠并发 进程≠线程≠协程

### 并行≠并发

推荐Golang作者Rob Pike 在Heroku's Waza 大会上的报告

- [Concurrency is not parallelism](https://blog.golang.org/concurrency-is-not-parallelism)
- [Video](http://www.youtube.com/watch?v=f6kdp27TYZs)
- [Slides](https://talks.golang.org/2012/concurrency.slide)

各种有趣和奇葩的解释见[zhihu并发](https://www.zhihu.com/question/33515481)

得票最多的答案如下：

> - 你吃饭吃到一半，电话来了，你一直到吃完了以后才去接，这就说明你不支持并发也不支持并行。
> - 你吃饭吃到一半，电话来了，你停了下来接了电话，接完后继续吃饭，这说明你支持并发。
> - 你吃饭吃到一半，电话来了，你一边打电话一边吃饭，这说明你支持并行。
>
> 并发的关键是你有处理多个任务的能力，不一定要同时。
> 并行的关键是你有同时处理多个任务的能力。
> 所以我认为它们最关键的点就是：是否是『同时』。

但是上述回答并没有很明确给出为什么在性能上并发对高IO的任务能够提升效率。

我们在上面回答的基础上做这样的拓展，首先做两个假设:

1. 你是单核的，因此不支持并行，所以没有办法边接电话边吃饭。这个假设也符合python在设计上的GIL。
2. 食物消化同样看作是一个独立的任务，该任务不能在吃饭的时候进行，而只能在饭后进行

不支持异步并发的程序中，吃饭和消化通常是写在同一个函数中，消化是在该函数的结尾处调用的。
消化的时候不能做任何其他的事情。
那么假设吃饭1小时，消化1小时，打电话1小时。完成整个事情需要1+1+1=3小时。

但是消化这个步骤依靠胃来进行，和你的大脑和其他机能无关。这样消化这个步骤就被类比成了一个IO操作，依赖于
比如网络或者读写的IO设备，而不占用cpu。将消化这个步骤包装成一个独立函数，则这个函数就叫做协程。
这个协程能够在进行其他任务（比如打电话）时进行。
那么完成整个事情需要1+1=2小时。

以上的假设还是有不完全正确的地方，就是吃饭和消化没有办法同时进行。
更进一步，如果把每一口食物的进食和每一口食物的笑话再分解成独立的函数（协程），
那么这时，吃饭和消化就可以同时进行。总时间还是2小时。

所以，从这个例子可以看出，作出异步特性的程序的一个关键是将程序中IO读写的部分尽可能划分成为粒度足够小的功能块。

### 进程≠线程≠协程

## 同步代码和异步代码对比

### 什么是异步？

我们来写一个简易版本的异步代码，并给出相应的同步代码作为对比。

- 异步版本(asynchronous version)

```python
#!/user/bin/env python3
# async.py
import asyncio

async def async_print():
  print("Hello")
  await asyncio.sleep(2)
  print("World")

async def main():
  await asyncio.gather(
    async_print(),
    async_print()
  )

if __name__ == "__main__":
  import time
  start = time.perf_counter()
  asyncio.run(main())
  elapsed = time.perf_counter() - start
  print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```

```shell
$ python3.6 async.py
Hello
Hello
World
World
async.py executed in 2.00 seconds.
```

- 同步版本(synchronous version)

```python
#!/usr/bin/env python3
# sync.py
import time

def sync_print():
  print("Hello")
  time.sleep(2)
  print("World")

def main():
  for _ in range(2):
    sync_print()

if __name__ == "__main__":
  start = time.perf_counter()
  main()
  elapsed = time.perf_counter() - start
  print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```

```shell
Hello
World
Hello
World
sync.py executed in 4.00 seconds.
```

从结果上，可以看到两个差别。1.时间上异步的代码用了2s，同步的代码用了4s，时间上同步是异步的两倍。
2.同步代码交替打印"Hello", "World",异步代码在该程序中先两次打印了"Hello", 再两次打印了"World".

时间上的差别是因为同步代码顺序执行了函数`sync_print()`两次，每次在执行到`time.sleep(2)`时程序停止在此处，
cpu等待该语句完成再执行。cpu的这个等待被称作阻塞(blocking)。
而在异步代码中，程序同样执行了函数`async_print()`两次，但与同步代码不同的是，在执行到`await asyncio.sleep(2)`时，
该函数在此处被挂起等待这条语句执行完毕后再返回执行后面的`print("World")`.
此处的`await asyncio.sleep(2)`模拟了一个耗时的IO操作，这种操作通常是因为网络IO或者文件的读写IO，通常可以同时进行。
cpu在这条语句挂起时没有停止运行，而是同时进行第二次的`async_print()`函数执行。
直到所有的IO操作都结束返回。

因此，虽然`await asyncio.sleep(2)`一样执行了两次，但这两次的执行是同时的，不涉及cpu的等待。因此总时间是2s而不是4s。

打印顺序的差别也是执行顺序的差别，在同步代码中，程序严格按照语句的顺序执行。因此先执行第一次`sync_print()`中的两次打印操作，
再执行第二次调用的两次打印操作。
然而在异步代码中，cpu直接在第一次sleep操作后转向第二次`async_print()`调用，执行了第二次的`print("Hello")`操作。
因此，先打印了"Hello"，再在sleep结束后打印了"World".

- 事件循环异步

在底层代码和库以及框架的编写中，更多使用事件循环来开启和监测各个异步操作。
事件循环的代码如下：
```python
#!/user/bin/env python3
# async_loop.py
import asyncio

async def async_print():
  print("Hello")
  await asyncio.sleep(2)
  print("World")

async def main():
  await asyncio.gather(
    async_print(),
    async_print()
  )

if __name__ == "__main__":
  import time

  loop = asyncio.get_event_loop()

  start = time.perf_counter()
  loop.run_until_complete(main())
  elapsed = time.perf_counter() - start
  print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```

结果与异步版本相同。

## 并发代码设计模式(Design Patterns)

### Chaining

### Queueing
