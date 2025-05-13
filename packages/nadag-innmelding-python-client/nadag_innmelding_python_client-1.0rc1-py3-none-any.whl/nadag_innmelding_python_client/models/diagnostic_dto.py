import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.diagnostic_dto_severity import DiagnosticDtoSeverity
    from ..models.identifikasjon import Identifikasjon


T = TypeVar("T", bound="DiagnosticDto")


@_attrs_define
class DiagnosticDto:
    """Result from checking a single validation rule.

    Attributes:
        target (Union[Unset, Identifikasjon]): Unik identifikasjon av et objekt, ivaretatt av den ansvarlige
            produsent/forvalter, som kan benyttes av eksterne applikasjoner som referanse til objektet.

            NOTE1 Denne eksterne objektidentifikasjonen må ikke forveksles med en tematisk objektidentifikasjon, slik som
            f.eks bygningsnummer.

            NOTE 2 Denne unike identifikatoren vil ikke endres i løpet av objektets levetid.
        target_type (Union[Unset, str]):
        property_ (Union[Unset, str]):
        severity (Union[Unset, DiagnosticDtoSeverity]):
        description (Union[Unset, str]):
        timestamp (Union[Unset, datetime.datetime]):
    """

    target: Union[Unset, "Identifikasjon"] = UNSET
    target_type: Union[Unset, str] = UNSET
    property_: Union[Unset, str] = UNSET
    severity: Union[Unset, "DiagnosticDtoSeverity"] = UNSET
    description: Union[Unset, str] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.target, Unset):
            target = self.target.to_dict()

        target_type = self.target_type

        property_ = self.property_

        severity: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.to_dict()

        description = self.description

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target
        if target_type is not UNSET:
            field_dict["targetType"] = target_type
        if property_ is not UNSET:
            field_dict["property"] = property_
        if severity is not UNSET:
            field_dict["severity"] = severity
        if description is not UNSET:
            field_dict["description"] = description
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.diagnostic_dto_severity import DiagnosticDtoSeverity
        from ..models.identifikasjon import Identifikasjon

        d = dict(src_dict)
        _target = d.pop("target", UNSET)
        target: Union[Unset, Identifikasjon]
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = Identifikasjon.from_dict(_target)

        target_type = d.pop("targetType", UNSET)

        property_ = d.pop("property", UNSET)

        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, DiagnosticDtoSeverity]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = DiagnosticDtoSeverity.from_dict(_severity)

        description = d.pop("description", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        diagnostic_dto = cls(
            target=target,
            target_type=target_type,
            property_=property_,
            severity=severity,
            description=description,
            timestamp=timestamp,
        )

        diagnostic_dto.additional_properties = d
        return diagnostic_dto

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
