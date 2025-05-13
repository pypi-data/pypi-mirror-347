"""Fetch and download DAT files."""
from datoso.configuration import logger


def fetch() -> None:
    """Fetch and download DAT files. (deprecated)."""
    logger.error('Deprecated, use datoso_seed_enhanced instead')
    raise NotImplementedError('Deprecated, use datoso_seed_enhanced instead')
