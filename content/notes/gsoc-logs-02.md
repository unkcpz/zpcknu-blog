+++
title="GSoC Logs: aiida_core"
date=2020-05-06
Tags=["GSoC", "AiiDA"]
Category=["Note"]
lastmod=2020-05-06
+++

## Description
Here I record the logs of exploring, changing of aiida_core code base.
The post is organized in date.

## May-06

#### The project entry point
I explore the code base of aiida_core, to decide where to kick off gsoc project.
There are lots of code involved with tornado, and I divide them into two categories.

1. The code interact with `plum`
2. The component that need asynchronous supported natually, e.g. `aiida/engine/transports.py`

The second one could be the good starting point.

The transports is a component in aiida_core used for handle the connection with
to the client machine. In principle, it may cost some time to open the link to
the computer, therefore it should not be blocked. That is why asynchronous programming
intervened.

`TransportQueue` object has its own loop, if not set, use the event loop of the main thread
i.e. `IOLoop.current()` . Then all the coroutines of transport tasks are running in this loop.

#### improved.
In test `tests/engine/test_work_chain.py`, the `inspect.stack` is now support nametuple to
inspect the function name. Therefore, can be improved for `python>=3.5`

#### `add_callback` v.s. `ensure_future` in process async test
Now I change process test in plum by launching a process throughly asynchronous
with `asyncio.ensure_future`. The previous implementation is adding a callback
function in the loop and then launch the loop. Here with pytest asyncio, I
have the whole test function running in a loop by decorate the test with
`@pytest.mark.asyncio`. As a result, I cannot add callback in the current loop, while
have to launch the coroutine by `ensure_future`. This is not wrong in the situation, but
this implementation is not compatible with the process test case in aiida_core which
add the function by `loop.add_callback` and then running the loop.

So my question is which implementation is good? Can I use the same approach in aiida_core?

My understanding is that ensure_future is register a coroutine to be run in the future.
`ensure_future` is the asynchronous counterpart of the `call_soon` which for running a
synchronous function in event loop. And to run function in the event loop of other
thread, `call_soon_threadsafe` and its asynchronous counterpart `run_corountine_threadsafe`
are used.

Please check https://cheat.readthedocs.io/en/latest/python/asyncio.html for more information.
