+++
title = "aiidalab部署的详细步骤"
Description = "详细描述如何在服务器上部署aiidalab"
Tags = ["aiidalab", "aiida"]
Categories = ["IT"]
date = 2020-08-20
+++

## 目的描述
本文详细描述使用aiidalab提供的[ansible playbook](https://github.com/aiidalab/ansible-playbook-aiidalab-server)
简便部署一个生产环境中安全可用的aiidalab。
其中JupyterHub的登陆方式为使用github账户验证登陆。最终的网页呈现在链接 https://aiidalab.paratera.com,
后续由paratera并行科技负责升级维护。该手册记录部署过程的详细步骤，以及中间可能遇见的问题，并在未来更新后续出现的
问题及其解决办法。

用于此次搭建测试的服务器由paratera并行科技提供，为阿里云的云服务器，配置如下：
```
CPU: 1*Intel(R) Xeon(R) Platinum 8269CY CPU @ 2.50GHz
RAM: 8G
disk: 40G
OS: ubuntu18.04LST
```

在实际生产过程，通常需要尽可能保证核数和aiidalab的用户数相同，硬盘保证每个aiidalab用户有10G的储存空间。
最终，希望搭建一个在大陆地区能够快速访问和使用的aiidalab，并支持连接使用paratera并行科技提供的计算资源（显然也能方便支持用户正在使用的其他资源）。

## 分布步骤

说明：由于部署工作需要同时设计本地机器工具的下载和使用，以及登陆远程服务器进行配置、部署以及测试，
因此为了方便时别需要在哪里操作，本地的操作会在开始前注释**在本地计算机（local）进行**；远端服务其的操作
同样会在开始前注释**在远端服务器（remote）进行**。

### 服务器端的准备步骤
在服务器上新建用户`aiidalab`并赋予其sudo权限。

**在远端服务器（remote）进行**。

```
# useradd -m -G sudo aiidalab
```

配置docker镜像至国内源，若使用aliyun，可参考 https://help.aliyun.com/document_detail/60750.html 获取并配置docker源。

### 下载aiidalab ansible playbook 并安装所需的部署工具
该小节内容均同aiidalab ansible playbook的[文档](https://github.com/aiidalab/ansible-playbook-aiidalab-server#ansible-playbook-for-aiida-lab-server)，请务必参考原文档，以免下面内容更新不及时。

**在本地计算机（local）进行**
```
git clone https://github.com/aiidalab/ansible-playbook-aiidalab-server.git
cd ansible-playbook-aiidalab
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

### 修改记录远程机器信息的hosts文件并运行playbook

**在本地计算机（local）进行**

修改当前ansible文件夹中 `hosts` 文件的IP以及私钥路进信息。

（该步与原文档不同）修改`playbook.yml` 文件中 `aiidalab_server_build_locally` 为开启状态。
并增加 `aiidalab_server_docker_stack: develop` 找到正确的docker stack的标签。
选择在远端手动构建docker容器。选择手动构建的主要原因是可以自定义docker容器内容（比如使用未发布的aiida_core版本），同时需要解决容器构建时的网络问题。

修改ansible role `geerlingguy.docker` 的任务中关于docker-compose安装时使用的地址。
即修改文件`ansible-playbook-aiidalab-server/roles/geerlingguy.docker/tasks/docker-compose.yml` 中 `Install Docker Compose` 步骤
的url为`https://get.daocloud.io/docker/compose/releases/download`。请参考 https://get.daocloud.io/ 获取关于镜像详细信息。

修改后的`playbook.yml`增加了以下内容：
```
aiidalab_server_build_locally: true
aiidalab_server_docker_stack: develop
```

运行playbook：
```
ansible-playbook playbook.yml --ask-become-pass
```

### 修改dockerfile并部署
**在远端服务器（remote）进行**

因为所需的`aiida_core`版本问题，以及docker容器安装时候的网络问题，需要进行以下修改：

- 将SSSP赝势库下载至本地，并拷贝进入容器
- 配置使用国内镜像的pypi源以及conda源
- 下载最新的openbabel conda安装包并使用离线安装
- 安装对应的未发布的`aiida_core` (aiidateam/aiida_core@develop).
- 安装对应的未合并的`aiidalab-widgets-base` (unkcpz/aiidalab-widgets-base@feature/ssh-by-priv-key)

以上修改的详细内容可以参考修改前好的[diff对比](https://gist.github.com/unkcpz/3c5ae907708f99bb861b54ff21eb03bd)

构建并运行docker容器，在`Dockerfile`做在的文件夹中执行：
```
docker build . -t aiidalab-docker-stack:latest
```

该过程需要比较长的时间。

### SSL/TLS证书

**在远端服务器（remote）进行**

我们选择使用 let's encrypt 的免费证书，以及其提供的证书工具 [certbot](https://certbot.eff.org/lets-encrypt/ubuntubionic-apache)。
选择对应的系统(ubuntu18.04-LTS)和服务器软件(apache)， 会弹出相应的配置方式。

配置后，编辑`/etc/apache2/sites-enabled/aiidalab-server.conf`开启443端口使用ssl，并将证书地址指向正确的文件夹。

### Use Github OAuth 验证用户

**在远端服务器（remote）进行**

首先进入 [GitHub OAuth application](https://github.com/settings/applications/new) 注册新的应用认证。
注册后可以在 `Settings>Developer>settings` 看见该应用认证。请记录以下内容并设置为jupyterhub启动时的环境变量。

编辑 `/etc/systemd/system/jupyterhub.service.d/override.conf` 并加入以下内容：
```
[Service]
Environment="OAUTH_CALLBACK_URL=https://aiidalab.paratera.com/hub/oauth_callback"
Environment="GITHUB_CLIENT_ID=×××"
Environment="GITHUB_CLIENT_SECRET=××××××××××××"
```
注意该文件的权限为 `0644` 除了用于开启jupyterhub服务的root用户，其他用户均不应该看到该文件内容：

```
$ sudo chmod 640 /etc/systemd/system/jupyterhub.service.d/override.conf
```

再修改`/etc/jupyterhub/jupyterhub_config.py`，在其中加入：

```
#===============================================================================                                        
from oauthenticator.github import GitHubOAuthenticator                                                                  
c.JupyterHub.authenticator_class = GitHubOAuthenticator                                                                 
c.GitHubOAuthenticator.create_users = True                                                                              

# c.GitHubOAuthenticator.whitelist = {'unkcpz', 'test'}                                                                 
c.GitHubOAuthenticator.admin_users = {'<admin_user>'}  
```

重新启动jupyterhub服务以及apache服务，载入新配置。

```
$ sudo service jupyterhub restart
$ sudo apachectl graceful
```

## 常见问题
