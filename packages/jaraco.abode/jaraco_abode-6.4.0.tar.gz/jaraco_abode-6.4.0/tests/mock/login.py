"""Mock Abode Login Response."""

from . import AUTH_TOKEN, panel, user


def post_response_ok(auth_token=AUTH_TOKEN):
    """Return the successful login response json."""
    return dict(
        token=auth_token,
        expired_at='2017-06-05 00:14:12',
        initiate_screen='timeline',
        user=user.get_response_ok(),
        panel=panel.get_response_ok(),
        permissions=dict(
            premium_streaming='0',
            guest_app='0',
            family_app='0',
            multiple_accounts='1',
            google_voice='1',
            nest='1',
            alexa='1',
            ifttt='1',
            no_associates='100',
            no_contacts='2',
            no_devices='155',
            no_ipcam='100',
            no_quick_action='25',
            no_automation='75',
            media_storage='3',
            cellular_backup='0',
            cms_duration='',
            cms_included='0',
        ),
        integrations={'nest': {'is_connected': 0, 'is_home_selected': 0}},
    )


def post_response_bad_request():
    """Return the failed login response json."""
    return dict(
        code=400,
        message='Username and password do not match.',
        detail=None,
    )


def post_response_mfa_code_required():
    """Return the MFA code required login response json."""
    return dict(
        code=200,
        mfa_type='google_authenticator',
        detail=None,
    )


def post_response_bad_mfa_code():
    """Return the bad MFA code login response json."""
    return dict(code=400, message='Invalid authentication key.', detail=None)


def post_response_unknown_mfa_type():
    """Return a login response json with an unknown mfa type."""
    return dict(code=200, mfa_type='sms', detail=None)
