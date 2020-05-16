+++
title="GSoC Logs: plumpy"
date=2020-04-29
Tags=["GSoC", "AiiDA"]
Category=["Note"]
lastmod=2020-05-16
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

## May-16

#### The idea behind communicator and process event loop

The bird-view review is based on the discussion https://github.com/aiidateam/plumpy/pull/150#issuecomment-621705277

In this section, code related examples in plumpy package and aiida_core is given for clarification.
The processes are running at the event loop of what we call worker thread.
Theoretically, in asyncio context, one thread only has one event loop running, and
processes running in that event loop asynchronously, aka non-blocking. When one process
running to a step asynchronously, it is running and other control signals are
still able to send to and received from the running process.

The reason that process working this way is that the process in plum did not do
computational resource cost jobs, it just serves as a record and state machine
of processes. All steps running in the process are IO based actions.

The communicator provided by kiwi is used to control the plum process.
It's OK if one process blocks all the others for quite some time while it is in a step,
however it should not block communications with RabbitMQ because this may
result in RabbitMQ thinking that this client (and all its processes) have died.
Therefore, to get rid of this, the communicator should be run at a different
thread from the process one, and RmqThreadCommunicator provided in kiwi API
work for this purpose. However, this cause another question which the callback
is invoked in though the scheduler in the communicator lead to the callback function
therefore is running in the communicator's event loop. We need schedule this
callback task in the loop of process' worker thread. So I use `asyncio.run_coroutine_threadsafe`
to schedule it in the correct loop.

There are three kinds of controller case, one uses rpc subscriber to pause, play, and kill
the process. This rpc subscriber is added in the communicator when the process initialized.
Similarly, the broadcast subscriber is added when processes initialized. The broadcast subscriber
is used when we need pause, play, and kill process one command for all.
The task actions such as launch, execute and continue processes are invoked without
initialize the process. That means we have no subscriber with over threads scheduler.
The subscriber has to be added manually before the process initialized.

Let's see the code of plumpy and aiida_core. In plum, the action invoke callback
is scheduled by method `_schedule_rpc` of Process class. Therefore, when process
initialized and running in the even loop, it can be controlled by the process_controller
over thread communicator. While as for the task actions, aiida_core add this subscriber
with `ProcessLauncher` in method `create_daemon_runner` of `manager` class, right after
the runner is created. Corresponding to that, to testing this behavior in plum,
a `LoopCommunicator` is used to converting a callback being scheduled to the right thread.
It should be noticed that all thread transition procedure is done by `plumpy.futures.create_task`.

As summary, there are only to place where the code call `run_coroutine_threadsafe` to correctlly
schedule the callback to event loop. One in `_schedule_rpc` and one in `create_task`.
