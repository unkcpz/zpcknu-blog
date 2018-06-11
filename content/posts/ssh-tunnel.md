+++
title = "ssh端口转发实现内外网穿透"
Description = "ssh端口转发，实现对内网机器的访问，和从外网访问内网机器。"
Tags = ["system", "ssh"]
Categories = ["manual"]
date = 2018-06-07
lastmod = 2018-06-07
+++

## 正向转发(Local forwarding)

正向转发用于向更深层的内网实现访问。举例如下：

首先来看一张网络拓扑。
![](/images/ssh-in.png)

当前的情况是，我的电脑可以通过ssh xxx.xxx.220.11登陆叫做28的机器，但不能直接ssh登陆到叫做16的服务器，
原因是16在28的子网。

然而，如果首先登陆28,是可以从28登陆到16的，因为他们同时位于10.1.xxx.xxx/16的子网段。

<span style="color:red">那么，我们怎样让我们的PC可以直接登陆到16呢？这里就要使用到ssh端口转发中的本地端口转发。</span>

直接来看解决办法：
登陆到名为28的服务器，执行
```sh
ssh -C -f -N -g -L 7002:10.1.255.101:22 unkcpz@localhost
```
这样就通过28完成了从PC到16的隧道穿越。
要直接访问16服务器，可以直接通过28的`7002`端口直接访问，如
```sh
ssh username@xxx.xxx.220.11 -p 7002
```

### For administration
下面来解释执行语句中各个参数的含义。
```sh
ssh -C -f -N -g -L 7002:10.1.255.101:22 unkcpz@localhost
```
详情请参考 [ssh-official](https://www.ssh.com/ssh/tunneling/example)和
[ibm-ssh中文](https://www.ibm.com/developerworks/cn/linux/l-cn-sshforward/)
```text
-L 本地转发 （这个参数在实现向内网穿透中最重要，下面会看到远程转发的例子）
-f 后台启用
-N 不打开远程shell，处于等待状态（不加-N则直接登录进去）
-g 启用网关功能 （Allows remote hosts to connect to local forwarded ports. ）
-C 压缩信息 (option has to do with compression)
```


## 反向转发(Remote forwarding)

反向转发也叫远程转发，同样用于向内网的穿透，但此时的情形与上面不同，此时客户端机器PC和内网机器
均能够访问外网，但是外网却无法通过内网机器的IP访问内网机器。

我们来看这个情形下的网络拓扑。
![](/images/ssh-out.png)

家中的电脑可以访问外网，名为28的服务器同样可以访问外网。那么要如何在家中的PC上访问28服务器呢？

首先，你需要有一台外网上购买的服务器，我们称这台为buy。
