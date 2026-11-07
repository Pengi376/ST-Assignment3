"""Console parsing, formatting, demo and interactive menu."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Run the interactive menu with one in-memory store for this session."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    print("\n============================================================\n "
          "               SMARTCARE Interactive Console\n"
          "============================================================\n"
          "Session data is temporary and will be discarded when you exit.")

    while True:
        print(
            '\nSmartCare Main Menu\n'
            '------------------------------------------------------------\n'
            '[1] Register patient \n'
            '[2] Find patient\n'
            '[3] Register practitioner \n'
            '[4] Find practitioner\n'
            '[5] Book appointment\n'
            '[6] Cancel appointment\n'
            '[7] Find appointment\n'
            '[8] List practitioner appointments\n'
            '[0] Exit\n'
            '------------------------------------------------------------\n'
        )
        try:
            choice = input('Choice: ').strip()
            if choice == '0':
                print('Session ended; in-memory data discarded.')
                return
            if choice not in {'1', '2', '3', '4', '5', '6', '7', '8'}:
                print('Unknown menu choice. Choose an option from 0 to 8.')
                continue

            if choice == '1':
                patient = patients.register_patient(
                    input('Patient ID: '),
                    input('Patient name: '),
                )
                print(f'Patient registered: {patient.patient_id}')
            elif choice == '2':
                patient = patients.find_patient(input('Patient ID: '))
                print(f'Patient found: {patient.patient_id} - {patient.name}')
            elif choice == '3':
                practitioner = practitioners.register_practitioner(
                    input('Practitioner ID: '),
                    input('Practitioner name: '),
                    input('Specialty: '),
                )
                print(f'Practitioner registered: {practitioner.practitioner_id}')
            elif choice == '4':
                practitioner = practitioners.find_practitioner(
                    input('Practitioner ID: '),
                )
                print(
                    f'Practitioner found: {practitioner.practitioner_id} - '
                    f'{practitioner.name} ({practitioner.specialty})',
                )
            elif choice == '5':
                appointment_id = input('Appointment ID: ')
                patient_id = input('Patient ID: ')
                practitioner_id = input('Practitioner ID: ')
                date_time = parse_date_time(
                    input('Date/time (YYYY-MM-DD HH:MM): '),
                )
                appointment = appointments.book_appointment(
                    appointment_id,
                    patient_id,
                    practitioner_id,
                    date_time,
                )
                print(f'Appointment booked: {format_appointment(appointment)}')
            elif choice == '6':
                appointment = appointments.cancel_appointment(
                    input('Appointment ID: '),
                )
                print(f'Appointment cancelled: {format_appointment(appointment)}')
            elif choice == '7':
                appointment = appointments.find_appointment(
                    input('Appointment ID: '),
                )
                print(f'Appointment found: {format_appointment(appointment)}')
            else:
                practitioner_id = input('Practitioner ID: ')
                status_text = input(
                    'Status (scheduled/cancelled/completed; blank for all): ',
                ).strip().lower()
                if status_text:
                    try:
                        status = AppointmentStatus(status_text)
                    except ValueError:
                        raise ValueError(
                            'Status must be scheduled, cancelled or completed',
                        ) from None
                else:
                    status = None
                found = appointments.list_practitioner_appointments(
                    practitioner_id,
                    status,
                )
                if not found:
                    print('No matching appointments found.')
                else:
                    for appointment in found:
                        print(format_appointment(appointment))
        except (ValueError, LookupError) as error:
            print(f'Error: {error}')
        except EOFError:
            print('Input ended; session data discarded.')
            return
