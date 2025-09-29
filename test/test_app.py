
import pytest
import datetime
from app import from_file_to_list, minor, category, cost_sort, data_sort, zapis, deleted, upd


def test_from_file_to_list(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Milk 50 Food\nBread 30 Food\n", encoding="utf-8")
    result = from_file_to_list(str(file_path))
    assert result == [["Milk", "50", "Food"], ["Bread", "30", "Food"]]


def test_minor_capitalization():
    massive = [["milk", "50", "food"], ["bread", "30", "food"]]
    result = minor(massive)
    assert result == [["Milk", "50", "Food"], ["Bread", "30", "Food"]]


def test_category_grouping():
    massive = [["Milk", "50", "Food"], ["Chair", "100", "Furniture"], ["Bread", "30", "Food"]]
    result = category(massive)
    assert result == {"Food": ["Milk", "Bread"], "Furniture": ["Chair"]}


def test_cost_sort_min(monkeypatch):
    massive = [["Milk", "50", "Food"], ["Bread", "30", "Food"], ["Chair", "100", "Furniture"]]
    monkeypatch.setattr("builtins.input", lambda _: "min")
    result = cost_sort(massive)
    assert [item[0] for item in result] == ["Bread", "Milk", "Chair"]


def test_cost_sort_invalid(monkeypatch):
    massive = [["Milk", "50", "Food"]]
    monkeypatch.setattr("builtins.input", lambda _: "wrong")
    result = cost_sort(massive)
    assert result == []
    


def test_data_sort_grouping():
    today = f"{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}"
    massive = [["Milk", "50", "Food", today], ["Bread", "30", "Food", today]]
    result = data_sort(massive)
    assert today in result
    assert "Milk" in result[today]
    assert "Bread" in result[today]


def test_zapis_add_valid(monkeypatch):
    massive = []
    today = f"{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}"
    monkeypatch.setattr("builtins.input", lambda _: "Milk 50 Food")
    result = zapis(massive)
    assert result[0][:3] == ["Milk", "50", "Food"]
    assert result[0][-1] == today


def test_zapis_invalid_price(monkeypatch):
    massive = []
    monkeypatch.setattr("builtins.input", lambda _: "Milk abc Food")
    result = zapis(massive)
    assert result == []


def test_deleted_remove(monkeypatch):
    massive = [["Milk", "50", "Food"]]
    monkeypatch.setattr("builtins.input", lambda _: "1")
    result = deleted(massive)
    assert result == []


def test_upd_write_and_read(tmp_path):
    file_path = tmp_path / "test.txt"
    massive = [["Milk", "50", "Food"], ["Bread", "30", "Food"]]
    upd(massive, str(file_path))
    read_back = from_file_to_list(str(file_path))
    assert read_back == massive




