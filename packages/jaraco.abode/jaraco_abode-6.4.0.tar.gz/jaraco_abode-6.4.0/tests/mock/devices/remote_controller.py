"""Mock Abode Remote Controller (Keyfob) Device."""

import jaraco.abode.devices.status as STATUS

DEVICE_ID = 'RF:0000416bb'


def device(devid=DEVICE_ID, status=STATUS.ONLINE, low_battery=False, no_response=False):
    """Remote controller mock device."""
    return dict(
        id=devid,
        type_tag='device_type.remote_controller',
        type='Remote Controller',
        name='Remote',
        area='1',
        zone='4',
        sort_order=None,
        is_window='',
        bypass='0',
        schar_24hr='0',
        sresp_mode_0='0',
        sresp_entry_0='0',
        sresp_exit_0='0',
        sresp_mode_1='5',
        sresp_entry_1='4',
        sresp_exit_1='0',
        sresp_mode_2='0',
        sresp_entry_2='4',
        sresp_exit_2='0',
        sresp_mode_3='0',
        sresp_entry_3='0',
        sresp_exit_3='0',
        version='852_00.00.03.05TC',
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
        actions=[
            {'label': 'Auto Flash', 'value': 'a=1&z=3&req=img;'},
            {'label': 'Never Flash', 'value': 'a=1&z=3&req=img_nf;'},
        ],
        status_icons=[],
        motion_event='1',
        wide_angle='0',
        icon='assets/icons/key-fob.svg',
    )
