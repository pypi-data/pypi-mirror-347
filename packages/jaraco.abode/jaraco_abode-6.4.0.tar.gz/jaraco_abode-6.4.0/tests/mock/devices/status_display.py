"""Mock Abode Status Display Device."""

import jaraco.abode.devices.status as STATUS

DEVICE_ID = 'ZB:00000004'


def device(devid=DEVICE_ID, status=STATUS.ONLINE, low_battery=False, no_response=False):
    """Status display mock device."""
    return dict(
        id=devid,
        type_tag='device_type.bx',
        type='Status Display',
        name='Status Indicator',
        area='1',
        zone='11',
        sort_order=None,
        is_window='',
        bypass='0',
        schar_24hr='0',
        sresp_mode_0='5',
        sresp_entry_0='5',
        sresp_exit_0='5',
        sresp_mode_1='5',
        sresp_entry_1='5',
        sresp_exit_1='5',
        sresp_mode_2='5',
        sresp_entry_2='5',
        sresp_exit_2='5',
        sresp_mode_3='5',
        sresp_entry_3='5',
        sresp_exit_3='5',
        version='SSL_00.00.03.03TC',
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
        siren_default=None,
        icon='assets/icons/unknown.svg',
    )
