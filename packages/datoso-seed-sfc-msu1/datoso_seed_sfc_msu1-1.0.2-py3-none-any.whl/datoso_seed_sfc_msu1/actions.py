"""Actions for the sfc msu1 seed."""
from datoso.configuration import logger
from datoso_seed_sfc_msu1.dats import SFCMSU1Dat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': SFCMSU1Dat,
        },
        {
            'action': 'DeleteOld',
            'folder': '{dat_destination}',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
}

def get_actions() -> dict:
    """Get the actions dictionary."""
    logger.error('Deprecated, use datoso_seed_enhanced instead')
    return actions
