import typing as tp
import typing_extensions as tp_e

# Vocabulary Types
Vocabulary = tp.Dict[str, tp.Union[str, int]]
Freq = tp.Optional[Vocabulary]

# Data types
Label = str
Words = tp.Iterable[str]
Labels = tp.Iterable[str]
