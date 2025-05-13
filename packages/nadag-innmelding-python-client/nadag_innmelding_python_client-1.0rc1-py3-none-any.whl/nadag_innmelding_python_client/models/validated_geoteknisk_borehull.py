from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.diagnostics_dto import DiagnosticsDto
    from ..models.geoteknisk_borehull import GeotekniskBorehull


T = TypeVar("T", bound="ValidatedGeotekniskBorehull")


@_attrs_define
class ValidatedGeotekniskBorehull:
    """GeotekniskBorehull med valideringsresultat

    Attributes:
        geoteknisk_borehull (Union[Unset, GeotekniskBorehull]): geografisk område representert ved et punkt som er den
            logiske enhet for tolking av laginndeling og egenskaper til de forskjellige jordlag <engelsk>geographical area
            represented by a location which is the logical unit for interpretation of stratification and properties for the
            different strata </engelsk>
        diagnostics (Union[Unset, DiagnosticsDto]): A Dto for Diagnostic instances, with a list of DiagnosticDto
            instances.
    """

    geoteknisk_borehull: Union[Unset, "GeotekniskBorehull"] = UNSET
    diagnostics: Union[Unset, "DiagnosticsDto"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        geoteknisk_borehull: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.geoteknisk_borehull, Unset):
            geoteknisk_borehull = self.geoteknisk_borehull.to_dict()

        diagnostics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.diagnostics, Unset):
            diagnostics = self.diagnostics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if geoteknisk_borehull is not UNSET:
            field_dict["geotekniskBorehull"] = geoteknisk_borehull
        if diagnostics is not UNSET:
            field_dict["diagnostics"] = diagnostics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.diagnostics_dto import DiagnosticsDto
        from ..models.geoteknisk_borehull import GeotekniskBorehull

        d = dict(src_dict)
        _geoteknisk_borehull = d.pop("geotekniskBorehull", UNSET)
        geoteknisk_borehull: Union[Unset, GeotekniskBorehull]
        if isinstance(_geoteknisk_borehull, Unset):
            geoteknisk_borehull = UNSET
        else:
            geoteknisk_borehull = GeotekniskBorehull.from_dict(_geoteknisk_borehull)

        _diagnostics = d.pop("diagnostics", UNSET)
        diagnostics: Union[Unset, DiagnosticsDto]
        if isinstance(_diagnostics, Unset):
            diagnostics = UNSET
        else:
            diagnostics = DiagnosticsDto.from_dict(_diagnostics)

        validated_geoteknisk_borehull = cls(
            geoteknisk_borehull=geoteknisk_borehull,
            diagnostics=diagnostics,
        )

        validated_geoteknisk_borehull.additional_properties = d
        return validated_geoteknisk_borehull

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
