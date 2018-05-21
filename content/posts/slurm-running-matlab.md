+++
title = "使用slurm在集群上使用matlab"
Description = "在集群上使用slurm任务管理系统，分别交互式的和提交任务式的使用matlab"
Tags = ["cluster", "matlab"]
Categories = ["manual"]
date = 2018-05-21
lastmod = 2018-05-21
+++

## 以任务的方式提交matlab任务(recommoned)

<span style="color:red">切记在要运行的 `.m` 文件的结尾加入 `quit`， 否则在任务结束后无法释放节点。</span>

slurm脚本模板为`matlab_job.sh`：
```sh
#!/bin/bash -l
# NOTE the -l flag!
#
#SBATCH -J test
#SBATCH -o test.output
#SBATCH -e test.error.output
# Default in slurm
# Request 5 hours run time
#SBATCH -t 5:0:0
# Requiest 1 node and 4 cores in partition normal
#SBATCH -p normal -N 1 -n 4
# NOTE Each node has 12 cores

module load matlab/R2016b

matlab -nodisplay -nosplash -nojvm -singleCompThread -r script.m
```
其中前三个参数`-nodisplay`, `-nosplash`, `-nojvm`保证了在命令行中而不是用图形界面执行matlab。
`-singleCompThread`参数为程序中有并行代码时使用，确保了每个核不会多线程运行。由于matlab的
多维度编程的性能提升很大，在大的矩阵操作时可将此参数关闭，来实现多线程。

参数`-r`后面紧跟所要运行的`.m`文件。

将脚本与要执行的`.m`文件放在相同文件夹下，运行`sbatch ./matlab_job.sh`即可。

## 交互式的申请节点并进行matlab运算(not recommoned)

<span style="color:red">两次\<ctrl+D\>: 切记在运行完交互式任务后手动退出计算节点，退出计算节点后还要退出子命令行，否则节点持续被占用。</span>

### Step 1
首先使用`salloc -p normal -N 1 -n 4`申请normal分区下1个节点4个核。
此时，会打开一个新的shell窗口。

用`squeue`查看申请到的是哪个节点，记住节点名称比如`cn16`，使用`ssh cn16`进入该计算节点。

### Step 2
`module load matlab/R2016b`
加载mablab可执行模块的到路径。

### Step 3
运行`matlab -nodisplay -nosplash -nojvm`打开命令行模式的matlab。
