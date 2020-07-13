class TestProcessSaving(unittest.TestCase):

    def test_save_future(self):
        """
        test `SavableFuture` is initialized with the event loop of process
        """
        loop = asyncio.new_event_loop()
        nsync_comeback = SavePauseProc(loop=loop)

        async def async_test():
            await utils.run_until_paused(nsync_comeback)

            # Create a checkpoint
            bundle = plumpy.Bundle(nsync_comeback)

            # here the future should be a SavableFuture in loop of process
            nsync_comeback.play()
            await nsync_comeback.future()

            self.assertListEqual([SavePauseProc.run.__name__, SavePauseProc.step2.__name__], nsync_comeback.steps_ran)

            proc_unbundled = bundle.unbundle()

            # At bundle time the Process was paused, the future of which will be persisted to the bundle.
            # As a result the process, recreated from that bundle, will also be paused and will have to be played
            proc_unbundled.play()
            self.assertEqual(0, len(proc_unbundled.steps_ran))

            # option A:
            await proc_unbundled.step_until_terminated()

            # option B:
            # why not future also fully saved and can be await here? Is that possible?
            await proc_unbundled.future()

            self.assertEqual([SavePauseProc.step2.__name__], proc_unbundled.steps_ran)

        loop.create_task(nsync_comeback.step_until_terminated())
        loop.run_until_complete(async_test())
