+++
title = "308集群：改建方案"
Description = "308集群的改建由于新加入一批计算资源，且原有管理方式分散，现计划实行改建，方便管理和使用。"
Tags = ["cluster", "system"]
Categories = ["manual"]
date = 2018-05-18
lastmod = 2018-05-22
+++

`$$\hat{H}\Psi = i \hbar \frac{\partial \psi}{\partial t}$$`

## 改建后的优点
- 对用户：
  1. 计算任务使用统一的脚本（slurm任务管理，当前最为流行）甚至与超算的使用方式相同，用户无需在不同的任
  务管理系统之间转换脚本。
  2. 资源按组分配，保证了每个用户的需求，增加了资源的使用率，减少了排队的等待时间。
  3. 若按照该计划实行，则组内几乎所有人的任务都能在组内所有的资源下进行，可减少超算的使用，节约了
  成本。
  4. 此时，超算的使用可将yjzhao和xbyang共10个用户分别分给指定使用者（一人一号），在确定计算方案后进行大项目的运算
  ，且方便统计使用率和投入产出比。
  5. 308集群改建后，超算上帐号可独立分配（一人一号），则用户配置因为用户的独立可以对当前使用的用户有最大的可调整和伸缩性。不会因为`~/.bashrc`的设置。
  造成原先可能出现的修改后其他软件无法正常使用的情况。
  6. matlab和python等长时间的计算任务通过与其他计算任务一样的方式管理，减少了用户对同一台机器使用
  的冲突，延长了机器的使用寿命。

- 对系统管理员：
  1. 方便管理
  2. 方便维护
  3. 方便统计
  4. 方便管理员的交接

## 改建前资源种类和数量
### 硬件情况
- 五舟：原28集群。cpu参数：Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz，内存128G。
共十个节点，每个节点20个核。
  - 当前有一个节点作为管理节点，机械硬盘10T。
  - 有一个节点有硬件问题，计算很慢，未查明原因。
- Dell R620: 原接入28的两台独立计算节点。Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz，内存64G
- Dell R610: 原16集群。cpu参数： Intel(R) Xeon(R) CPU E5645  @ 2.40GHz，内存32G
共十个节点，每个节点12个核。
  - 有一个节点内存故障，无法使用。
- Dell R620: 由景派提供的集群。Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz, 内存64G
共20个节点，每个节点12个核。
  - 有一个节点作为管理节点。硬盘600G.
- Dell R730: 现有作为matlab和独立任务的机器。Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz，内存128G
并有两块1TSSD硬盘做RAID。
  - 现该节点不接入任何集群，独立使用，无任务管理系统。
- Dell ?: 另外有一台储存原有16资料的管理节点，现在独立为储存用。
- Dell ?: 有一台故障机器，有大号的硬盘槽。
- PWMAT: 与pwmat软件共同购买的机器，有四个GeForce GTX 980，NVIDIA® Maxwell™ 架构。另外有12个核，参数？？

总计： 616xcpu & 4xGPU

当前以上机器除用于matlab或python等独立任务的机器，均需要关闭超线程。

### 平均计算能力描述
五舟的机器的计算速度平均到每个核
- 是Dell-R610的1.5到2倍/per core
- 是Dell-R620机器1.5倍/per core

### 系统和软件情况
- 原28集群和原16集群现通过五舟机器的一个节点作为管理节点，分别管理9个五舟的计算节点，2个dell R620
和10个dell R610. 所用系统为Rocks 6.1.1 内核版本2.6.32. 使用SGE作为任务管理系统。
- 景派提供的集群现在一个节点作为管理节点，管理其余19个计算节点。所用系统为CentOS-7.5, 内核版本3.10.0
搭配openHPC v1.3.4作为集群管理软件，使用Slurm作为任务管理系统。
- matlab服务器现有系统为CentOS-7.5,未装有集群管理和任务管理系统。
- PWMAT机器现有系统为CentOS-7.1，内核版本3.10.0, GPU编译器版本CUDA7.0。

## 改建后预期管理方式

### 硬件分配
管理节点，使用现有作为matlab和独立任务的节点作为管理节点，原因如下：

1. 该机器cpu主频低，不适于matlab和python等任务的计算
2. 该机器较新，且半年的使用确定机器稳定性很好。
3. 该机器的可拓展性好。

计算节点：

1. 五舟的机器共10个节点每个节点20个核，共200个核
2. Dell R620（包含原有两个节点和景派提供20个节点）共22个节点，每个节点12个核，共264个核
3. Dell R610，共10个节点，每个节点12个核，共120个核。
4. ？？？PWMAT机器是否作为计算节点接入？？？其使用GPU后的性能对大体系有10倍的速度提升。

储存设备：
使用统一的独立磁盘阵列，将用户数据储存在磁盘阵列中。保证原有28的10T容量4T资源和原有16的资源不动。做成RAID？？`/home`
现有运行matlab和独立任务的机器上的两块1TSSD做成RAID？？？`/`

### 改建后计算节点分组信息
#### 组内需求

1. 少核、小内存、短时间、多数量的任务，如小体系和高通亮，(yujs[周期], qiusb[二维], hecc[一维到三维], liaojh[周期], zhaoxy[搜索软件])
2. 多核、大内存、长时间、少数量的任务，如大体系和精细性质的计算，（tengq[optic-gap-defect], wangyp[gap-soc], wuyn[slab], tianry[defect]， luzw[defect]）
3. 其中soc和GW需要大内存的支持，<s>考虑将一个或两个五舟的计算节点增加RAM至256或512,否则需要合并多个节点才能满足内存需求（那么可能降低节点间信息交换的效率和浪费核的资源）</s>，可在超算上使用大内存节点，或者跨节点并行进行。

#### 根据需求的节点分组方案

1. 2个五舟节点分组`-p bigram`作为大内存节点，用于HSE+SOC和大内存需求的计算。WALLTIME=1month
2. 1个五舟节点分组`-p single`作为matlab和python等小型长时间独立任务节点，最高每人每次10个核
，WALLTIME=1month。<span stype="color:red">打开超线程</span>
3. 剩余7个五舟节点分组为`-p big`作为多核、长时间、少数量任务，大体系和精细性质的计算。最高每人每次40个核
，WALLTIME=2Weeks
4. 18个Dell R620分组为`-p small`作为少核、短时间、大数量任务，小体系（少于100个电子）和高通亮，或全局
搜索。<s>最高每人每次24个核，WALLTIME=1days</s>最高每人每次12个核，WALLTIME=3days。没有安装快速交换网络，跨节点并行没有明显的速度提升。
5. 4个Dell R620分组为`-p sfast`作为少核、短时间、大数量任务，小体系（少于100个电子）和高通亮，或全局
搜索。最高每人每次4个核，WALLTIME=12hours
6. 10个Dell-R610分组为`-p jp`，该项目主要供本科生使用。
人每次4个核，WALLTIME=7days
7. ？？？PWMAT机器如果接入统一管理，则用于超大体系（>100原子，K-mesh=4x4x4, 每电子布800s以上，或GW和
精细光学性质等）的长时间运算。速度可为普通cpu的10倍以上。

### 改建后软件信息

- 管理系统统一使用CentOS7.5 + openHPC-v1.3.4(xCat+Slurm)作为集群管理系统和软件。
- Intel的数学库和编译器当前使用最新且稳定的2017_update7版本，且规定每年年初更换为上一年的最稳定版本，
同时所有相关依赖软件重新编译。
- openmpi分别有gnu和intel编译的版本，版本号分别需要保持有1.10的稳定版本，和最新的稳定版本
（现在为3.1.0）
- ？？？如果PWMAT机器作为计算节点接入统一管理，使用最新的CUDA库和GPU支持的VASP和PWMAT和tensorflow。

## 改建后的优点
- 对用户：
  1. 计算任务使用统一的脚本（slurm任务管理，当前最为流行）甚至与超算的使用方式相同，用户无需在不同的任
  务管理系统之间转换脚本。
  2. 资源按组分配，保证了每个用户的需求，增加了资源的使用率，减少了排队的等待时间。
  3. 若按照该计划实行，则组内几乎所有人的任务都能在组内所有的资源下进行，可减少超算的使用，节约了
  成本。
  4. 此时，超算的使用可将yjzhao和xbyang共10个用户分别分给指定使用者（一人一号），在确定计算方案后进行大项目的运算
  ，且方便统计使用率和投入产出比。
  5. 308集群改建后，超算上帐号可独立分配（一人一号），则用户配置因为用户的独立可以对当前使用的用户有最大的可调整和伸缩性。不会因为`~/.bashrc`的设置。
  造成原先可能出现的修改后其他软件无法正常使用的情况。
  6. matlab和python等长时间的计算任务通过与其他计算任务一样的方式管理，减少了用户对同一台机器使用
  的冲突，延长了机器的使用寿命。

- 对系统管理员：
  1. 方便管理
  2. 方便维护
  3. 方便统计
  4. 方便管理员的交接

## 改建中可能出现的成本和困难

### 改建成本

- 一个独立储存阵列盒
- 修复存在问题的五舟机器
- <s>DellR620使用的快速交换网络</s>
- 更换原有16中Dell-R610中一台机器的损坏内存, 型号如下：

```text
Handle 0x110B, DMI type 17, 28 bytes
Memory Device
       Array Handle: 0x1000
       Error Information Handle: Not Provided
       Total Width: 72 bits
       Data Width: 64 bits
       Size: 4096 MB
       Form Factor: DIMM
       Set: 6
       Locator: DIMM_B3
       Bank Locator: Not Specified
       Type: DDR3
       Type Detail: Synchronous Registered (Buffered)
       Speed: 1333 MHz
       Manufacturer: 00AD00B380AD
       Serial Number: 03691E86
       Asset Tag: 01114461
       Part Number: HMT351R7BFR8A-H9  
       Rank: 2
```
<s>- 加大五舟两个节点作为大内存所需的内存条，增加到256G，型号如下：

```text
Handle 0x0030, DMI type 17, 34 bytes
Memory Device
        Array Handle: 0x0026
        Error Information Handle: Not Provided
        Total Width: 72 bits
        Data Width: 64 bits
        Size: 16384 MB
        Form Factor: DIMM
        Set: None
        Locator: P2_DIMMG1
        Bank Locator: Node1_Bank0
        Type: DDR3
        Type Detail: Registered (Buffered)
        Speed: 1333 MHz
        Manufacturer: Samsung           
        Serial Number: 97EF4A3D    
        Asset Tag: Dimm6_AssetTag
        Part Number: M393B2G70QH0-
        Rank: 1
        Configured Clock Speed: 1333 MHz

```
</s>


### 困难
储存问题：

- 现在308集群用户大都存放在五舟机器的现有管理节点上，共10块1T机械硬盘，共4.1T资源，且其分区方式诡异。
还有部分资料储存在原有16集群的管理节点上。
- 因此如何将这部分数据保持不损坏的情况下向独立阵列转移？
- 新版CentOS7.5使用xfs文件系统，而旧的Rocks6.1.1使用ext4文件系统，数据拷贝还是直接转移硬盘？
- 是否有必要做RAID？？

分区信息:
```text
[jsy@wz-hpc jsy]$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0 223.1G  0 disk
|-sda1   8:1    0  97.7G  0 part /
|-sda2   8:2    0  19.5G  0 part /var
|-sda3   8:3    0   9.8G  0 part [SWAP]
|-sda4   8:4    0     1K  0 part
`-sda5   8:5    0  96.1G  0 part /state/partition1
sdb      8:16   0   9.1T  0 disk
`-sdb1   8:17   0   9.1T  0 part /public
sr0     11:0    1  1024M  0 rom  
[jsy@wz-hpc jsy]$ df -h
Filesystem            Size  Used Avail Use% Mounted on
/dev/sda1              97G   19G   73G  21% /
tmpfs                  64G   84K   64G   1% /dev/shm
/dev/sda5              95G   79G   12G  88% /state/partition1
/dev/sda2              20G  2.6G   16G  15% /var
/dev/sdb1             9.0T  3.7T  4.9T  44% /public
tmpfs                  31G   79M   31G   1% /var/lib/ganglia/rrds
```

任务运行和数据备份问题：

- 改建期间，所有在运行的任务需要停止。改建会在暑假较少人使用时进行，改建时间预定为7天。
硬件和基础软件部署完成后，可以立刻保证VASP的使用。
- 改建后，所有的超算上的帐号密钥统一回收修改，需要在修改前让所有用户备份全部资料。修改后再统一合理
申请分配。

A：
以上问题需要服务方协助并提供合理的解决方案。

分区方案： --- Jason Yu

- `/`， `/boot`, `swap`, `/home`，`/opt/ohpc/pub` 均单独挂载。
- 其中`/home`放在独立阵列中。
- 其余分区挂载在SSD硬盘上。<span style="color:red">注意ssd挂载参数</span>
- 分区需求，在系统升级和重做时不会影响`/home`和已经安装的公有软件。

A: --- 景派科技

- 储存提前打包备份。
- 磁盘非差异化并不分散，且不需要大型文件系统。
- 独立阵列卡，做RAID
- 分区采用`xfs+lvm`或`btrfs`，有较好的灵活性和满足以上JY所提需求。

### 不确定性

`$$\Delta \chi \Delta \rho \geq \frac{\hbar}{2}$$`

- 根据使用需求，是否dell-R620 `-p small`分组的机器有必要使用快速交换网络，达到节点间的合理快速并行？

A： <s>有必要。有跨节点的需求。</s>
A： 没必要。没有跨节点的需求。--- Prof. Yang

## PS

jp提供的20个节点中有三个节点有16个核，且记得提醒其关闭超线程。
