import functools
import logging
from typing import Callable, ParamSpec, TypeVar, overload

from django.conf import settings
from django.db import transaction

_P = ParamSpec("_P")
_T = TypeVar("_T")


def _atomic_operation(fnc: Callable[_P, _T]) -> Callable[_P, _T]:
    @functools.wraps(fnc)
    def wraps(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        with transaction.atomic():
            return fnc(*args, **kwargs)

    return wraps


def _selector(
    atomic: bool, ignore_transactions: bool
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    if ignore_transactions or settings.IGNORE_OPERATION_SETTINGS:  # type: ignore
        return lambda x: x
    if atomic:
        return _atomic_operation

    return lambda x: x


@overload
def operation(
    *, atomic: bool = True, ignore_transactions: bool = False
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    ...


@overload
def operation(
    fnc: Callable[_P, _T], *, atomic: bool = True, ignore_transactions: bool = False
) -> Callable[_P, _T]:
    ...


def operation(
    fnc: Callable[_P, _T] | None = None, *, atomic: bool = True, ignore_transactions: bool = False
) -> Callable[_P, _T] | Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """
    Define a functional operation.

    Functional operations are a logical concept that regroup actions that should live together.

    They are bound to the concept of atomicity and durability:
    * Atomic operations will all succeed or the application will revert to the previous state

    Durable operation are not supported yet.

    Settings IGNORE_OPERATION_SETTINGS set to True overrides ignore_transactions to True

    :param fnc: the function to decorate
    :param atomic: operation is atomic
    :param ignore_transactions: ignore transactions parameters
    :return: decorated function
    """
    if fnc is None:
        return lambda f: operation(
            f,
            atomic=atomic,
            ignore_transactions=ignore_transactions,
        )

    fnc = _selector(atomic, ignore_transactions)(fnc)

    @functools.wraps(fnc)
    def wraps(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        operation_name = fnc.__name__ if hasattr(fnc, "__name__") else repr(fnc)

        logging.debug(
            "Entering operation",
            extra={
                "operation_name": operation_name,
            },
        )
        try:
            return_value = fnc(*args, **kwargs)
        except Exception as err:
            logging.error(
                "Operation failed",
                exc_info=err,
                stack_info=True,
                extra={
                    "operation_name": operation_name,
                },
            )
            raise
        logging.debug(
            "Operation complete",
            extra={"operation_name": operation_name},
        )
        return return_value

    return wraps  # type: ignore
