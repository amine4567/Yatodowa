from functools import reduce
from typing import Callable


def chain_decorators(decorators: tuple[Callable], func: Callable) -> Callable:
    """Apply decorators on function from left to right

    Args:
        decorators (tuple[Callable]): The leftmost decorator is applied first
        func (Callable): Decorated function

    Returns:
        Callable: Transformed function

    Examples:
        >>> chain_decorators([dec1, dec2, dec3], func)

        is equivalent to

        >>> @dec3
        ... @dec2
        ... @dec1
        ... def func(...):
        ...     ...
    """
    modified_f = reduce(
        lambda decorated, decorator: decorator(decorated),
        decorators,
        func,
    )
    return modified_f
