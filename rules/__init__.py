"""Rule module"""


from .rule import (
    Rule, RuleException, 
    GameWon, InvalidPosition,
    SwapRequest
)

from .freestyle import FreeStyle
from .standard import Standard
