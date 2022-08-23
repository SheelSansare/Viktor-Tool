import abc
import os
from .api_v1 import API as API
from .core import Color as Color, File as File
from .geometry import GeoPoint as GeoPoint, GeoPolygon as GeoPolygon, GeoPolyline as GeoPolyline, Point as Point, TransformableObject as TransformableObject
from abc import ABC, abstractmethod
from collections import OrderedDict
from enum import Enum
from io import BytesIO, StringIO
from typing import Any, Callable, Dict, List, Sequence, Tuple, Type, Union

class ViewError(Exception): ...
class SummaryError(Exception): ...

class DataStatus(Enum):
    INFO: DataStatus
    SUCCESS: DataStatus
    WARNING: DataStatus
    ERROR: DataStatus

class DataItem:
    def __init__(self, label: str, value: Union[str, float, None], subgroup: DataGroup = ..., *, prefix: str = ..., suffix: str = ..., number_of_decimals: int = ..., status: DataStatus = ..., status_message: str = ..., explanation_label: str = ...) -> None: ...
    @property
    def subgroup(self) -> DataGroup: ...

class DataGroup(OrderedDict):
    def __init__(self, *args: DataItem, **kwargs: DataItem) -> None: ...
    @classmethod
    def from_data_groups(cls, groups: List[DataGroup]) -> DataGroup: ...

class MapEntityLink:
    def __init__(self, label: str, entity_id: int) -> None: ...

class MapFeature(ABC, metaclass=abc.ABCMeta):
    def __init__(self, *, title: str = ..., description: str = ..., color: Color = ..., entity_links: List[MapEntityLink] = ..., identifier: Union[int, str] = ...) -> None: ...

class MapPoint(MapFeature):
    def __init__(self, lat: float, lon: float, alt: float = ..., *, icon: str = ..., **kwargs: Any) -> None: ...
    @classmethod
    def from_geo_point(cls, point: GeoPoint, *, icon: str = ..., **kwargs: Any) -> MapPoint: ...
    @property
    def lat(self) -> float: ...
    @property
    def lon(self) -> float: ...
    @property
    def alt(self) -> float: ...

class MapPolyline(MapFeature):
    def __init__(self, *points: MapPoint, **kwargs: Any) -> None: ...
    @classmethod
    def from_geo_polyline(cls, polyline: GeoPolyline, **kwargs: Any) -> MapPolyline: ...
    @property
    def points(self) -> List[MapPoint]: ...

class MapLine(MapPolyline):
    def __init__(self, start_point: MapPoint, end_point: MapPoint, **kwargs: Any) -> None: ...
    @property
    def start_point(self) -> MapPoint: ...
    @property
    def end_point(self) -> MapPoint: ...

class MapPolygon(MapFeature):
    def __init__(self, points: List[MapPoint], *, holes: List[MapPolygon] = ..., **kwargs: Any) -> None: ...
    @property
    def points(self) -> List[MapPoint]: ...
    @property
    def holes(self) -> List[MapPolygon]: ...
    @classmethod
    def from_geo_polygon(cls, polygon: GeoPolygon, **kwargs: Any) -> MapPolygon: ...

class MapLegend:
    def __init__(self, entries: List[Tuple[Color, str]]) -> None: ...

class MapLabel:
    def __init__(self, lat: float, lon: float, text: str, scale: float, *, fixed_size: bool = ...) -> None: ...

class Label:
    size_factor: Any
    color: Any
    def __init__(self, point: Point, *text: str, size_factor: float = ..., color: Color = ...) -> None: ...
    @property
    def point(self) -> Point: ...
    @property
    def text(self) -> Union[str, Tuple[str, ...]]: ...
    def serialize(self) -> dict: ...

class _SubResult(ABC, metaclass=abc.ABCMeta): ...

class _ViewResult(ABC, metaclass=abc.ABCMeta):
    def __init__(self, version: int) -> None: ...

class _DataSubResult(_SubResult):
    def __init__(self, data: DataGroup) -> None: ...

class _GeometrySubResult(_SubResult):
    def __init__(self, geometry: Union[TransformableObject, Sequence[TransformableObject], File], labels: List[Label] = ...) -> None: ...

class _ImageSubResult(_SubResult):
    def __init__(self, image: BytesIO, image_type: str) -> None: ...

class _GeoJSONSubResult(_SubResult):
    def __init__(self, geojson: dict, labels: List[MapLabel] = ..., legend: MapLegend = ..., interaction_groups: Dict[str, Sequence[Union[int, str, MapFeature]]] = ...) -> None: ...

class _WebSubResult(_SubResult):
    def __init__(self, *, html: StringIO = ..., url: str = ...) -> None: ...

class _PlotlySubResult(_SubResult):
    def __init__(self, figure: Union[str, dict]) -> None: ...

class _PDFSubResult(_SubResult):
    def __init__(self, *, file: File = ..., url: str = ...) -> None: ...

class GeometryResult(_ViewResult):
    def __init__(self, geometry: Union[TransformableObject, Sequence[TransformableObject], File], labels: List[Label] = ...) -> None: ...

class GeometryAndDataResult(_ViewResult):
    def __init__(self, geometry: Union[TransformableObject, Sequence[TransformableObject], File], data: DataGroup, labels: List[Label] = ...) -> None: ...

class DataResult(_ViewResult):
    def __init__(self, data: DataGroup) -> None: ...

class _ImageResult(_ViewResult):
    def __init__(self, image: BytesIO, image_type: str) -> None: ...

class _ImageAndDataResult(_ViewResult):
    def __init__(self, image: BytesIO, image_type: str, data: DataGroup) -> None: ...

class PNGResult(_ImageResult):
    def __init__(self, image: BytesIO) -> None: ...
    @classmethod
    def from_path(cls, file_path: Union[str, bytes, os.PathLike]) -> PNGResult: ...

class PNGAndDataResult(_ImageAndDataResult):
    def __init__(self, image: BytesIO, data: DataGroup) -> None: ...

class JPGResult(_ImageResult):
    def __init__(self, image: BytesIO) -> None: ...
    @classmethod
    def from_path(cls, file_path: Union[str, bytes, os.PathLike]) -> JPGResult: ...

class JPGAndDataResult(_ImageAndDataResult):
    def __init__(self, image: BytesIO, data: DataGroup) -> None: ...

class SVGResult(_ImageResult):
    def __init__(self, image: StringIO) -> None: ...
    @classmethod
    def from_path(cls, file_path: Union[str, bytes, os.PathLike]) -> SVGResult: ...

class SVGAndDataResult(_ImageAndDataResult):
    def __init__(self, image: StringIO, data: DataGroup) -> None: ...

class GeoJSONResult(_ViewResult):
    def __init__(self, geojson: dict, labels: List[MapLabel] = ..., legend: MapLegend = ..., *, interaction_groups: Dict[str, Sequence[Union[int, str, MapFeature]]] = ...) -> None: ...

class GeoJSONAndDataResult(_ViewResult):
    def __init__(self, geojson: dict, data: DataGroup, labels: List[MapLabel] = ..., legend: MapLegend = ..., *, interaction_groups: Dict[str, Sequence[Union[int, str, MapFeature]]] = ...) -> None: ...

class MapResult(GeoJSONResult):
    def __init__(self, features: List[MapFeature], labels: List[MapLabel] = ..., legend: MapLegend = ..., *, interaction_groups: Dict[str, Sequence[Union[int, str, MapFeature]]] = ...) -> None: ...

class MapAndDataResult(GeoJSONAndDataResult):
    def __init__(self, features: List[MapFeature], data: DataGroup, labels: List[MapLabel] = ..., legend: MapLegend = ..., *, interaction_groups: Dict[str, Sequence[Union[int, str, MapFeature]]] = ...) -> None: ...

class WebResult(_ViewResult):
    def __init__(self, *, html: StringIO = ..., url: str = ...) -> None: ...
    @classmethod
    def from_path(cls, file_path: Union[str, bytes, os.PathLike]) -> WebResult: ...

class WebAndDataResult(_ViewResult):
    def __init__(self, *, html: StringIO = ..., url: str = ..., data: DataGroup = ...) -> None: ...

class PlotlyResult(_ViewResult):
    def __init__(self, figure: Union[str, dict]) -> None: ...

class PlotlyAndDataResult(_ViewResult):
    def __init__(self, figure: Union[str, dict], data: DataGroup) -> None: ...

class PDFResult(_ViewResult):
    def __init__(self, *, file: File = ..., url: str = ...) -> None: ...
    @classmethod
    def from_path(cls, file_path: Union[str, bytes, os.PathLike]) -> PDFResult: ...

class SummaryItem:
    def __init__(self, label: str, item_type: Type[Union[str, float]], source: str, value_path: str, *, suffix: str = ..., prefix: str = ...) -> None: ...

class Summary(OrderedDict):
    def __init__(self, **items: SummaryItem) -> None: ...

class View(ABC, metaclass=abc.ABCMeta):
    def __init__(self, label: str, duration_guess: int, *, description: str = ..., update_label: str = ..., **kwargs: Any) -> None: ...
    def __call__(self, view_function: Callable) -> Callable: ...
    @property
    @abstractmethod
    def result_type(self) -> Type[_ViewResult]: ...

class GeometryView(View):
    result_type: Any
    def __init__(self, label: str, duration_guess: int, *, description: str = ..., update_label: str = ..., view_mode: str = ..., default_shadow: bool = ..., up_axis: str = ...) -> None: ...

class DataView(View):
    result_type: Any

class GeometryAndDataView(View):
    result_type: Any
    def __init__(self, label: str, duration_guess: int, *, description: str = ..., update_label: str = ..., view_mode: str = ..., default_shadow: bool = ..., up_axis: str = ...) -> None: ...

class SVGView(View):
    result_type: Any

class SVGAndDataView(View):
    result_type: Any

class GeoJSONView(View):
    result_type: Any

class GeoJSONAndDataView(View):
    result_type: Any

class MapView(View):
    result_type: Any

class MapAndDataView(View):
    result_type: Any

class PNGView(View):
    result_type: Any

class PNGAndDataView(View):
    result_type: Any

class JPGView(View):
    result_type: Any

class JPGAndDataView(View):
    result_type: Any

class WebView(View):
    result_type: Any

class WebAndDataView(View):
    result_type: Any

class PlotlyView(View):
    result_type: Any

class PlotlyAndDataView(View):
    result_type: Any

class PDFView(View):
    result_type: Any

class InteractionEvent:
    type: Any
    value: Any
    def __init__(self, event_type: str, value: Any) -> None: ...
