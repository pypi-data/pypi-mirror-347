
from inspect import signature as _mutmut_signature

def _mutmut_trampoline(orig, mutants, *args, **kwargs):
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*args, **kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*args, **kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition('.')[-1]
    result = mutants[mutant_name](*args, **kwargs)
    return result


from inspect import signature as _mutmut_signature

def _mutmut_yield_from_trampoline(orig, mutants, *args, **kwargs):
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = yield from orig(*args, **kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = yield from orig(*args, **kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition('.')[-1]
    result = yield from mutants[mutant_name](*args, **kwargs)
    return result


# climatetimer/constants.py
from datetime import datetime, timezone

# Available reference timestamps
REFERENCES = {
    "paris": datetime(2016, 4, 22, 0, 0, 0, tzinfo=timezone.utc),
    "kyoto": datetime(2005, 2, 16, 0, 0, 0, tzinfo=timezone.utc),
}

# Descriptions for each reference event
REFERENCE_INFO = {
    "paris": (
        "Paris Agreement (April 22, 2016): Global commitment to limit warming to well below "
        "2°C above pre-industrial levels with 190+ countries participating."
    ),
    "kyoto": (
        "Kyoto Protocol (February 16, 2005): First binding international agreement to reduce "
        "greenhouse gas emissions with 192 countries participating."
    ),
}

# Fixed duration constants in seconds
SECOND_DURATION = 1
MINUTE_DURATION = 60
QUARTER_DURATION = 15 * 60  # 15-minute block
HOUR_DURATION = 3600
DAY_DURATION = 24 * 3600
WEEK_DURATION = 7 * 24 * 3600
