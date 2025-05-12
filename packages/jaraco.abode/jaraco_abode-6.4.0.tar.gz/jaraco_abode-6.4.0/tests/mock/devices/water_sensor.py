"""Mock Abode Power Switch Sensor Device."""

import jaraco.abode.devices.status as STATUS

DEVICE_ID = 'RF:00000008'


def device(devid=DEVICE_ID, status=STATUS.OFF, low_battery=False, no_response=False):
    """Water sensor mock device."""
    return dict(
        id=devid,
        type_tag='device_type.water_sensor',
        type='Water Sensor',
        name='Downstairs Bathroo',
        area='1',
        zone='26',
        sort_order='0',
        is_window='0',
        bypass='0',
        schar_24hr='1',
        sresp_mode_0='0',
        sresp_entry_0='0',
        sresp_exit_0='0',
        sresp_mode_1='0',
        sresp_entry_1='0',
        sresp_exit_1='0',
        sresp_mode_2='0',
        sresp_entry_2='0',
        sresp_exit_2='0',
        sresp_mode_3='0',
        sresp_entry_3='0',
        sresp_exit_3='0',
        capture_mode=None,
        origin='abode',
        control_url='',
        deep_link=None,
        status_color='#5cb85c',
        faults={
            'low_battery': int(low_battery),
            'tempered': 0,
            'supervision': 0,
            'out_of_order': 0,
            'no_response': int(no_response),
        },
        status=status,
        statuses={'hvac_mode': None},
        status_ex='',
        actions=[],
        status_icons=[],
        icon='assets/icons/water-value-shutoff.svg',
    )
