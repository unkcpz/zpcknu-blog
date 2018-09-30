+++
title = "Tight binding 紧束缚模型"
Description = "紧束缚模型 （Tight binding） 模型的介绍"
Tags = ["model", "physics", "tight-binding"]
Categories = ["intro"]
date = 2018-09-30
+++

## 紧束缚模型

紧束缚模型(Tight binding)是计算周期性体系电子结构的一种方法。 它和原子轨道线性组合方法 (LCAO)
方法相似。即便这种近似方法忽略了电子-电子相互作用，它还是能够达到特定精度的结果，并且可作为其他
更为精确方法的出发点。

原胞中的波函数 `$\psi_{unit, cell}(\mathbf{r})$` 可以认为由晶胞中所有原子价轨道线性组合而成:

`$$\psi_{unit, cell}(\mathbf{r})=\displaystyle\sum_{a} \sum_{ao}c_{ao,a}\phi_{ao}^{Z_a}(\mathbf{r}-\mathbf{r_a})$$`

其中，`$a$`为对所有原子求和，`$ao$`为对所有原子轨道求和。上式可以被简写为对所有轨道求和:

`$$\psi_{unit, cell}(\mathbf{r})=\displaystyle\sum_i c_i \phi_i (\mathbf{r}-\mathbf{r_i})$$`

其中参数 `$c_i$` 可通过将波函数代入Schrödinger方程获得。比如，以 `$\mathrm{CaSO}_4$` 为例，
其价轨道分别为Ca原子的4s轨道，硫原子的3s轨道和3个3p轨道，氧原子的2s轨道和3个2p轨道。因此，
对于一份 `$\mathrm{CaSO}_4$` 共有 `$1+4+4\times 4=21$` 项波函数参数项，(`$i=1,\dots, 21$`)。

### 一维单原子晶体

### 一维双原子晶体

### 石墨烯 (Graphene)

### 锂 (bcc) 晶体
