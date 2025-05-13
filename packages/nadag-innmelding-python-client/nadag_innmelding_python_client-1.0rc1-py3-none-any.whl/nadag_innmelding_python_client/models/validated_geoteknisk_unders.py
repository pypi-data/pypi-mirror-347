from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.diagnostics_dto import DiagnosticsDto
    from ..models.geoteknisk_unders import GeotekniskUnders


T = TypeVar("T", bound="ValidatedGeotekniskUnders")


@_attrs_define
class ValidatedGeotekniskUnders:
    """GeotekniskUnders med valideringsresultat

    Attributes:
        geoteknisk_unders (Union[Unset, GeotekniskUnders]): geografisk område hvor det finnes eller er planlagt
            geotekniske borehull tilhørende et gitt prosjekt <engelsk>geographical area where there are or are planned
            geotechnical boreholes for a given project</engelsk>
        diagnostics (Union[Unset, DiagnosticsDto]): A Dto for Diagnostic instances, with a list of DiagnosticDto
            instances.
    """

    geoteknisk_unders: Union[Unset, "GeotekniskUnders"] = UNSET
    diagnostics: Union[Unset, "DiagnosticsDto"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        geoteknisk_unders: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.geoteknisk_unders, Unset):
            geoteknisk_unders = self.geoteknisk_unders.to_dict()

        diagnostics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.diagnostics, Unset):
            diagnostics = self.diagnostics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if geoteknisk_unders is not UNSET:
            field_dict["geotekniskUnders"] = geoteknisk_unders
        if diagnostics is not UNSET:
            field_dict["diagnostics"] = diagnostics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.diagnostics_dto import DiagnosticsDto
        from ..models.geoteknisk_unders import GeotekniskUnders

        d = dict(src_dict)
        _geoteknisk_unders = d.pop("geotekniskUnders", UNSET)
        geoteknisk_unders: Union[Unset, GeotekniskUnders]
        if isinstance(_geoteknisk_unders, Unset):
            geoteknisk_unders = UNSET
        else:
            geoteknisk_unders = GeotekniskUnders.from_dict(_geoteknisk_unders)

        _diagnostics = d.pop("diagnostics", UNSET)
        diagnostics: Union[Unset, DiagnosticsDto]
        if isinstance(_diagnostics, Unset):
            diagnostics = UNSET
        else:
            diagnostics = DiagnosticsDto.from_dict(_diagnostics)

        validated_geoteknisk_unders = cls(
            geoteknisk_unders=geoteknisk_unders,
            diagnostics=diagnostics,
        )

        validated_geoteknisk_unders.additional_properties = d
        return validated_geoteknisk_unders

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
