import threading
from typing import Any, Callable, Iterable, Mapping, Optional


class Thread(threading.Thread):
    """Thread that return result at join()"""

    _target = None
    _args = ()
    _kwargs = {}
    _result = None
    _on_end_callback = None
    _on_end_callback_args = ()
    _on_end_callback_kwargs = {}

    def __init__(
        self,
        group: None = None,
        target: Optional[Callable[..., object]] = None,
        name: Optional[str] = None,
        args: Iterable[Any] = (),
        kwargs: Optional[Mapping[str, Any]] = {},
        *,
        daemon: Optional[bool] = True,
        on_end_callback: Optional[Callable[..., Any]] = None,
        on_end_callback_args: Iterable[Any] = (),
        on_end_callback_kwargs: Optional[Mapping[str, Any]] = {},
    ) -> None:
        """Thread init

        Args:
            group (None, optional): Thread group. Defaults to None.
            target (Optional[Callable[..., object]], optional): Target that will be called on start(). Defaults to None.
            name (Optional[str], optional): Thread name. Defaults to None.
            args (Iterable[Any], optional): Target's args. Defaults to ().
            kwargs (Optional[Mapping[str, Any]], optional): Target's kwargs. Defaults to None.
            daemon (Optional[bool], optional): Set thread to be daemon. Defaults to True.
            on_end_callback (Optional[Callable[..., Any]], optional): Callback to call before thread will be terminated. Defaults to None.
            on_end_callback_args (Iterable[Any], optional): on_end_callback' args. Defaults to ().
            on_end_callback_kwargs (Optional[Mapping[str, Any]], optional): on_end_callback's kwargs. Defaults to None.
        """
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._result = None
        self._on_end_callback = on_end_callback
        self._on_end_callback_args = on_end_callback_args
        self._on_end_callback_kwargs = on_end_callback_kwargs

    def run(self):
        """Thread's run"""
        if self._target is None:
            return
        try:
            self._result = self._target(*self._args, **self._kwargs)
            if self._on_end_callback is not None:
                self._on_end_callback(
                    self._result,
                    *self._on_end_callback_args,
                    **self._on_end_callback_kwargs,
                )
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def join(self, timeout: Optional[float] = None):
        """Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is called terminates – either normally or through an unhandled exception or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a floating point number specifying a timeout for the operation in seconds (or fractions thereof). As join() always returns None, you must call is_alive() after join() to decide whether a timeout happened – if the thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current thread as that would cause a deadlock. It is also an error to join() a thread before it has been started and attempts to do so raises the same exception.

        Args:
            timeout (Optional[float], optional): Join timeout. Defaults to None.

        Returns:
            Any: Returns result of target
        """
        super().join(timeout=timeout)
        return self._result
