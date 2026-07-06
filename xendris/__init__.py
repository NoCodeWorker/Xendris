"""
Xendris — public framework layer over the internal Phyng scientific engine.

Stable API candidates for v0.2.0:
    xendris
    xendris.frontera_c   — stable bridge over selected Phyng scientific primitives
    xendris.core.rag     — stable source and claim registry bridge

Experimental/internal namespaces remain importable by direct path for backward
compatibility, but are not advertised as stable top-level exports yet:
    xendris.core.campaigns
    xendris.models
    xendris.benchmarks
    xendris.prompts
    xendris.outputs
    xendris.scripts

Stable importability does not imply scientific validation.
"""

__version__ = "0.2.0"
__all__ = ["frontera_c"]

from . import frontera_c  # noqa: F401, E402 — make frontera_c importable
