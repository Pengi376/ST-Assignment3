import pytest

from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

def foundation() -> tuple[
    SmartCareDataStore,
    Patient,
    Practitioner,
    AppointmentService,
]:
    """Create fresh registered participants and services for a supplied
    check.
    """
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(
        data_store,
    ).register_practitioner('D1', 'Taylor Example', 'General')
    return (data_store, patient, practitioner, AppointmentService(data_store))

def test_required_fields() -> None:
    """Verify required fields."""
    with pytest.raises(ValueError):
        Patient(' ', 'Alex Example')
    with pytest.raises(ValueError):
        Patient('P1', ' ')
    with pytest.raises(ValueError):
        Patient(' ', ' ')
    with pytest.raises(ValueError):
        Practitioner('D1', 'Taylor Example', '')
    with pytest.raises(ValueError):
        Practitioner('D1', ' ', 'General')
    with pytest.raises(ValueError):
        Practitioner(' ', 'Taylor Example', 'General')
    with pytest.raises(ValueError):
        Practitioner(' ', ' ', '')

def test_registration_and_booking() -> None:
    """Verify registration and booking."""
    data_store, patient, practitioner, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )
    assert appointment_service.find_appointment('A1') is appointment
    assert appointment.patient is patient and appointment.practitioner is practitioner
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [appointment]

def test_cancel_appointment_changes_status_and_returns_same_object():
    """Verify cancel_appointment changes status and returns."""
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient_service.register_patient("P001", "John Doe")

    practitioner_service.register_practitioner(
        "PR001",
        "Dr Smith",
        "General Practice",
    )

    appointment = appointment_service.book_appointment(
        "A001",
        "P001",
        "PR001",
        datetime(2026, 1, 1, 10, 0),
    )

    result = appointment_service.cancel_appointment("A001")

    assert result is appointment
    assert result.status is AppointmentStatus.CANCELLED

def test_appointment_feilds_not_empty() -> None:
    """Verify appointment feilds not empty."""
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)
    patient_service.register_patient("P001", "John Doe")
    practitioner_service.register_practitioner(
        "PR001",
        "Dr Smith",
        "General Practice",
    )
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            " ",
            "P001",
            "PR001",
            datetime(2026, 1, 1, 10, 0),
         )
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            "A001",
            " ",
            "PR001",
            datetime(2026, 1, 1, 10, 0),
        )
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            "A001",
            "P001",
            " ",
            datetime(2026, 1, 1, 10, 0),
        )
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            "A001",
            "P001",
            "PR001",
            datetime(0000, 0, 0, 0, 0),
        )

