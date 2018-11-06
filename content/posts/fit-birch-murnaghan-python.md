+++
title = "Birch Murnaghan 状态方程拟合"
date = 2018-11-06
Description = ""
Categories = ["python"]
Tag = ["code", "eos", "science"]
+++

## 完整代码下载
[code](https://github.com/unkcpz/images/blob/master/zpcknu-blog/fit-bm-eos.py)

运行后生成下图：
![](https://github.com/unkcpz/images/blob/master/zpcknu-blog/fit-bm.png)


## 代码部分解释

### 拟合方程形式
```python
import numpy as np
def birch_murnaghan(V, E0, V0, B0, B01):
    r = (V0 / V) ** (2. / 3.)
    return E0 + 9. / 16. * B0 * V0 * (r - 1.) ** 2 * \
                (2. + (B01 - 4.) * (r - 1.))
```

### 拟合方程得到参数
```python
def fit_birch_murnaghan_params(volumes_, energies_):
    from scipy.optimize import curve_fit

    volumes = np.array(volumes_)
    energies = np.array(energies_)
    params, covariance = curve_fit(
        birch_murnaghan, xdata=volumes, ydata=energies,
        p0=(
            energies.min(),  # E0
            volumes.mean(),  # V0
            0.1,  # B0
            3.,  # B01
        ),
        sigma=None
    )
    return params, covariance
```

### 使用得到的参数插值做图
```python
    def plot_eos(volumes_, energies_):
        """
        Plots equation of state taking as input the pk of the ProcessCalculation
        printed at the beginning of the execution of run_eos_wf
        """
        import matplotlib.pyplot as plt

        volumes = np.array(volumes_)
        energies = np.array(energies_)

        params, covariance = fit_birch_murnaghan_params(volumes, energies)

        vmin = volumes.min()
        vmax = volumes.max()
        vrange = np.linspace(vmin, vmax, 300)

        plt.plot(volumes,energies,'o')
        plt.plot(vrange, birch_murnaghan(vrange, *params))

        plt.xlabel("Volume (ang^3)")
        # I take the last value in the list of units assuming units do not change
        plt.ylabel("Energy (eV)")
        plt.show()
```

### 调用

```python
awithe = np.array(
    [[0.95, -10.54342866],
    [0.96, -10.65937674],
    [0.97, -10.74563203],
    [0.98 , -10.80462694],
    [0.99, -10.83863631],
    [1.00 , -10.85001443],
    [1.01 , -10.84077847],
    [1.02, -10.81303532],
    [1.03, -10.76877249],
    [1.04, -10.70952633],
    [1.05 ,-10.63683672]])
a = [i[0] for i in awithe]
e = [i[1] for i in awithe]

volumes = [i**3 for i in a]
p, c = fit_birch_murnaghan_params(volumes, e)
print p, c

plot_eos(volumes, e)
```
