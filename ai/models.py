from g4f import models as __g4f_models
import Levenshtein
from functools import lru_cache


__TEXT_MODELS = set()
__IMAGE_MODELS = set()


def __init():
    for name, model in __g4f_models.ModelUtils.convert.items():
        if isinstance(model, __g4f_models.ImageModel):
            __IMAGE_MODELS.add(name)
        else:
            __TEXT_MODELS.add(name)


def get_text_models() -> set[str]:
    if len(__TEXT_MODELS) == 0:
        __init()
    return __TEXT_MODELS.copy()


def get_image_models() -> set[str]:
    if len(__IMAGE_MODELS) == 0:
        __init()
    return __IMAGE_MODELS.copy()


@lru_cache
def __get_ratio(str1: str, str2: str) -> float:
    str1 = str1.replace("-", "").replace(" ", "").lower()
    str2 = str2.replace("-", "").replace(" ", "").lower()
    return Levenshtein.ratio(str1, str2)


def __get_sorted_list_by_similarity(prompt: str, collection: set[str]) -> list[str]:
    return sorted(
        collection,
        key=lambda s: __get_ratio(prompt, s),
        reverse=True,
    )


def find_closest_text_models(prompt: str, n: int | None = None) -> list[str]:
    similar = __get_sorted_list_by_similarity(prompt=prompt, collection=get_text_models())
    if n is not None and n < len(similar):
        if n < 1:
            raise ValueError("Invalid var 'n' -> must be greater than 1")
        return similar[:n]
    return similar


def find_closest_image_models(prompt: str, n: int | None = None) -> list[str]:
    similar = __get_sorted_list_by_similarity(prompt=prompt, collection=get_image_models())
    if n is not None and n < len(similar):
        if n < 1:
            raise ValueError("Invalid var 'n' -> must be greater than 1")
        return similar[:n]
    return similar
