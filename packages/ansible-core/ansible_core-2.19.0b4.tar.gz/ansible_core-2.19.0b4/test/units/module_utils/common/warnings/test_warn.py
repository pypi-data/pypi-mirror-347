# -*- coding: utf-8 -*-
# (c) 2019 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import pytest
import typing as t

from ansible.module_utils._internal import _traceback
from ansible.module_utils.common import warnings
from ansible.module_utils.common.messages import WarningSummary, Detail

from ansible.module_utils.common.warnings import warn
from units.mock.messages import make_summary
from units.mock.module import ModuleEnvMocker

pytestmark = pytest.mark.usefixtures("module_env_mocker")


def test_warn():
    warn('Warning message')
    assert warnings.get_warning_messages() == ('Warning message',)
    assert warnings.get_warnings() == [make_summary(WarningSummary, Detail(msg='Warning message'))]


def test_multiple_warnings():
    messages = [
        'First warning',
        'Second warning',
        'Third warning',
    ]

    for w in messages:
        warn(w)

    assert warnings.get_warning_messages() == tuple(messages)
    assert warnings.get_warnings() == [make_summary(WarningSummary, Detail(msg=w)) for w in messages]


def test_dedupe_with_traceback(module_env_mocker: ModuleEnvMocker) -> None:
    module_env_mocker.set_traceback_config([_traceback.TracebackEvent.WARNING])
    msg = "a warning message"

    # WarningMessageDetail dataclass object hash is the dedupe key; presence of differing tracebacks or SourceContexts affects de-dupe

    for _i in range(0, 10):
        warn(msg)  # same location, same traceback- should be collapsed to one message

    assert len(warnings.get_warning_messages()) == 1
    assert len(warnings.get_warnings()) == 1

    for _i in range(0, 10):
        warn(msg)  # with tracebacks on, we should have a different source location than the first loop, but still de-dupe

    assert len(warnings.get_warning_messages()) == 2
    assert len(warnings.get_warnings()) == 2


@pytest.mark.parametrize(
    'test_case',
    (
        1,
        True,
        [1],
        {'k1': 'v1'},
        (1, 2),
        6.62607004,
        b'bytestr',
        None,
    )
)
def test_warn_failure(test_case: t.Any):
    with pytest.raises(TypeError, match=f"must be <class 'str'> instead of {type(test_case)}"):
        warn(test_case)
