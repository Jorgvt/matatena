# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_exceptions.ipynb.

# %% auto 0
__all__ = ['ColumnFullError']

# %% ../01_exceptions.ipynb 3
class ColumnFullError(Exception):
    """
    Raised when trying to put a dice in a column that is already full.
    """
    pass