import pytest
import pathlib
import tempfile
import distutils.dir_util
import shutil

from . import tester


@pytest.fixture
def exercise_dir():
    return pathlib.Path(__file__).parent.resolve() / 'submission_example'


@pytest.yield_fixture
def submission_dir(exercise_dir):
    with tempfile.TemporaryDirectory() as submission_dir:
        submission_dir = pathlib.Path(submission_dir)
        distutils.dir_util.copy_tree(str(exercise_dir), str(submission_dir))
        yield submission_dir


def test_run_tests():
    pass


def test_copy(exercise_dir, submission_dir):
    # remove tests from submission dir
    tests_folders = tester.collect_tests_folders(exercise_dir)
    for tests_folder in tests_folders:
        test_path = pathlib.Path(submission_dir) / tests_folder
        shutil.rmtree(test_path, ignore_errors=True)

    # trigger
    tester.copy(exercise_dir, tests_folders, submission_dir)

    # validate
    for tests_folder in tests_folders:
        test_path = pathlib.Path(submission_dir) / tests_folder
        assert test_path.exists()


def test_collect_tests_folders(exercise_dir):
    tests_folders = tester.collect_tests_folders(exercise_dir)

    assert tests_folders == [
        pathlib.Path('ex0/tests'),
    ]
