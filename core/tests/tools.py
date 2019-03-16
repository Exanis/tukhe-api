import os
import json
from unittest.mock import patch


def snapshot(function, snapshot_name, expect_call=True):
    def wrapper(target):
        def wrapped(*args, **kwargs):
            with patch(function) as patch_function:
                target(patch_function, *args, **kwargs)
                if expect_call:
                    patch_function.assert_called()
                    params = patch_function.call_args
                    local_snapshot(snapshot_name, function, params)
                else:
                    patch_function.assert_not_called()
        return wrapped
    return wrapper


def local_snapshot(snapshot_name, function, content):
    target_file = os.path.join(
        os.path.dirname(__file__),
        "snapshot",
        snapshot_name + "_" + function + ".snap"
    )
    if os.path.isfile(target_file):
        with open(target_file, 'r') as fp:
            expected_params = fp.read()
            json_params = json.dumps(content)
            assert json_params == expected_params
    else:
        print("No snapshot found for " + snapshot_name + ", writing it.")
        with open(target_file, "w") as fp:
            json.dump(content, fp)
