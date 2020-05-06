+++
title="GSoC Logs: plumpy"
date=2020-04-29
Tags=["GSoC", "AiiDA"]
Category=["Note"]
+++

## Description
This page contains logs about difficulties and short details of each PR in plumpy
migration part of project. Each sections are tagged by date, include the short descriptions
of the PR or the difficulties I faced in the project.

## 28th-April
The first [PR](https://github.com/aiidateam/plumpy/pull/151) which attempt to drops all the
py2 dependencies.

I did it with first remove all `six` package dependencies and all `from __future__` clause.
As tutor [suggested](https://github.com/aiidateam/plumpy/pull/151#pullrequestreview-401765724),
there are following codes also need to be modified to give up compatible
with py2:

- Classes without parent other than `object` do not need to be inherited from `object` anymore,
i.e. change  `class Sub(object):` to `class Sub:`
- `types.SimpleNamespace` is built in py3, therefore no need to implement it by ourselves.
- Get rid of `SavableFuture._tb_logger` in `plumpy.persistence.py` and related functionality

#### What is `types.SimpleNamespace`?
`types.SimpleNamespace` is just a simple `object` subclass but provides attriute access to
its namespace.
It has no much different from `class NS: pass` but more versatile.
This provides the following advantages over an empty class[^simpleNamespace]:
- It allows you to initialize attributes while constructing the object: sn = SimpleNamespace(a=1, b=2)
- It provides a readable repr(): eval(repr(sn)) == sn
- It overrides the default comparison. Instead of comparing by id(), it compares attribute values instead.

[^simpleNamespace]: https://stackoverflow.com/questions/37161275/what-is-the-difference-between-simplenamespace-and-empty-class-definition

#### Can not get rid of `SavableFuture._tb_logger`
The class `SavableFuture` is inherited from `tornado.concurrent.Future`
The `_tb_logger` still be used in tornado's Future. So It can only be
get rid of after remove the need of tornado Future.
