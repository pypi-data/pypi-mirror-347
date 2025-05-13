"""This module contains the ``BaseConfig`` class."""

from __future__ import annotations

import importlib
import importlib.util
from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import partial
from typing import Any, ClassVar, Generic, TypeVar

from tno.quantum.utils._base_arguments import BaseArguments
from tno.quantum.utils._utils import convert_to_snake_case
from tno.quantum.utils.validation import (
    check_kwarglike,
    check_snake_case,
    check_string,
)

# ruff: noqa:  UP007

T = TypeVar("T")


@dataclass(init=False)
class BaseConfig(ABC, BaseArguments, Generic[T]):
    """Abstract base configuration class for creating instances of a specific class.

    The :py:class:`BaseConfig` class allows users to easily create configuration classes
    that can be used to instantiate arbitrary class objects. For instance, see
    :py:class:`~BackendConfig` or :py:class:`~OptimizerConfig`.

    Each configuration class must implement a :py:meth:`supported_items` method that
    returns a dictionary with as keys the `snake_case` class names and as values
    constructors of supported classes. These can be either the class or callable objects
    that return class instances.

    From a configuration object, instances can be created using the
    :py:meth:`get_instance` method.

    The `name` attribute can be provided in either snake_case, camelCase or PascalCase,
    that is, ``"TestSolver"`` and ``"test_solver"`` will be treated the same.

    Example:
        >>> from tno.quantum.utils import BaseConfig
        >>>
        >>> def add(x, y):
        ...     return x + y
        >>>
        >>> def mul(x, y):
        ...     return x * y
        >>>
        >>> class IntegerConfig(BaseConfig[int]):
        ...     @staticmethod
        ...     def supported_items():
        ...         return { "add": add, "mul": mul }
        >>>
        >>> config = IntegerConfig(name="mul", options={"x": 6, "y": 7})
        >>> config.get_instance()
        42
    """

    _name: str
    """Name used to determine the name of the to instantiate class."""
    _options: dict[str, Any]
    """Keyword arguments to be passed to the constructor of the class."""
    _supported_custom_items: ClassVar[dict[str, type[Any] | Callable[..., Any]]] = {}

    def __init__(self, name: str, options: Mapping[str, Any] | None = None) -> None:
        """Init :py:class:`BaseConfig`.

        Args:
            name: Name used to determine the name of the to instantiate class.
            options: Keyword arguments to be passed to the constructor of the class.

        Raises:
            TypeError: If `name` is not a string or `options` is not a mapping.
            KeyError: If `options` has a key that is not a string.
            KeyError: If `name` does not match any of the supported items.
        """
        self._name = check_string(name, "name")
        self._name = convert_to_snake_case(self._name, path=True)
        self._options = (
            check_kwarglike(options, "options", safe=True)
            if options is not None
            else {}
        )

        if self._name not in self.supported_items() | self.supported_custom_items():
            msg = f"Name '{self._name}' does not match any of the supported items."
            raise KeyError(msg)

    @property
    def name(self) -> str:
        """Name used to determine the name of the to instantiate class."""
        return self._name

    @property
    def options(self) -> dict[str, Any]:
        """Keyword arguments to be passed to the constructor of the class."""
        return self._options

    @staticmethod
    @abstractmethod
    def supported_items() -> (
        dict[str, type[T]]
        | dict[str, Callable[..., T]]
        | dict[str, type[T] | Callable[..., T]]
    ):
        """Returns the supported classes.

        This method must be implemented for each configuration class and should return a
        dictionary with as keys the `snake_case` class names and values the supported
        classes or callable objects that return supported classes.

        Returns:
            Dictionary with constructors of supported classes.
        """

    @classmethod
    def supported_custom_items(
        cls,
    ) -> (
        dict[str, type[T]]
        | dict[str, Callable[..., T]]
        | dict[str, type[T] | Callable[..., T]]
    ):
        """Returns the supported custom classes."""
        prefix = cls.prefix()
        return {
            full_name[len(prefix) :]: item
            for full_name, item in cls._supported_custom_items.items()
            if full_name.startswith(prefix)
        }

    @classmethod
    def register_custom_item(cls, name: str, item: type[T] | Callable[..., T]) -> None:
        """Register a custom item to the supported custom items.

        Args:
            name: Name of the custom item to be added. Will be converted to
                snake_case version.
            item: Custom item to be added. Item needs to be a constructor of the
                custom class and can be the class itself or a callable function that
                returns the class instance.

        Raises:
            ValueError: If `name` already exists in supported items or supported
                custom items.
            TypeError: If `item` is not a class or callable object.
        """
        check_snake_case(name, "name", path=True, warn=True)
        name = convert_to_snake_case(name, path=True)

        if not callable(item):
            msg = f"Provided item {item} is not a class or callable object."
            raise TypeError(msg)

        if name in cls.supported_items():
            msg = (
                f"The custom item with name `{name}` can't be added because there "
                f"already exists a similar named item within `supported_items`."
            )
            raise ValueError(msg)

        if name in cls.supported_custom_items():
            msg = (
                f"The custom item with name `{name}` can't be added because there "
                f"already exists a similar named item within `supported_custom_items`."
            )
            raise ValueError(msg)

        cls._supported_custom_items[cls.prefix() + name] = item

    @classmethod
    def prefix(cls) -> str:
        """Compute prefix that prevents naming conflicts in storage of custom items."""
        return f"{cls.__name__}-"

    def get_instance(self, *additional_args: Any, **additional_kwargs: Any) -> T:
        """Creates configured object instance.

        Args:
            additional_args: Additional constructor arguments to be passed to the class.
            additional_kwargs: Additional constructor keyword arguments that are not
                provided by the options, If the keyword argument is also provided in the
                options, the``additional_kwargs`` take priority.

        Returns:
            A configured object.
        """
        supported_items = self.supported_items()
        supported_custom_items = self.supported_custom_items()
        all_supported_items: dict[str, type[T] | Callable[..., T]] = {
            **supported_items,
            **supported_custom_items,
        }

        name_snake_case = convert_to_snake_case(self._name, path=True)
        if name_snake_case not in all_supported_items:
            msg = (
                f"The provided configuration with name `{self._name}` is invalid. "
                f"Allowed values are: {list(all_supported_items.keys())}."
            )
            raise KeyError(msg)
        object_class = all_supported_items[name_snake_case]
        return object_class(*additional_args, **{**self._options, **additional_kwargs})


if importlib.util.find_spec("pennylane") is not None:
    from pennylane.devices import Device

    @dataclass(init=False)
    class BackendConfig(BaseConfig[Device]):
        """Configuration class for creating PennyLane device instances.

        Supported backends can be found by calling
        :py:meth:`~BackendConfig.supported_items`.

        Example:
            >>> from tno.quantum.utils import BackendConfig
            >>>
            >>> # List all supported backends
            >>> sorted(BackendConfig.supported_items())[:4]
            ['default.clifford', 'default.gaussian', 'default.mixed', 'default.qubit']
            >>>
            >>> # Instantiate a backend
            >>> config = BackendConfig(name="default.qubit", options={"wires": 5})
            >>> type(config.get_instance())
            <class 'pennylane.devices.default_qubit.DefaultQubit'>
        """

        def __init__(self, name: str, options: Mapping[str, Any] | None = None) -> None:
            """Init :py:class:`BackendConfig`.

            Args:
                name: Name of the PennyLane :py:class:`~pennylane.devices.Device`,
                    for example ``"default.qubit"``.
                options: Keyword arguments to be passed to the constructor of the device
                    class.

            Raises:
                TypeError: If `name` is not a string or `options` is not a mapping.
                KeyError: If `options` has a key that is not a string.
                KeyError: If `name` does not match any of the supported backends.
            """
            super().__init__(name=name, options=options)

        @staticmethod
        def supported_items() -> dict[str, Callable[..., Device]]:
            """Obtain all supported PennyLane backend devices.

            Returns:
                Dictionary with callable that instantiate Pennylane Device instances.

            Raises:
                ModuleNotFoundError: If PennyLane can not be detected and no backends
                    can be found.
            """
            try:
                import pennylane as qml

                return {
                    device_name: partial(qml.device, name=device_name)
                    for device_name in qml.plugin_devices
                }
            except ModuleNotFoundError as exception:
                msg = "PennyLane can't be detected and hence no devices can be found."
                raise ModuleNotFoundError(msg) from exception


if importlib.util.find_spec("torch") is not None:
    from torch.optim.optimizer import Optimizer

    @dataclass(init=False)
    class OptimizerConfig(BaseConfig[Optimizer]):
        """Configuration class for creating instances of a PyTorch optimizer.

        Currently only a selection of PyTorch optimizers are supported. See the
        documentation of :py:meth:`~OptimizerConfig.supported_items` for information on
        which optimizers are supported.

        Example:
            >>> import torch
            >>> from tno.quantum.utils import OptimizerConfig
            >>>
            >>> # List all supported optimizers
            >>> list(OptimizerConfig.supported_items())
            ['adagrad', 'adam', 'rprop', 'stochastic_gradient_descent']
            >>>
            >>> # Instantiate an optimizer
            >>> config = OptimizerConfig(name="adagrad", options={"lr": 0.5})
            >>> type(config.get_instance(params=[torch.rand(1)]))
            <class 'torch.optim.adagrad.Adagrad'>
        """

        def __init__(self, name: str, options: Mapping[str, Any] | None = None) -> None:
            """Init :py:class:`OptimizerConfig`.

            Args:
                name: Name of the :py:class:`torch.optim.optimizer.Optimizer` class.
                options: Keyword arguments to be passed to the optimizer. Must be a
                    mapping-like object keys being string objects. Values can be
                    anything depending on specific optimizer.

            Raises:
                TypeError: If `name` is not a string or `options` is not a mapping.
                KeyError: If `options` has a key that is not a string.
                KeyError: If `name` does not match any of the supported optimizers.
            """
            super().__init__(name=name, options=options)

        @staticmethod
        def supported_items() -> dict[str, type[Optimizer]]:
            """Obtain supported PyTorch optimizers.

            If PyTorch is installed then the following optimizers are supported:

                - Adagrad
                    - name: ``"adagrad"``
                    - options: see `Adagrad kwargs`__

                - Adam
                    - name: ``"adam"``
                    - options: see `Adam kwargs`__

                - Rprop
                    - name: ``"rprop"``
                    - options: see `Rprop kwargs`__

                - SDG:
                    - name: ``"stochastic_gradient_descent"``
                    - options: see `SDG kwargs`__


            __ https://pytorch.org/docs/stable/generated/torch.optim.Adagrad.html
            __ https://pytorch.org/docs/stable/generated/torch.optim.Adam.html
            __ https://pytorch.org/docs/stable/generated/torch.optim.Rprop.html
            __ https://pytorch.org/docs/stable/generated/torch.optim.SGD.html

            Raises:
                ModuleNotFoundError: If PyTorch can not be detected and no optimizers
                    can be found.

            Returns:
                Dictionary with supported optimizers by their name.
            """
            try:
                from torch.optim.adagrad import Adagrad
                from torch.optim.adam import Adam
                from torch.optim.rprop import Rprop
                from torch.optim.sgd import SGD

            except ModuleNotFoundError as exception:
                msg = "Torch can't be detected and hence no optimizers can be found."
                raise ModuleNotFoundError(msg) from exception

            else:
                return {
                    "adagrad": Adagrad,
                    "adam": Adam,
                    "rprop": Rprop,
                    "stochastic_gradient_descent": SGD,
                }
