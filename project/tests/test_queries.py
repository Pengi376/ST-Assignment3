from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import (
    appointment_sort_key,
    select_appointments,
)


def make_appointment(
    appointment_id: str,
    practitioner: Practitioner,
    date_time: datetime,
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    """Create an appointment for query tests."""
    return Appointment(
        appointment_id,
        Patient('P1', 'Alex Example'),
        practitioner,
        date_time,
        status,
    )


def test_select_appointments_filters_practitioner_and_status() -> None:
    """Default includes all statuses; explicit statuses filter exactly."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    other_practitioner = Practitioner('D2', 'Morgan Example', 'General')
    when = datetime(2026, 10, 1, 9)
    scheduled = make_appointment('A1', practitioner, when)
    cancelled = make_appointment(
        'A2', practitioner, when, AppointmentStatus.CANCELLED,
    )
    completed = make_appointment(
        'A3', practitioner, when, AppointmentStatus.COMPLETED,
    )
    other = make_appointment('A0', other_practitioner, when)
    source = [completed, other, scheduled, cancelled]

    assert select_appointments(source, 'D1') == [
        scheduled, cancelled, completed,
    ]
    for status, expected in (
        (AppointmentStatus.SCHEDULED, [scheduled]),
        (AppointmentStatus.CANCELLED, [cancelled]),
        (AppointmentStatus.COMPLETED, [completed]),
    ):
        assert select_appointments(source, 'D1', status) == expected
    assert select_appointments(
        source, 'D2', AppointmentStatus.COMPLETED,
    ) == []


def test_select_appointments_orders_without_mutating_source() -> None:
    """Sort by time then ID while preserving source order and fields."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    later = make_appointment(
        'A1', practitioner, datetime(2026, 10, 1, 10),
    )
    equal_time_z = make_appointment(
        'A9', practitioner, datetime(2026, 10, 1, 9),
    )
    equal_time_a = make_appointment(
        'A2', practitioner, datetime(2026, 10, 1, 9),
    )
    source = [later, equal_time_z, equal_time_a]
    original_order = source.copy()
    original_fields = [
        (item.appointment_id, item.date_time, item.status, item.practitioner)
        for item in source
    ]

    result = select_appointments(source, 'D1')

    assert result == [equal_time_a, equal_time_z, later]
    assert source == original_order
    assert [
        (item.appointment_id, item.date_time, item.status, item.practitioner)
        for item in source
    ] == original_fields
    assert result is not source
    assert all(actual is expected for actual, expected in zip(
        result, [equal_time_a, equal_time_z, later],
    ))


def test_select_appointments_returns_fresh_lists_and_repeats_cleanly() -> None:
    """Empty, sorted and unsorted calls return distinct result lists."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    sorted_items = [
        make_appointment('A1', practitioner, datetime(2026, 10, 1, 9)),
        make_appointment('A2', practitioner, datetime(2026, 10, 1, 10)),
    ]
    unsorted_items = list(reversed(sorted_items))

    empty_source: list[Appointment] = []
    empty_result = select_appointments(empty_source, 'D1')
    assert empty_result == []
    assert empty_result is not empty_source

    for source in (sorted_items, unsorted_items):
        before = source.copy()
        first = select_appointments(source, 'D1')
        second = select_appointments(source, 'D1')
        expected = sorted(sorted_items, key=appointment_sort_key)
        assert first == expected and second == expected
        assert first is not source and second is not source and first is not second
        assert source == before
        assert all(actual is expected_item for actual, expected_item in zip(
            first, expected,
        ))

    first.clear()
    assert len(sorted_items) == 2


def test_appointment_sort_key_and_query_use_named_key(monkeypatch) -> None:
    """The direct key contract and its use by query sorting are verified."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    later = make_appointment(
        'A1', practitioner, datetime(2026, 10, 1, 10),
    )
    earlier = make_appointment(
        'A2', practitioner, datetime(2026, 10, 1, 9),
    )
    assert appointment_sort_key(earlier) == (
        datetime(2026, 10, 1, 9),
        'A2',
    )

    import smartcare.queries as queries

    key_calls: list[Appointment] = []

    def recording_key(appointment: Appointment) -> tuple[datetime, str]:
        key_calls.append(appointment)
        return appointment_sort_key(appointment)

    monkeypatch.setattr(queries, 'appointment_sort_key', recording_key)
    assert queries.select_appointments([later, earlier], 'D1') == [
        earlier, later,
    ]
    assert key_calls == [later, earlier]
