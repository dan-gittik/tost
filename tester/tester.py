import pathlib
import typing
import shutil
import os
import contextlib


@contextlib.contextmanager
def in_directory(path):
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


def run_tests(exercise_dir: pathlib.Path, submission_dir: pathlib.Path, exercises: typing.List[int] = []):
    print(f'running tests on: {submission_dir} for exercises: {exercises}')

    # download repo
    print(f'downloading repo: {submission_dir}')
    # credentials

    # replace tests
    print(f'collecting tests from {exercise_dir}')
    tests = collect_tests_folders(exercise_dir)
    print(f'tests collected: {",".join(tests)}')

    print(f'replacing tests folder')
    copy(tests, submission_dir)

    # run container
    print(f'running tester container')
    # attach repo volume
    # entrypoint: pytest ...

    # read output

    # parse output
    # parse output per exercise


def copy(exercise_dir: pathlib.Path, tests_folders: typing.List[pathlib.Path], submission_dir: pathlib.Path):
    print(f'copying tests to {submission_dir}')
    with in_directory(submission_dir):
        print('replacing tests')
        for test_folder in tests_folders:
            print(f'replacing {test_folder}')
            source = exercise_dir / test_folder
            target = submission_dir / test_folder
            print(f'copying {source} to {target}')
            shutil.rmtree(target, ignore_errors=True)
            shutil.copytree(source, target)


def collect_tests_folders(directory: pathlib.Path) -> typing.List[pathlib.Path]:
    tests = []
    with in_directory(directory):
        for prefix, directories, files in os.walk('.', topdown=True):
            directories[:] = [
                directory for directory in directories if not directory.startswith('.')
            ]
            for directory in directories:
                if directory == 'tests':
                    test = os.path.join(prefix, directory)
                    print(f'found tests folder: {test}')
                    tests.append(pathlib.Path(test))
    return tests
