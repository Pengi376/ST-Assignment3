from smartcare import console
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus


def test_menu_reuses_session_store_and_recovers_from_invalid_commands(
    monkeypatch,
    capsys,
) -> None:
    """Keep session data across menu actions and recover without bad writes."""
    stores: list[SmartCareDataStore] = []

    def create_store() -> SmartCareDataStore:
        store = SmartCareDataStore()
        stores.append(store)
        return store

    inputs = iter([
        '1', 'P1', 'Alex Example',
        '1', 'P1', 'Replacement Patient',
        '3', 'D1', 'Taylor Example', 'General',
        '3', 'D1', 'Replacement Practitioner', 'Other',
        '5', 'A1', 'P1', 'D1', 'not-a-date',
        '5', 'A1', 'P999', 'D1', '2026-10-01 09:00',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '5', 'A1', 'P1', 'D1', '2026-10-01 10:00',
        '6', 'A1',
        '7', 'A1',
        '8', 'D1', 'scheduled',
        '8', 'D1', '',
        '8', 'missing', '',
        '8', 'D1', 'invalid',
        '2', 'P1',
        '4', 'D1',
        '9',
        '0',
    ])
    monkeypatch.setattr(console, SmartCareDataStore.__name__, create_store)
    monkeypatch.setattr('builtins.input', lambda _prompt='': next(inputs))

    console.run_menu()

    output = capsys.readouterr().out
    assert len(stores) == 1
    assert len(stores[0].list_patients()) == 1
    assert len(stores[0].list_practitioners()) == 1
    assert stores[0].find_patient('P1').name == 'Alex Example'
    assert stores[0].find_practitioner('D1').name == 'Taylor Example'
    stored_appointments = stores[0].list_appointments()
    assert len(stored_appointments) == 1
    assert stored_appointments[0].appointment_id == 'A1'
    assert stored_appointments[0].status is AppointmentStatus.CANCELLED
    assert 'Use date/time format YYYY-MM-DD HH:MM' in output
    assert 'Patient not found' in output
    assert 'Appointment ID already exists' in output
    assert 'Appointment cancelled:' in output
    assert 'Appointment found:' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'No matching appointments found.' in output
    assert 'Practitioner not found' in output
    assert 'Status must be scheduled, cancelled or completed' in output
    assert 'Unknown menu choice' in output
    assert 'Session ended; in-memory data discarded.' in output


def test_menu_recovers_from_blank_unknown_and_impossible_date_inputs(
    monkeypatch,
    capsys,
) -> None:
    """Rejected blank and lookup inputs leave session state unchanged."""
    stores: list[SmartCareDataStore] = []

    def create_store() -> SmartCareDataStore:
        store = SmartCareDataStore()
        stores.append(store)
        return store

    inputs = iter([
        '1', ' ', 'Invalid Patient',
        '1', 'P1', 'Alex Example',
        '3', ' ', 'Invalid Practitioner', 'General',
        '3', 'D1', 'Taylor Example', 'General',
        '2', '',
        '4', ' ',
        '7', ' ',
        '7', 'missing',
        '6', ' ',
        '6', 'missing',
        '5', 'A1', 'P1', 'D1', '2026-02-30 09:00',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '0',
    ])
    monkeypatch.setattr(console, SmartCareDataStore.__name__, create_store)
    monkeypatch.setattr('builtins.input', lambda _prompt='': next(inputs))

    console.run_menu()

    output = capsys.readouterr().out
    assert len(stores) == 1
    store = stores[0]
    assert [patient.patient_id for patient in store.list_patients()] == ['P1']
    assert [
        practitioner.practitioner_id
        for practitioner in store.list_practitioners()
    ] == ['D1']
    assert [item.appointment_id for item in store.list_appointments()] == ['A1']
    assert 'Patient ID cannot be blank' in output
    assert 'Practitioner ID cannot be blank' in output
    assert output.count('cannot be blank') >= 4
    assert output.count('Appointment not found') == 2
    assert 'Appointment ID cannot be blank' in output
    assert 'Invalid calendar date/time' in output
    assert 'Appointment booked:' in output
    assert 'Session ended; in-memory data discarded.' in output


def test_menu_handles_conflicts_freed_slots_and_repeated_cancellation(
    monkeypatch,
    capsys,
) -> None:
    """Conflicts reject bookings while cancellation frees the slot."""
    stores: list[SmartCareDataStore] = []

    def create_store() -> SmartCareDataStore:
        store = SmartCareDataStore()
        stores.append(store)
        return store

    inputs = iter([
        '1', 'P1', 'Alex Example',
        '1', 'P2', 'Sam Example',
        '3', 'D1', 'Taylor Example', 'General',
        '3', 'D2', 'Morgan Example', 'General',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '5', 'A2', 'P2', 'D1', '2026-10-01 09:00',
        '5', 'A3', 'P2', 'D2', '2026-10-01 09:00',
        '6', 'A1',
        '5', 'A4', 'P2', 'D1', '2026-10-01 09:00',
        '6', 'A1',
        '0',
    ])
    monkeypatch.setattr(console, SmartCareDataStore.__name__, create_store)
    monkeypatch.setattr('builtins.input', lambda _prompt='': next(inputs))

    console.run_menu()

    output = capsys.readouterr().out
    assert len(stores) == 1
    appointments = stores[0].list_appointments()
    assert [appointment.appointment_id for appointment in appointments] == [
        'A1', 'A3', 'A4',
    ]
    assert appointments[0].status is AppointmentStatus.CANCELLED
    assert appointments[1].practitioner.practitioner_id == 'D2'
    assert appointments[2].practitioner.practitioner_id == 'D1'
    assert output.count('Practitioner already has a SCHEDULED appointment') == 1
    assert output.count('Only SCHEDULED appointments may be cancelled') == 1
    assert output.count('Appointment booked:') == 3
    assert 'Appointment cancelled:' in output
    assert 'Session ended; in-memory data discarded.' in output
