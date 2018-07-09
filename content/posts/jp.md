+++
title = "JP暂时服务器使用"
Description = "集群使用openHPC搭建，使用xCAT+slurm.系统采用CentOS7.5"
Tags = ["cluster", "system"]
Categories = ["manual"]
date = 2018-07-05
lastmod = 2018-07-05
+++

##

```bash
#!/bin/bash -l
# NOTE the -l flag!
#
#SBATCH -J bcNy-155839
# Default in slurm
#SBATCH --mail-user username@domain.tld
#SBATCH --mail-type=ALL
# Request 5 hours run time
#SBATCH -t 120:0:0
#SBATCH -A your_project_id_here
#
#SBATCH -p normal -N 1 -n 12
# NOTE Each Kalkyl node has eight cores
#

module load vasp/5.4.4-impi-mkl


cwd=`pwd`
dir="${cwd}/vasp_run"
vaspdir="/home/unkcpz/summer-BNC/BxNxCy/vasp"

for i in {14001..15839}
do
# echo "id$i DONE" >> log.txt
vrun_dir="${dir}/id$i"

if [ -f "$vrun_dir/static/POSCAR" ] && [ -f "$vrun_dir/static/INCAR" ] && \                                   
   [ -f "$vrun_dir/static/POTCAR" ] && [ -f "$vrun_dir/static/KPOINTS" ]; then                                
        cd "$vrun_dir/static"
        mpirun -n 12 vasp_std_noZ
        echo "id$i DONE" >> ${cwd}/log.txt
else
        echo "INPUT files for vasp run not all found in $vrun_dir/relax, \                                    
please check the directory."
fi
done
```
