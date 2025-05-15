from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.xls.common import *
from spire.xls import *
from ctypes import *
import abc

class GoalSeekResult (SpireObject) :
    


    
    def Determine(self):
        """

        """
        GetDllLibXls().GoalSeekResult_Determine.argtypes=[c_void_p]
        CallCFunction(GetDllLibXls().GoalSeekResult_Determine, self.Ptr)

    @property
    def TargetCellName(self)->str:
        GetDllLibXls().GoalSeekResult_get_TargetCellName.argtypes=[c_void_p]
        GetDllLibXls().GoalSeekResult_get_TargetCellName.restype=c_void_p
        ret = CallCFunction(GetDllLibXls().GoalSeekResult_get_TargetCellName, self.Ptr)
        return PtrToStr(ret)

    @property
    def VariableCellName(self)->str:
        GetDllLibXls().GoalSeekResult_get_VariableCellName.argtypes=[c_void_p]
        GetDllLibXls().GoalSeekResult_get_VariableCellName.restype=c_void_p
        ret = CallCFunction(GetDllLibXls().GoalSeekResult_get_VariableCellName, self.Ptr)
        return PtrToStr(ret)
    

    @property
    def Iterations(self)->int:
        GetDllLibXls().GoalSeekResult_get_Iterations.argtypes=[c_void_p]
        GetDllLibXls().GoalSeekResult_get_Iterations.restype=c_int
        ret = CallCFunction(GetDllLibXls().GoalSeekResult_get_Iterations, self.Ptr)
        return ret

    @property
    def TargetValue(self)->float:
        GetDllLibXls().GoalSeekResult_get_TargetValue.argtypes=[c_void_p]
        GetDllLibXls().GoalSeekResult_get_TargetValue.restype=c_double
        ret = CallCFunction(GetDllLibXls().GoalSeekResult_get_TargetValue, self.Ptr)
        return ret

    

    @property
    def GuessResult(self)->float:
        GetDllLibXls().GoalSeekResult_get_GuessResult.argtypes=[c_void_p]
        GetDllLibXls().GoalSeekResult_get_GuessResult.restype=c_double
        ret = CallCFunction(GetDllLibXls().GoalSeekResult_get_GuessResult, self.Ptr)
        return ret