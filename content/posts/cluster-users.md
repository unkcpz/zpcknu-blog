+++
title = "308集群：用户手册"
Description = ""
Tags = ["cluster", "system"]
Categories = ["manual"]
date = 2018-04-28
+++

## 集群描述

### 集群名称
- 原先16的10个节点全部接入原先的28统一管理，所以不再以16和28称呼，集群名称现在
为''2816''或者叫做''集群''
- 现有的用作matlab和python单独计算的机器就叫暂时称作"matlab服务器"
- `pwmat`计算机器称作''pwmat''
- 原先的16登陆节点还存放有一些数据和vasp赝势，称作''16储存''

### 集群IP
```
2816:
    IP = 202.38.220.11, Port = 22

matlab服务器:
    IP = 202.38.220.11, Port = 7001

16储存:
    IP = 202.38.220.11, Port = 7002

pwmat:
    IP = 202.38.220.14, Port = 22
```

### 集群信息和性能
* 2816
  * compute-0-0到compute-0-8共9个节点每个节点20cores，每个核：Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz
  * compute-0-9到compute-0-19共10个节点每个节点12cores，每个核： Intel(R) Xeon(R) CPU E5645  @ 2.40GHz

## 脚本模板

## 任务管理系统`SGE`使用

## `module`软件模块挂载

## 并行环境（`mpi`）描述
