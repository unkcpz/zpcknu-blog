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
  * compute-0-0到compute-0-8共9个节点每个节点:20cores，cpu参数：Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz，内存128G
  * compute-0-9到compute-0-19共10个节点每个节点:12cores，cpu参数： Intel(R) Xeon(R) CPU E5645  @ 2.40GHz，内存32G
* matlab服务器
  * 一个计算节点:20cores, cpu参数：Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
* pwmat
  * 4×GPU，单GPU参数：
  * 16×cpu，单cpu参数：

## 任务管理系统`SGE`使用

### `SGE`现有环境描述

现在共有三种队列

1. `big.q`： 使用的节点为compute-0-0到compute-0-7，内存大，cpu性能好，为对速度需求高且有大
    内存需求的计算任务使用
2. `med.q`： 使用的节点为compute-1-0到compute-1-5，性能一般，允许跨节点并行，性能稳定，为长时间计算的任务准备。
3. `small.q`：使用的节点为compute-2-0到compute-2-3，性能一般，小型体系和短时间任务所用，不可使用多余单个节点的核数。
4. `big_split.q`：使用节点为compute-3-0，cpu性能好，为小体系需要快速完成的任务准备（如高通量和搜索软件），
    该队列不可以设置核数大于4的单个任务。

### `qsub`使用和参数
* `-pe <arg1> <arg2>`： parellel environment
  * <arg1> 第一个参数为所使用的并行环境，统一后2816机器只有一个环境为`mpi`。
  * <arg2> 第二个参数为计算所使用的核数，根据用户需求指定。
* `-q <arg>`： 指定队列
  * <arg> 该参数指定所用的计算队列。

### `SGE`脚本模板
```bash
#!/bin/bash     
#$ -S /bin/sh
#$ -cwd            
#$ -V            
#$ -N out
#$ -pe mpi 12
#$ -q med.q
#$ -j y

module load vasp/5.4.4-impi-mkl15

mpirun -n ${NSLOTS} vasp_std
```
脚本同正常脚本所用的`sh`为第二行所用的`sh`
在工作目录中写入该文件，保存名称如`job.sh`,在命令行中运行以下命令即可提交认为到节点。
<span style="color:red">*请根据任务的需求认真确定和选择`-pe`和`-q`两个参数!!!*</span>

```sh
$ qsub job.sh
```

<span style="color:red">*若要提交任务到指定节点，或交互式运行任务，请参考管理员手册，或直接咨询管理员。*</span>

### `qrsh`使用

参数基本同`qsub`

功能为申请指定节点。

## `module`软件模块挂载


## 并行环境（`mpi`）描述
