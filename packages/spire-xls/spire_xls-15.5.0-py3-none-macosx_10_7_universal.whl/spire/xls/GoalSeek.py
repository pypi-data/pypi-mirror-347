from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.xls.common import *
from spire.xls import *
from ctypes import *
import abc

class GoalSeek (SpireObject) :
    """

    """
    @dispatch
    def __init__(self):
        GetDllLibXls().GoalSeek_CreateGoalSeek.restype = c_void_p
        intPtr = CallCFunction(GetDllLibXls().GoalSeek_CreateGoalSeek)
        super(GoalSeek, self).__init__(intPtr)


    @property
    def MaxIterations(self)->int :
        """

        """
        GetDllLibXls().GoalSeek_get_MaxIterations.argtypes=[c_void_p]
        GetDllLibXls().GoalSeek_get_MaxIterations.restype=c_int
        ret = CallCFunction(GetDllLibXls().GoalSeek_get_MaxIterations, self.Ptr)
        return ret

    @MaxIterations.setter
    def MaxIterations(self, value:int):
        GetDllLibXls().GoalSeek_get_MaxIterations.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibXls().GoalSeek_get_MaxIterations, self.Ptr, value)

    @dispatch
    def TryCalculate(self ,targetCell:'CellRange', targetValue:float , variableCell:'CellRange')->GoalSeekResult:
        """
    <summary>
        Try goal seek calculate.
    </summary>
        """
        intPtrtargetCell:c_void_p = targetCell.Ptr
        intPtrvariableCell:c_void_p = variableCell.Ptr

        GetDllLibXls().GoalSeek_TryCalculate.argtypes=[c_void_p ,c_void_p,c_double,c_void_p]
        GetDllLibXls().GoalSeek_TryCalculate.restype=c_void_p
        intPtr = CallCFunction(GetDllLibXls().GoalSeek_TryCalculate, self.Ptr, intPtrtargetCell,targetValue ,intPtrvariableCell)
        ret = None if intPtr==None else GoalSeekResult(intPtr)
        return ret

    @dispatch
    def TryCalculate(self ,targetCell:'CellRange', targetValue:float , variableCell:'CellRange',guess:float)->GoalSeekResult:
        """
    <summary>
        Try goal seek calculate.
    </summary>
        """
        intPtrtargetCell:c_void_p = targetCell.Ptr
        intPtrvariableCell:c_void_p = variableCell.Ptr

        GetDllLibXls().GoalSeek_TryCalculateTTVG.argtypes=[c_void_p ,c_void_p,c_double,c_void_p,c_double]
        GetDllLibXls().GoalSeek_TryCalculateTTVG.restype=c_void_p
        intPtr = CallCFunction(GetDllLibXls().GoalSeek_TryCalculateTTVG, self.Ptr, intPtrtargetCell,targetValue ,intPtrvariableCell,guess)
        ret = None if intPtr==None else GoalSeekResult(intPtr)
        return ret