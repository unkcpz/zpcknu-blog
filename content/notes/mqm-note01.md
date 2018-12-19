+++
title = "现代量子力学笔记(一): 实验和意念显现"
Tags = ["note", "physics", "quantum"]
Categories = ["note"]
date = 2018-12-18
draft = true
+++

## Stern-Gerlach 实验
这个实验直观表示出,一个原子尺度的系统会表现出量子的特性.这种所谓的量子的特性,
是与经典物理的直觉相违背的.

实验的装置如下:
![](https://upload.wikimedia.org/wikipedia/commons/e/ee/Stern-Gerlach_experiment_svg.svg)
(Wiki图)银原子经过特定方向的磁场,在探测设备上得到该银原子的落点; (1) furnace, (2) beam of silver atoms,
(3) inhomogeneous magnetic field, (4) classically expected result, (5) observed result

### 第一个和经典相违背的结果

在这个实验中,可以得到一个与经典直觉相违背的结果:发射出的银原子因为角动量的方向各异本应该在观测器上得到连续的落点(上图[4]),
但结果只观测到分立的两个落点(上图[5]).

这说明,出射的银原子的角动量不是如同经典所理解的有方向变化的是分立的,而是如所观测的离散的.

## Stern-Gerlach Sequential 实验
通过上面的实验,原子束会被分成分立的两束,通过串联这样的装置可以进行下面这样的实验:
![](https://upload.wikimedia.org/wikipedia/commons/3/35/Sg-seq.svg)

(top) 最上方的系统表示,经过分离z方向S-G装置(z-SG)粒子束被分成`$z_{-}$`和`$z_{+}$`两束,过滤掉`$z_{-}$`,
仅让`$z_{+}$`再次通过z-SG,仅仅得到`$z_{+}$`,`$z_{-}$`完全被过滤了.
这是直觉可以接受的.

(middle) 中间的系统表示,经过分离z方向S-G装置(z-SG)粒子数被分成`$z_{-}$`和`$z_{+}$`两束,过滤掉`$z_{-}$`,
仅让`$z_{+}$`通过分离x方向S-G装置 (*x-SG*),可以得到`$x_{-}$`和`$x_{+}$`.
x方向上的信息都有,这从直觉上也没什么问题.

(bottom) 同上方装置,但在最后又过滤了`$x_{-}$`直留下`$x_{+}$`经过后续的(*z-SG*).发现此时粒子束,
又被分成了`$z_{-}$`和`$z_{+}$`两束.
这是和直觉相违背的,已经被过滤干净的`$z_{-}$`怎么又在后面重新出现了呢?

### 第二个和经典相违背的结果
Stern-Gerlach Sequential实验的最后一个结果与经典直觉所理解的不同,为什么一个已经被过滤的信息有重新出现了呢?

这个例子在量子力学中被用来说明我们不能同时(simultaneously)确定z方向上的结果和x方向上的结果.
更详细的说就是,粒子束在进入一个x-SG装置后,其中z方向上的信息就被破坏了.

## Stern-Gerlach结果与经典光学的类比
上面的结果使我们想到经典光学中类似的情况:
