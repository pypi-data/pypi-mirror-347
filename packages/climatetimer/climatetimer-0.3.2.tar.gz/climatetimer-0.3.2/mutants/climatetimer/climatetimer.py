
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


# climatetimer/climatetimer.py
import warnings
from datetime import datetime, timedelta, timezone
from math import floor
from typing import Tuple

from .constants import (
    REFERENCES,
    REFERENCE_INFO,
    SECOND_DURATION,
    MINUTE_DURATION,
    QUARTER_DURATION,
    HOUR_DURATION,
    DAY_DURATION,
    WEEK_DURATION,
)

# Supported block types and their durations (in seconds)
TIME_BLOCKS = {
    "second": SECOND_DURATION,
    "minute": MINUTE_DURATION,
    "quarter": QUARTER_DURATION,
    "15m": QUARTER_DURATION,
    "hour": HOUR_DURATION,
    "day": DAY_DURATION,
    "week": WEEK_DURATION,
}


class ClimateTimer:
    """
    Computes time block IDs (blockid) and time periods (period) for various time units
    since a selected climate agreement (Paris Agreement or Kyoto Protocol).

    The reference timestamp is specified as a positional argument:
        - "paris": April 22, 2016 (UTC)
        - "kyoto": February 16, 2005 (UTC)

    Methods:
      - blockid(date, blocktype="quarter") -> int
      - period(block_id, blocktype="quarter") -> Tuple[datetime, datetime]
      - info() -> str
    """

    def xǁClimateTimerǁ__init____mutmut_orig(self, reference: str):
        """
        Initialize ClimateTimer with a reference timestamp.

        Args:
            reference (str): Must be either "paris" or "kyoto".

        Raises:
            ValueError: If an invalid reference is provided.
        """
        reference = reference.lower()
        if reference not in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")

        self.reference = REFERENCES[reference]
        self.refkey = reference  # Save the key for info() lookup

    def xǁClimateTimerǁ__init____mutmut_1(self, reference: str):
        """
        Initialize ClimateTimer with a reference timestamp.

        Args:
            reference (str): Must be either "paris" or "kyoto".

        Raises:
            ValueError: If an invalid reference is provided.
        """
        reference = None
        if reference not in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")

        self.reference = REFERENCES[reference]
        self.refkey = reference  # Save the key for info() lookup

    def xǁClimateTimerǁ__init____mutmut_2(self, reference: str):
        """
        Initialize ClimateTimer with a reference timestamp.

        Args:
            reference (str): Must be either "paris" or "kyoto".

        Raises:
            ValueError: If an invalid reference is provided.
        """
        reference = reference.lower()
        if reference  in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")

        self.reference = REFERENCES[reference]
        self.refkey = reference  # Save the key for info() lookup

    def xǁClimateTimerǁ__init____mutmut_3(self, reference: str):
        """
        Initialize ClimateTimer with a reference timestamp.

        Args:
            reference (str): Must be either "paris" or "kyoto".

        Raises:
            ValueError: If an invalid reference is provided.
        """
        reference = reference.lower()
        if reference not in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")

        self.reference = REFERENCES[None]
        self.refkey = reference  # Save the key for info() lookup

    def xǁClimateTimerǁ__init____mutmut_4(self, reference: str):
        """
        Initialize ClimateTimer with a reference timestamp.

        Args:
            reference (str): Must be either "paris" or "kyoto".

        Raises:
            ValueError: If an invalid reference is provided.
        """
        reference = reference.lower()
        if reference not in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")

        self.reference = None
        self.refkey = reference  # Save the key for info() lookup

    def xǁClimateTimerǁ__init____mutmut_5(self, reference: str):
        """
        Initialize ClimateTimer with a reference timestamp.

        Args:
            reference (str): Must be either "paris" or "kyoto".

        Raises:
            ValueError: If an invalid reference is provided.
        """
        reference = reference.lower()
        if reference not in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")

        self.reference = REFERENCES[reference]
        self.refkey = None  # Save the key for info() lookup

    xǁClimateTimerǁ__init____mutmut_mutants = {
    'xǁClimateTimerǁ__init____mutmut_1': xǁClimateTimerǁ__init____mutmut_1, 
        'xǁClimateTimerǁ__init____mutmut_2': xǁClimateTimerǁ__init____mutmut_2, 
        'xǁClimateTimerǁ__init____mutmut_3': xǁClimateTimerǁ__init____mutmut_3, 
        'xǁClimateTimerǁ__init____mutmut_4': xǁClimateTimerǁ__init____mutmut_4, 
        'xǁClimateTimerǁ__init____mutmut_5': xǁClimateTimerǁ__init____mutmut_5
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁClimateTimerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁClimateTimerǁ__init____mutmut_mutants"), *args, **kwargs)
        return result 

    __init__.__signature__ = _mutmut_signature(xǁClimateTimerǁ__init____mutmut_orig)
    xǁClimateTimerǁ__init____mutmut_orig.__name__ = 'xǁClimateTimerǁ__init__'



    @staticmethod
    def _validate_datetime(dt: datetime) -> datetime:
        """
        Ensure dt is a timezone-aware datetime.

        Args:
            dt (datetime): Datetime to validate.

        Returns:
            datetime: A timezone-aware datetime.

        Raises:
            TypeError: If dt is not a datetime object.
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"Expected a datetime object, got {type(dt).__name__}.")

        if dt.tzinfo is None:
            warnings.warn("Naive datetime provided; assuming UTC.", UserWarning)
            return dt.replace(tzinfo=timezone.utc)

        return dt

    @staticmethod
    def _validate_blocktype(blocktype: str):
        """
        Validate that blocktype is supported.

        Args:
            blocktype (str): The block type to validate.

        Raises:
            ValueError: If blocktype is not supported.
        """
        if blocktype not in TIME_BLOCKS:
            raise ValueError(f"Invalid blocktype '{blocktype}'. Choose from {list(TIME_BLOCKS.keys())}.")

    @staticmethod
    def _validate_block_id(block_id: int) -> int:
        """
        Validate that block_id is a positive integer.

        Args:
            block_id (int): The block ID to validate.

        Returns:
            int: The validated block ID.

        Raises:
            ValueError: If block_id is not a positive integer.
        """
        if not isinstance(block_id, int) or block_id < 1:
            raise ValueError(f"Invalid block_id {block_id}. Must be a positive integer.")

        return block_id

    def xǁClimateTimerǁblockid__mutmut_orig(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_1(self, date: datetime, blocktype: str = "XXquarterXX") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_2(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = None
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_3(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(None)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_4(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(None)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_5(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = None

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_6(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = None
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_7(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc + self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_8(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = None

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_9(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() * TIME_BLOCKS[blocktype]) + 1

    def xǁClimateTimerǁblockid__mutmut_10(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[None]) + 1

    def xǁClimateTimerǁblockid__mutmut_11(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) - 1

    def xǁClimateTimerǁblockid__mutmut_12(self, date: datetime, blocktype: str = "quarter") -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for which to compute the block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            int: The computed block ID.
        """
        blocktype = blocktype.lower()
        self._validate_blocktype(blocktype)
        date = self._validate_datetime(date)

        # Convert date to UTC before calculating the difference
        date_utc = date.astimezone(timezone.utc)
        delta = date_utc - self.reference

        return floor(delta.total_seconds() / TIME_BLOCKS[blocktype]) + 2

    xǁClimateTimerǁblockid__mutmut_mutants = {
    'xǁClimateTimerǁblockid__mutmut_1': xǁClimateTimerǁblockid__mutmut_1, 
        'xǁClimateTimerǁblockid__mutmut_2': xǁClimateTimerǁblockid__mutmut_2, 
        'xǁClimateTimerǁblockid__mutmut_3': xǁClimateTimerǁblockid__mutmut_3, 
        'xǁClimateTimerǁblockid__mutmut_4': xǁClimateTimerǁblockid__mutmut_4, 
        'xǁClimateTimerǁblockid__mutmut_5': xǁClimateTimerǁblockid__mutmut_5, 
        'xǁClimateTimerǁblockid__mutmut_6': xǁClimateTimerǁblockid__mutmut_6, 
        'xǁClimateTimerǁblockid__mutmut_7': xǁClimateTimerǁblockid__mutmut_7, 
        'xǁClimateTimerǁblockid__mutmut_8': xǁClimateTimerǁblockid__mutmut_8, 
        'xǁClimateTimerǁblockid__mutmut_9': xǁClimateTimerǁblockid__mutmut_9, 
        'xǁClimateTimerǁblockid__mutmut_10': xǁClimateTimerǁblockid__mutmut_10, 
        'xǁClimateTimerǁblockid__mutmut_11': xǁClimateTimerǁblockid__mutmut_11, 
        'xǁClimateTimerǁblockid__mutmut_12': xǁClimateTimerǁblockid__mutmut_12
    }

    def blockid(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁClimateTimerǁblockid__mutmut_orig"), object.__getattribute__(self, "xǁClimateTimerǁblockid__mutmut_mutants"), *args, **kwargs)
        return result 

    blockid.__signature__ = _mutmut_signature(xǁClimateTimerǁblockid__mutmut_orig)
    xǁClimateTimerǁblockid__mutmut_orig.__name__ = 'xǁClimateTimerǁblockid'



    def xǁClimateTimerǁblockids__mutmut_orig(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_1(self, start_date: datetime, end_date: datetime, blocktype: str = "XXquarterXX") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_2(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(None)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_3(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(None)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_4(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = None
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_5(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(None)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_6(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = None

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_7(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date >= end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_8(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("XXstart_date must not be after end_dateXX")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_9(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(None, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_10(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, None)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_11(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid( blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_12(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date,)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_13(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = None
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_14(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(None, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_15(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, None)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_16(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid( blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_17(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date,)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_18(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = None

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_19(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(None, end_block + 1))

    def xǁClimateTimerǁblockids__mutmut_20(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block - 1))

    def xǁClimateTimerǁblockids__mutmut_21(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range(start_block, end_block + 2))

    def xǁClimateTimerǁblockids__mutmut_22(self, start_date: datetime, end_date: datetime, blocktype: str = "quarter") -> list:
        """
        Compute the list of time block IDs for the given start and end datetimes and block type.

        Args:
            start_date (datetime): The start datetime of the range.
            end_date (datetime): The end datetime of the range.
            blocktype (str, optional): The type of time block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            list: A list of block IDs covering the date range.
        """
        # Validate the block type and the datetimes
        self._validate_blocktype(blocktype)
        start_date = self._validate_datetime(start_date)
        end_date = self._validate_datetime(end_date)

        # Ensure the start date is not after the end date
        if start_date > end_date:
            raise ValueError("start_date must not be after end_date")

        # Compute the block IDs for the start and end dates
        start_block = self.blockid(start_date, blocktype)
        end_block = self.blockid(end_date, blocktype)

        # Return the list of block IDs from start to end (inclusive)
        return list(range( end_block + 1))

    xǁClimateTimerǁblockids__mutmut_mutants = {
    'xǁClimateTimerǁblockids__mutmut_1': xǁClimateTimerǁblockids__mutmut_1, 
        'xǁClimateTimerǁblockids__mutmut_2': xǁClimateTimerǁblockids__mutmut_2, 
        'xǁClimateTimerǁblockids__mutmut_3': xǁClimateTimerǁblockids__mutmut_3, 
        'xǁClimateTimerǁblockids__mutmut_4': xǁClimateTimerǁblockids__mutmut_4, 
        'xǁClimateTimerǁblockids__mutmut_5': xǁClimateTimerǁblockids__mutmut_5, 
        'xǁClimateTimerǁblockids__mutmut_6': xǁClimateTimerǁblockids__mutmut_6, 
        'xǁClimateTimerǁblockids__mutmut_7': xǁClimateTimerǁblockids__mutmut_7, 
        'xǁClimateTimerǁblockids__mutmut_8': xǁClimateTimerǁblockids__mutmut_8, 
        'xǁClimateTimerǁblockids__mutmut_9': xǁClimateTimerǁblockids__mutmut_9, 
        'xǁClimateTimerǁblockids__mutmut_10': xǁClimateTimerǁblockids__mutmut_10, 
        'xǁClimateTimerǁblockids__mutmut_11': xǁClimateTimerǁblockids__mutmut_11, 
        'xǁClimateTimerǁblockids__mutmut_12': xǁClimateTimerǁblockids__mutmut_12, 
        'xǁClimateTimerǁblockids__mutmut_13': xǁClimateTimerǁblockids__mutmut_13, 
        'xǁClimateTimerǁblockids__mutmut_14': xǁClimateTimerǁblockids__mutmut_14, 
        'xǁClimateTimerǁblockids__mutmut_15': xǁClimateTimerǁblockids__mutmut_15, 
        'xǁClimateTimerǁblockids__mutmut_16': xǁClimateTimerǁblockids__mutmut_16, 
        'xǁClimateTimerǁblockids__mutmut_17': xǁClimateTimerǁblockids__mutmut_17, 
        'xǁClimateTimerǁblockids__mutmut_18': xǁClimateTimerǁblockids__mutmut_18, 
        'xǁClimateTimerǁblockids__mutmut_19': xǁClimateTimerǁblockids__mutmut_19, 
        'xǁClimateTimerǁblockids__mutmut_20': xǁClimateTimerǁblockids__mutmut_20, 
        'xǁClimateTimerǁblockids__mutmut_21': xǁClimateTimerǁblockids__mutmut_21, 
        'xǁClimateTimerǁblockids__mutmut_22': xǁClimateTimerǁblockids__mutmut_22
    }

    def blockids(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁClimateTimerǁblockids__mutmut_orig"), object.__getattribute__(self, "xǁClimateTimerǁblockids__mutmut_mutants"), *args, **kwargs)
        return result 

    blockids.__signature__ = _mutmut_signature(xǁClimateTimerǁblockids__mutmut_orig)
    xǁClimateTimerǁblockids__mutmut_orig.__name__ = 'xǁClimateTimerǁblockids'



    def xǁClimateTimerǁperiod__mutmut_orig(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_1(self, block_id: int, blocktype: str = "XXquarterXX") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_2(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(None)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_3(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(None)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_4(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = None
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_5(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference - timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_6(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id + 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_7(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 2) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_8(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) / TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_9(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[None])
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_10(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = None
        return start, start + timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_11(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start - timedelta(seconds=TIME_BLOCKS[blocktype])

    def xǁClimateTimerǁperiod__mutmut_12(self, block_id: int, blocktype: str = "quarter") -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            blocktype (str, optional): The type of block ("second", "minute", "quarter", "hour", "day", "week").
                                       Defaults to "quarter".

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_blocktype(blocktype)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[blocktype])
        return start, start + timedelta(seconds=TIME_BLOCKS[None])

    xǁClimateTimerǁperiod__mutmut_mutants = {
    'xǁClimateTimerǁperiod__mutmut_1': xǁClimateTimerǁperiod__mutmut_1, 
        'xǁClimateTimerǁperiod__mutmut_2': xǁClimateTimerǁperiod__mutmut_2, 
        'xǁClimateTimerǁperiod__mutmut_3': xǁClimateTimerǁperiod__mutmut_3, 
        'xǁClimateTimerǁperiod__mutmut_4': xǁClimateTimerǁperiod__mutmut_4, 
        'xǁClimateTimerǁperiod__mutmut_5': xǁClimateTimerǁperiod__mutmut_5, 
        'xǁClimateTimerǁperiod__mutmut_6': xǁClimateTimerǁperiod__mutmut_6, 
        'xǁClimateTimerǁperiod__mutmut_7': xǁClimateTimerǁperiod__mutmut_7, 
        'xǁClimateTimerǁperiod__mutmut_8': xǁClimateTimerǁperiod__mutmut_8, 
        'xǁClimateTimerǁperiod__mutmut_9': xǁClimateTimerǁperiod__mutmut_9, 
        'xǁClimateTimerǁperiod__mutmut_10': xǁClimateTimerǁperiod__mutmut_10, 
        'xǁClimateTimerǁperiod__mutmut_11': xǁClimateTimerǁperiod__mutmut_11, 
        'xǁClimateTimerǁperiod__mutmut_12': xǁClimateTimerǁperiod__mutmut_12
    }

    def period(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁClimateTimerǁperiod__mutmut_orig"), object.__getattribute__(self, "xǁClimateTimerǁperiod__mutmut_mutants"), *args, **kwargs)
        return result 

    period.__signature__ = _mutmut_signature(xǁClimateTimerǁperiod__mutmut_orig)
    xǁClimateTimerǁperiod__mutmut_orig.__name__ = 'xǁClimateTimerǁperiod'



    def xǁClimateTimerǁinfo__mutmut_orig(self) -> str:
        """
        Return a plain-text description of the instantiated time reference.

        Returns:
            str: A description of the reference event.
        """
        return REFERENCE_INFO[self.refkey]

    def xǁClimateTimerǁinfo__mutmut_1(self) -> str:
        """
        Return a plain-text description of the instantiated time reference.

        Returns:
            str: A description of the reference event.
        """
        return REFERENCE_INFO[None]

    xǁClimateTimerǁinfo__mutmut_mutants = {
    'xǁClimateTimerǁinfo__mutmut_1': xǁClimateTimerǁinfo__mutmut_1
    }

    def info(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁClimateTimerǁinfo__mutmut_orig"), object.__getattribute__(self, "xǁClimateTimerǁinfo__mutmut_mutants"), *args, **kwargs)
        return result 

    info.__signature__ = _mutmut_signature(xǁClimateTimerǁinfo__mutmut_orig)
    xǁClimateTimerǁinfo__mutmut_orig.__name__ = 'xǁClimateTimerǁinfo'


