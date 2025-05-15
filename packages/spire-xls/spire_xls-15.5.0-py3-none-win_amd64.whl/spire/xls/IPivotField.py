from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.xls.common import *
from spire.xls import *
from ctypes import *
import abc

class IPivotField (abc.ABC) :
    """

    """

    @abc.abstractmethod
    def AddLabelFilter(self ,type:'PivotLabelFilterType',value1:'SpireObject',value2:'SpireObject'):
        """
    <summary>
        Add label filter for pivot field, only for row and column field.
    </summary>
    <param name="type">Filter type.</param>
    <param name="value1">First filter value.</param>
    <param name="value2">Second filter value, only for Between and NotBetween type.</param>
        """
        pass



    @abc.abstractmethod
    def AddValueFilter(self ,type:'PivotValueFilterType',dataField:'IPivotDataField',value1:'SpireObject',value2:'SpireObject'):
        """
    <summary>
        Add value filter for pivot field, only for row and column field.
    </summary>
    <param name="type">Filter type.</param>
    <param name="dataField">Filter data field.</param>
    <param name="value1">First filter value.</param>
    <param name="value2">Second filter value, only for Between and NotBetween type.</param>
        """
        pass
    @dispatch

    @abc.abstractmethod
    def CreateGroup(self ,startValue:float,endValue:float,intervalValue:float):
        """
    <summary>
        Create group for current field.
    </summary>
    <param name="startValue">The start number value</param>
    <param name="endValue">The end number value</param>
    <param name="intervalValue">The interval number value</param>
        """
        pass

    @property

    @abc.abstractmethod
    def CustomName(self)->str:
        """

        """
        pass

    @CustomName.setter
    @abc.abstractmethod
    def CustomName(self, value:str):
        """

        """
        pass

    @property

    @abc.abstractmethod
    def Name(self)->str:
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Axis(self)->'AxisTypes':
        """

        """
        pass


    @Axis.setter
    @abc.abstractmethod
    def Axis(self, value:'AxisTypes'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def NumberFormat(self)->str:
        """

        """
        pass


    @NumberFormat.setter
    @abc.abstractmethod
    def NumberFormat(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Subtotals(self)->'SubtotalTypes':
        """

        """
        pass


    @Subtotals.setter
    @abc.abstractmethod
    def Subtotals(self, value:'SubtotalTypes'):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def CanDragToRow(self)->bool:
        """

        """
        pass


    @CanDragToRow.setter
    @abc.abstractmethod
    def CanDragToRow(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def CanDragToColumn(self)->bool:
        """

        """
        pass


    @CanDragToColumn.setter
    @abc.abstractmethod
    def CanDragToColumn(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def CanDragToPage(self)->bool:
        """

        """
        pass


    @CanDragToPage.setter
    @abc.abstractmethod
    def CanDragToPage(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def CanDragOff(self)->bool:
        """

        """
        pass


    @CanDragOff.setter
    @abc.abstractmethod
    def CanDragOff(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def ShowBlankRow(self)->bool:
        """

        """
        pass


    @ShowBlankRow.setter
    @abc.abstractmethod
    def ShowBlankRow(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def CanDragToData(self)->bool:
        """

        """
        pass


    @CanDragToData.setter
    @abc.abstractmethod
    def CanDragToData(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def IsFormulaField(self)->bool:
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Formula(self)->str:
        """

        """
        pass


    @Formula.setter
    @abc.abstractmethod
    def Formula(self, value:str):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def RepeatItemLabels(self)->bool:
        """

        """
        pass


    @RepeatItemLabels.setter
    @abc.abstractmethod
    def RepeatItemLabels(self, value:bool):
        """

        """
        pass


