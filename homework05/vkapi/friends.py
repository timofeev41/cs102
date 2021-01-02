import dataclasses
import math
import time
import typing as tp

from vkapi import config, session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    """
    Ответ на вызов метода `friends.get`.

    :param count: Количество пользователей.
    :param items: Список идентификаторов друзей пользователя или список пользователей.
    """

    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    user_data = {
        "access_token": config.VK_CONFIG["access_token"],
        "v": config.VK_CONFIG["version"],
        "count": count,
        "user_id": user_id if user_id is not None else "",
        "fields": ",".join(fields) if fields is not None else "",
        "offset": offset,
    }
    response = session.get("/friends.get", params=user_data)
    if "error" in response.json() or not response.ok:
        raise APIError(response.json()["error"]["error_msg"])
    else:
        return FriendsResponse(
            count=response.json()["response"]["count"],
            items=response.json()["response"]["items"],
        )


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    # user_data = {"source_uid": source_uid, "target_uid": target_uid, "target_uids": target_uids,
    # "order": order, "count": count, "offset": offset, "progress": progress}
    # response = session.get("/friends.getMutual", params=user_data)
    # if "error" in response.json():
    #     raise APIError(response.json()["error"]["error_msg"])
    # else:
    #     result = MutualFriends(id=)
    #     return result
