import os
import shutil
import tempfile

import pytest
from gcfpy.utils import previous_data


@pytest.fixture
def temp_history_file(monkeypatch):
    tmp_dir = tempfile.mkdtemp()
    path = os.path.join(tmp_dir, "last_files.txt")
    monkeypatch.setattr(previous_data, "HISTORY_FILE", path)
    yield path
    shutil.rmtree(tmp_dir)


def test_save_and_load_previous_file(temp_history_file):
    fake_file = os.path.join(os.path.dirname(temp_history_file), "fake.csv")
    with open(fake_file, "w") as f:
        f.write("test")

    previous_data.save_previous_file(fake_file)
    assert os.path.exists(temp_history_file)

    result = previous_data.load_previous_file()
    assert result == fake_file


def test_duplicate_not_saved_twice(temp_history_file):
    file1 = os.path.join(os.path.dirname(temp_history_file), "file1.csv")
    with open(file1, "w") as f:
        f.write("abc")

    previous_data.save_previous_file(file1)
    previous_data.save_previous_file(file1)

    with open(temp_history_file) as f:
        lines = f.read().splitlines()

    assert lines.count(file1) == 1


def test_max_history_limit(temp_history_file):
    dir_path = os.path.dirname(temp_history_file)
    files = []
    for i in range(previous_data.MAX_HISTORY + 2):
        path = os.path.join(dir_path, f"f{i}.csv")
        with open(path, "w") as f:
            f.write("data")
        previous_data.save_previous_file(path)
        files.append(path)

    with open(temp_history_file) as f:
        lines = f.read().splitlines()

    assert len(lines) == previous_data.MAX_HISTORY
    assert lines == files[-previous_data.MAX_HISTORY :]


def test_load_previous_file_invalid_index(temp_history_file):
    file_path = os.path.join(os.path.dirname(temp_history_file), "f.csv")
    with open(file_path, "w") as f:
        f.write("abc")

    previous_data.save_previous_file(file_path)
    result = previous_data.load_previous_file(index=-99)
    assert result is None


def test_load_previous_file_not_found_on_disk(temp_history_file):
    fake_path = os.path.join(os.path.dirname(temp_history_file), "not_exist.csv")
    with open(temp_history_file, "w") as f:
        f.write(fake_path)

    result = previous_data.load_previous_file()
    assert result is None


def test_load_previous_file_no_history_file(monkeypatch):
    tmp_path = tempfile.mkdtemp()
    monkeypatch.setattr(
        previous_data, "HISTORY_FILE", os.path.join(tmp_path, "nope.txt")
    )
    result = previous_data.load_previous_file()
    assert result is None
