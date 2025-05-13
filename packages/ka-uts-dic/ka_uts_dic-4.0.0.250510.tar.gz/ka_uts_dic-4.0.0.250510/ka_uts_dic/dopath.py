import os

from ka_uts_log.log import LogEq
from ka_uts_uts.utils.pac import Pac

from typing import Any

TyPathLike = os.PathLike
TyAny = Any
TyArr = list[Any]
TyDic = dict[Any, Any]
TyPath = str
TyStr = str

TnAny = None | TyAny
TnDic = None | TyDic


class DoPath:

    @staticmethod
    def sh_path(d_path: TyDic, kwargs: TyDic) -> TyPath:
        LogEq.debug("d_path", d_path)
        _a_part: TyArr = []
        _package: TyStr = kwargs.get('package', '')
        for _k, _v in d_path.items():
            LogEq.debug("_k", _k)
            LogEq.debug("_v", _v)
            match _v:
                case 'key':
                    _val = kwargs.get(_k)
                    if _val:
                        _a_part.append(_val)
                case 'pac':
                    _val = Pac.sh_path_by_path(_package, _k)
                    if _val:
                        _a_part.append(_val)
                case _:
                    _a_part.append(_k)
        LogEq.debug("_a_part", _a_part)
        if not _a_part:
            msg = f"a_part for d_path = {d_path} is undefined or empty"
            raise Exception(msg)
        return os.path.join(*_a_part)
