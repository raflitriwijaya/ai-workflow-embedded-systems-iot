"""Single source of truth for the harness version.

Per spec §10.4 the evaluation harness itself is SemVer-versioned; the engine
version is stamped onto every ``evaluation_runs`` row so historical scores
remain attributable to the engine that produced them.
"""
__version__ = "1.0.0"
ENGINE_VERSION = __version__
