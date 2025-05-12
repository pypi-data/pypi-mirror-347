"""Strategy pattern implementation for cipher algorithms."""

import importlib
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Type


class CipherStrategy(ABC):  # pragma: no cover
    """Abstract base class for all cipher strategies."""

    @abstractmethod
    def encrypt(self, message: str, key: Any) -> str:
        """Encrypt a message using the strategy's algorithm."""
        pass

    @abstractmethod
    def decrypt(self, message: str, key: Any) -> str:
        """Decrypt a message using the strategy's algorithm."""
        pass


class CipherFactory:
    """Factory for creating cipher strategy instances."""

    _strategies: Dict[str, Type[CipherStrategy]] = {}
    _initialized = False

    @classmethod
    def _initialize(cls) -> None:
        """Initialize the factory by loading all available strategies."""
        if cls._initialized:
            return

        # Get the directory where strategies are stored
        strategies_dir = os.path.join(os.path.dirname(__file__), "strategies")

        # Skip if the directory doesn't exist
        if not os.path.isdir(strategies_dir):
            cls._initialized = True
            return

        # Find all Python files in the strategies directory
        for filename in os.listdir(strategies_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                try:
                    # Import the module dynamically
                    module = importlib.import_module(f"ciphers.strategies.{module_name}")

                    # Look for classes that inherit from CipherStrategy
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, CipherStrategy)
                            and attr is not CipherStrategy
                        ):
                            # Register the strategy with its lowercase name
                            cls.register_cipher(module_name, attr)
                except ImportError:
                    # Skip if there's an import error
                    continue

        cls._initialized = True

    @classmethod
    def get_cipher(cls, algorithm: str) -> CipherStrategy:
        """
        Get a cipher strategy instance by name.

        Args:
            algorithm: The name of the cipher algorithm

        Returns:
            An instance of the requested cipher strategy

        Raises:
            ValueError: If the algorithm is not supported
        """
        # Initialize if not already done
        if not cls._initialized:
            cls._initialize()

        if algorithm not in cls._strategies:
            supported = ", ".join(cls._strategies.keys())
            raise ValueError(
                f"Unsupported algorithm: {algorithm}. Supported algorithms: {supported}"
            )

        return cls._strategies[algorithm]()

    @classmethod
    def register_cipher(cls, name: str, strategy_class: Type[CipherStrategy]) -> None:
        """
        Register a new cipher strategy.

        Args:
            name: The name of the cipher algorithm
            strategy_class: The cipher strategy class
        """
        cls._strategies[name] = strategy_class
