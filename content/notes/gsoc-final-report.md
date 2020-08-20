+++
title="Final report GSoC 2020: full support of asyncio in AiiDA"
date=2020-08-20
Tags=["GSoC"]
Category=["Note"]
+++

## Codes and links of all achievement for easy evaluation

- [X] Drop the old version tornado and uses asyncio event loop tornado in `circus`.
  - [circus#1129](https://github.com/circus-tent/circus/pull/1129) circus with new tornado>5.0.2
  - (under review) [circus#1132](https://github.com/circus-tent/circus/pull/1132) Fix the `quit --waiting` command hang up issue

- [X] Replace `tornado` with `asyncio` in plumpy.
  - [plumpy#150](https://github.com/aiidateam/plumpy/pull/150) where also archive all discussion in community rebased in [plumpy#160](https://github.com/aiidateam/plumpy/pull/160).
  - plumpy documentation revamp. (Ongoing) https://github.com/aiidateam/plumpy/pull/167
- [X] Replace `tornado` with `asyncio` in `aiida_core`.
  - (under review)[aiida_core#4218](https://github.com/aiidateam/aiida-core/pull/4218) drop tornado<5 and implement new event loop policy with asyncio.

## Sporadic contributions in and out of the AiiDA community during GSoC.
  - Mentioned minor fix for `nest_asyncio` https://github.com/erdewit/nest_asyncio/pull/28 .
  - PRs: https://github.com/aiidateam/aiida-core/pull/4271 , https://github.com/aiidateam/aiida-core/pull/4081
  - Code review attempts: https://github.com/aiidateam/aiida-core/pull/4117 , https://github.com/aiidateam/aiida-core/pull/3977
  - (under review) aiidalab: https://github.com/aiidalab/aiidalab-widgets-base/pull/110

## Logs and week summary of the project
All posts about the project is in my personal blog tag with gsoc: https://morty.tech/tags/gsoc/
