from typing import Tuple, Iterable


__all__ = [
    'ReplyTo', 'Attachment',
]

ReplyTo = Tuple[str, str]
Attachment = Iterable[Tuple[str, object, str]]
