import pytest

from datetime import datetime

from smartcare import data_store
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
    return data_store, patient, practitioner, AppointmentService(data_store)

def test_patient_registeration_with_same_patient_id() -> None:
    """Verify patient_registeration with same patient ID."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'david')
    with pytest.raises(ValueError):
        PatientService(data_store).register_patient('P1', 'paul')

def test_patient_registeration_with_unused_id() -> None:
    """Verify patient_registeration with unused ID."""
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'david')
    patient1 = PatientService(data_store).register_patient('P2', 'Eshay')
    assert patient is not patient1

def test_cancel_appointment_twice_raises_value_error():
    """Verify cancel_appointment twice."""
    data_store = SmartCareDataStore()

    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient_service.register_patient("P001", "Barry")

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

    appointment_service.cancel_appointment("A001")

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A001")

    assert appointment.status is AppointmentStatus.CANCELLED


def test_known_patient_lookup() -> None:
    """Verify known patient lookup."""
    data_store, patient, practitioner, appointment = foundation()
    find = PatientService(data_store).find_patient('P1')
    assert find is patient

def unknown_patient_lookup_reports_absence() -> None:
    """Verify unknown patient lookup reports absence."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)
    with pytest.raises(LookupError):
        service.find_patient("PR999")

def test_known_practitioner_lookup() -> None:
    """Verify known practitioner lookup."""
    data_store, patient, practitioner, appointment = foundation()
    find = PractitionerService(data_store).find_practitioner('D1')
    assert find is practitioner

def test_unknown_practitioner_lookup() -> None:
    """Verify unknown practitioner lookup."""
    data_store = SmartCareDataStore()
    with pytest.raises(LookupError):
        PractitionerService(data_store).find_practitioner('33')

def test_unknown_appointment_lookup() -> None:
    """Verify unknown appointment lookup."""
    data_store = SmartCareDataStore()
    with pytest.raises(LookupError):
        AppointmentService(data_store).find_appointment('33')

def test_practitioner_registration() -> None:
    """Verify practitioner registration."""
    data_store = SmartCareDataStore()
    PractitionerService(data_store,).register_practitioner(
        'D1', 'Taylor Example', 'General')

def test_practitioner_registration_with_same_id() -> None:
    """Verify practitioner registration with same id."""
    data_store, patient, practitioner, appointment = foundation()
    with pytest.raises(ValueError):
        PractitionerService(data_store).register_practitioner('D1', 'steve', 'General')



def test_cancelled_appointment_does_not_stop_new_appointment_at_same_time():
    """Verify cancel_appointment does not stop new appointment at same time."""
    data_store = SmartCareDataStore()

    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient_service.register_patient("P001", "John Doe")
    patient_service.register_patient("P002", "Jeff Doe")

    practitioner_service.register_practitioner(
        "PR001",
        "Dr Smith",
        "General Practice",
    )

    appointment_service.book_appointment(
        "A001",
        "P001",
        "PR001",
        datetime(2026, 1, 1, 10, 0),
    )
    appointment_service.cancel_appointment("A001")

    appointment_service.book_appointment(
        "A002",
        "P002",
        "PR001",
        datetime(2026, 1, 1, 10, 0),
    )


def test_cannot_duplicate_appointments():
    """Verify cannot have duplicate appointments."""
    data_store = SmartCareDataStore()

    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient = patient_service.register_patient(
        "P001",
        "John Doe",
    )

    practitioner = practitioner_service.register_practitioner(
        "PR001",
        "Dr Smith",
        "General Practice",
    )

    appointment_service.book_appointment(
        "A002",
        "P001",
        "PR001",
        datetime(2026, 1, 1, 10, 0),
    )
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
        "A002",
        "P001",
        "PR001",
        datetime(2026, 1, 1, 10, 0),
    )

def known_appointment_lookup() -> None:
    """Verify known appointment lookup reports absence."""
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

    find_appointment = appointment_service.find_appointment('A001')
    assert find_appointment is appointment


