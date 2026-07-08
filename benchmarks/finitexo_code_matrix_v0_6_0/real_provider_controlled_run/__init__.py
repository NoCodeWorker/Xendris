"""Finitexo Code Matrix v0.6.0 real-provider controlled run."""

__all__ = [
    "ControlledRunConfig",
    "ControlledProviderResult",
    "ControlledProviderSpec",
    "run_controlled_provider_benchmark",
    "write_controlled_run_artifacts",
]


def __getattr__(name):
    if name in __all__:
        from . import controlled_run

        return getattr(controlled_run, name)
    raise AttributeError(name)
