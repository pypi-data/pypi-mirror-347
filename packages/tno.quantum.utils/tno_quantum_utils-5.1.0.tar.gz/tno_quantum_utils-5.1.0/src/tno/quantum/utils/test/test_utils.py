"""This module contains tests for ``tno.quantum.utils._utils``."""

import pytest

from tno.quantum.utils import convert_to_snake_case, get_installed_subclasses
from tno.quantum.utils.validation import check_snake_case


class BaseModel:
    """Dummy base model"""

    def __init__(self, arg1: int, arg2: int) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class ModelA(BaseModel):
    """Model A (supported)"""


class ModelB(BaseModel):
    """Model B (supported)"""


class ModelC:
    """Model C (not supported)"""


def test_get_supported_subclasses() -> None:
    """Test get supported models for dummy models"""

    supported_subclasses = get_installed_subclasses("utils.test.test_utils", BaseModel)

    assert "model_a" in supported_subclasses
    assert "model_b" in supported_subclasses
    assert "model_c" not in supported_subclasses


@pytest.mark.parametrize(
    ("x", "expected_output"),
    [
        ("a", "a"),
        ("A", "a"),
        ("StronglyEntangledModel", "strongly_entangled_model"),
        ("BasicModel", "basic_model"),
        ("QModel", "q_model"),
        ("TESTTwoWords", "test_two_words"),
        ("ModelA", "model_a"),
        ("Model with spaces", "model_with_spaces"),
        ("Model-with mixed--multiple  spaces", "model_with_mixed_multiple_spaces"),
    ],
)
def test_convert_to_snake(x: str, expected_output: str) -> None:
    """Test convert to snake case helper function."""
    converted_x = convert_to_snake_case(x)
    assert converted_x == expected_output
    assert check_snake_case(converted_x, "converted_x")


@pytest.mark.parametrize(
    "x",
    ["1abc", "!abc", "#aa", ".aa", "~bb"],
)
def test_convert_to_snake_raise_error_first_char_invalid(x: str) -> None:
    """Test raise error convert to snake case helper function."""
    error_msg = "Input cannot start with a number or any special symbol"
    with pytest.raises(ValueError, match=error_msg):
        convert_to_snake_case(x)


@pytest.mark.parametrize(
    "x",
    ["abc!", "aa#aa", "default.value", "when~bb"],
)
def test_convert_to_snake_raise_error_special_char_invalid(x: str) -> None:
    """Test raise error convert to snake case helper function."""
    error_msg = "Input cannot contain special characters."
    with pytest.raises(ValueError, match=error_msg):
        convert_to_snake_case(x)


def test_convert_to_snake_path() -> None:
    """Test path flag of convert to snake case."""
    x = "default.value"
    converted_x = convert_to_snake_case(x, path=True)
    assert converted_x == "default.value"
    assert check_snake_case(converted_x, "converted_x", path=True)
