+++
title = "git中使用rebase和amend整理提交记录"
Description = "git's rebase and amend. how to use."
Tags = ["git"]
Categories = ["system"]
date = 2019-05-30
+++

## Why and When to use `rebase` and `amend`?
首先假设读者已经会使用基础的`add` `commit` `push` `pull` `fetch` 等命令来版本管理一个
软件仓库。
如果没有遇到协作开发时，无论整个版本如何管理，即使再混乱也不会引起大的问题。
但是在多人协作开发时，或者同在如github,gitlab这样的地方协作维护一个开源代码，
那么你就应该尽量规范你的每次提交，也就是在push之前反复确认，以保证当前这个push所包含的所有
commit记录都是有用且清晰的。

### `amend`: 重置commit信息
这会发生在两种情况中，第一种情况是当你的`commit -m`后面所写入的信息有错误时，你可能想要修改
这个写错的信息。第二种情况是，当你反复进行一些细小的修改后又不想在log中留下一长串的commit记录。

这时你会用到：

```bash
$ git commit --amend
```

该命令会打开编辑器，第一行显示你上一次的commit的信息。如果有错误，修改错误后保存（情况一）。如果是在
缓冲区中add进新的修改，则这个commit会加入这些新的修改（情况二），而不产生新的新的commit记录。

### `rebase`：整理以往`commit`记录

这里仅仅介绍rebase的squash功能。

你已经多次commit多个不同的修改，比如你的log如下：

```text
commit 5350734970c1da481de7274b690042c6465c433b (HEAD -> covtest-local)
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:28:32 2019 +0800

    edit a

commit 71924b4ccb39aae9a37a8c2c21fc6c2186c58fe8
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:28:23 2019 +0800

    edit a

commit 3c5e541f9cf456ba4d10d500899657037fb036a3
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:28:15 2019 +0800

    edit a

commit 2adf28f5e0e379895fc8edcfcb2b2d709f4867b4
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:27:23 2019 +0800

    add c

commit e9d2a252f8cfccf59f3063754e8a8729c54aa517
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:27:12 2019 +0800

    add b

commit b11b3d3d0dad46719cb91d7ad73797fd0866396d
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:26:56 2019 +0800

    add a

commit b04f6529f14afa95b8e7df420f62f75285409ae7 (origin/covtest-local)
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Sat May 11 00:23:51 2019 +0800

    Release v1.0.2
    concurrency bugfix..

```

其中最新的六次commit事实上都是一些简单的修改，你认为没有必要分成这么多条记录。所以你希望把版本
流变为下列形式(合并1～3与4～6)：

```text
commit f68f23a4c8c613a8ece39b362c9c241fc0a82b7f (HEAD -> covtest-local)
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:28:15 2019 +0800

    edit a

commit b2ad3048b94b2844b90db738219e804163ec2b1b
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Thu May 30 13:26:56 2019 +0800

    add a, b, c

commit b04f6529f14afa95b8e7df420f62f75285409ae7 (origin/covtest-local)
Author: Jason Eu <morty.yu@yahoo.com>
Date:   Sat May 11 00:23:51 2019 +0800

    Release v1.0.2
    concurrency bugfix..

```

这时用到的就是`rebase`，用于整理向前回溯的多个记录。

这个例子中，我们希望把到从记录`HEAD`到`b04f6529f14afa95b8e7df4` 之间的六条进行合并。
用到命令：

```bash
$ git rebase -i b04f6529f14afa95b8e7df4
```

或者
```bash
$ git rebase -i HEAD~6
```

这时同样会打开git默认编辑器（默认编辑器的设置[参考这里](https://stackoverflow.com/questions/2596805/how-do-i-make-git-use-the-editor-of-my-choice-for-commits)）.

每条记录之前的单词表示要对该条记录所作的操作，

- pick：表示保留这条记录
- s: 用于将这条记录向上合并
- <...>

在这个例子中，我们作如下编辑：

```text
pick add a
s add b
s add c
pick edit a
s edit a
s edit a
```

保存退出后会对每一个pick进行一次commit信息的编写，前三条合并为 `add a, b, c`,
后面三条则简化为 `edit a`

保存退出后就会得到如上所示的新的结果。

如果你已经将之前的结果push到远端仓库中，则这时你需要用`git push -f` 来覆盖之前的commit记录。
## 总结

在pull request之前尽量管理好自己的commit记录，保证记录的清晰有用。请频繁使用`--amend` 和 `rebase`
