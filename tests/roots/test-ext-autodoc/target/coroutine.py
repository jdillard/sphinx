class AsyncClass:
    async def do_coroutine(self):
        """A documented coroutine function"""
        attr_coro_result = await _other_coro_func()  # NOQA

    @classmethod
    async def do_coroutine2(cls):
        """A documented coroutine classmethod"""
        pass

    @staticmethod
    async def do_coroutine3():
        """A documented coroutine staticmethod"""
        pass


async def _other_coro_func():
    return "run"
