import string
import typing as tp

Words = tp.Iterable[str]


def clean(word: str) -> str:
    translator = str.maketrans("", "", string.punctuation + string.digits)
    return word.translate(translator).lower()


def prepare_data(data: Words) -> tp.List[str]:
    clean_data: tp.List[str] = []
    for item in data:
        clean_item = clean(item)
        if clean_item:
            clean_data.append(clean_item)
    return clean_data
