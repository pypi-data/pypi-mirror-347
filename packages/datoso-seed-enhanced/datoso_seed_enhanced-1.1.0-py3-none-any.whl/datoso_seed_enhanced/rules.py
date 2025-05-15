"""Rules for the Super Famicom Speed Hacks seed."""
from datoso_seed_enhanced.dats import EnhancedDat

rules = [
    {
        'name': '32X MD+ Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': '32X',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MD+',
            },
        ],
    },
    {
        'name': '32X MSU-MD Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': '32X',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MSU-MD',
            },
        ],
    },
    {
        'name': 'Sega CD Hacks Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega CD Hacks',
            },
        ],
    },
    {
        'name': 'Mega Drive Enhanced Colors Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Enhanced Colors',
            },
        ],
    },
    {
        'name': 'Mega Drive MD+ Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MD+',
            },
        ],
    },
    {
        'name': 'Mega Drive Mode 1 CD Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mode 1 CD',
            },
        ],
    },
    {
        'name': 'Mega Drive MSU-MD Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MSU-MD',
            },
        ],
    },
    {
        'name': 'Super Famicom Enhanced Colors Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Enhanced Colors',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Super Famicom',
            },
        ],
    },
    {
        'name': 'Super Famicom Speed Hacks Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 0,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Speed Hacks',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Super Famicom',
            },
        ],
    },
    {
        'name': 'Super Famicom MSU1-SFC Dat',
        '_class': EnhancedDat,
        'seed': 'enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MSU1',
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Super Famicom',
            },
        ],
    },
]


def get_rules() -> list:
    """Get the rules."""
    return rules
