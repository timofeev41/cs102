import typing as tp
import typing_extensions as tp_e


# Vocabulary Types
from sqlalchemy.orm.query import Query

Vocabulary = tp.Dict[str, tp.Union[str, int]]
Freq = tp.Optional[Vocabulary]

# Data types
Label = str
Words = tp.Iterable[str]
Labels = tp.Iterable[Label]
NewsList = tp.List[tp.Dict[str, tp.Union[int, str]]]

# db types
DBEntries = tp.Iterable[Query[tp.Any]]
