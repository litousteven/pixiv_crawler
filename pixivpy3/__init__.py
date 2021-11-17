"""
Pixiv API library
"""
__version__ = '3.6.1'

from .papi import PixivAPI
from .utils import PixivError

__all__ = ('PixivAPI', 'PixivError')
