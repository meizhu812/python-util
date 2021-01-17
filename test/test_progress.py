from unittest import TestCase

from util.progress import ActiveStateError, FulfillStateError, Progress, TerminateStateError


class TestProgress(TestCase):
    _progress: Progress

    def setUp(self) -> None:
        self._progress = Progress(target=1)

    def test___init___(self):
        progress = self._progress
        self.assertFalse(progress.terminated)
        self.assertFalse(progress.active)
        self.assertFalse(progress.fulfilled)
        self.assertEqual(1, progress.target)
        self.assertEqual(0, progress.value)

    def test_activate(self):
        progress = self._progress
        with self.subTest('success_if_not_active'):
            progress.activate()
            self.assertTrue(progress.active)
        with self.subTest('raises_if_active'):
            self.assertRaises(ActiveStateError, progress.activate)
        with self.subTest('raises_if_terminated'):
            progress.finish(force=True)
            self.assertRaises(TerminateStateError, progress.activate)

    def test_update(self):
        progress = self._progress
        with self.subTest('raises_if_not_active'):
            self.assertRaises(ActiveStateError, progress.update)
        with self.subTest('success_if_active'):
            progress.activate()
            progress.update()
            self.assertEqual(1, progress.value)

    def test_end(self):
        progress = Progress(target=2)
        with self.subTest('raises_if_not_active'):
            self.assertRaises(ActiveStateError, progress.finish)
        with self.subTest('if_active'):
            progress.activate()
            progress.update()
            with self.subTest('raises_if_progress_not_fulfilled'):
                self.assertFalse(progress.fulfilled)
                self.assertRaises(FulfillStateError, progress.finish)
            with self.subTest('success_if_fulfilled'):
                progress.update()
                self.assertTrue(progress.fulfilled)
                progress.finish()
                self.assertFalse(progress.active)

    def test_end_force(self):
        progress = self._progress
        with self.subTest('raises_if_not_active'):
            self.assertRaises(ActiveStateError, progress.finish, force=True)
        with self.subTest('success_if_active'):
            progress.activate()
            self.assertFalse(progress.fulfilled)
            progress.finish(force=True)
            self.assertFalse(progress.active)
