import os

from ka_uts_log.log import LogEq
from ka_uts_dic.dopath import DoPath
from ka_uts_obj.path import Path

from typing import Any

TyPathLike = os.PathLike
TyAny = Any
TyArr = list[Any]
TyDic = dict[Any, Any]
TyPath = str
TyStr = str

TnAny = None | TyAny
TnDic = None | TyDic


class DoDoPath:

    @classmethod
    def sh_path(cls, dodopath: TyDic, kwargs: TyDic) -> TyPath:
        LogEq.debug("dodopath", dodopath)
        if not dodopath:
            return ''
        _d_path: TyDic = dodopath.get('d_path', {})
        LogEq.debug("_d_path", _d_path)
        _path: TyPath = DoPath.sh_path(_d_path, kwargs)
        LogEq.debug("_path", _path)

        _datetype = dodopath.get('datetype')
        LogEq.debug("_datetype", _datetype)

        if _datetype:
            _path = Path.sh_path_by_datetype(_path, _datetype, kwargs)
        return _path
