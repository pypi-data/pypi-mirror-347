"""
This module provides task scheduling classes for the management of OmniTracker
SRR (NHRR) processing for Department UMH.
    SRR: Sustainability Risk Rating
    NHRR: Nachhaltigkeits Risiko Rating
"""
import os
import shutil

from ka_uts_log.log import LogEq
from ka_uts_dic.dopath import DoPath
from ka_uts_obj.path import Path
from ka_uts_uts.ioc.yaml_ import Yaml_

from typing import Any

TyAny = Any
TyDic = dict[Any, Any]
TyDoD = dict[Any, TyDic]
TyAoD = list[TyDic]
TyAoDoD = list[TyDoD]
TyPath = str
TnAny = None | TyAny


class Setup:
    """
    Setup function class
    """
    @staticmethod
    def copytree(src: Any, tgt: Any) -> None:
        if not src:
            return
        if not os.path.exists(tgt):
            os.makedirs(tgt)
        shutil.copytree(src, tgt, dirs_exist_ok=True)

    @classmethod
    def sh_path_for_loc(cls, dod_copy, loc, kwargs: TyDic) -> TyPath:
        _d_copy = dod_copy.get(loc, [])
        if not _d_copy:
            msg = f"{loc}-array for _d_copy = {_d_copy} is empty"
            raise Exception(msg)
        _path = DoPath.sh_path(_d_copy, kwargs)
        if not _path:
            msg = f"{loc}-path for _d_copy = {_d_copy} is undefined or empty"
            raise Exception(msg)
        return _path

    @classmethod
    def setup(cls, kwargs: TyDic) -> None:
        _aodod_copy: TyAny = kwargs.get('aodod_copy', [])
        print("--------------------------------------")
        LogEq.debug("_aodod_copy", _aodod_copy)
        print(f"_aodod_copy = {_aodod_copy}")
        print("--------------------------------------")
        if not _aodod_copy:
            _in_path_aodod_copy: TyPath = kwargs.get('in_path_aodod_copy', '')
            _path: TyPath = Path.sh_path_by_tpl_and_pac(_in_path_aodod_copy, kwargs)
            _aodod_copy = Yaml_.read_with_safeloader(_path)
            if not _aodod_copy:
                raise Exception(f"Content of yaml file = {_path} is undefined or empty")

        print("======================================")
        print(f"_aodod_copy = {_aodod_copy}")
        print("======================================")
        for _dod_copy in _aodod_copy:
            print(f"_dod_copy = {_dod_copy}")
            _src_path = cls.sh_path_for_loc(_dod_copy, 'src', kwargs)
            _dst_path = cls.sh_path_for_loc(_dod_copy, 'dst', kwargs)
            LogEq.debug("_src_path", _src_path)
            LogEq.debug("_dst_path", _dst_path)
            cls.copytree(_src_path, _dst_path)
