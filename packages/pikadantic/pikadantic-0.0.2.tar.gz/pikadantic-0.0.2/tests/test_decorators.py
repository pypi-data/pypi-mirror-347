from unittest.mock import ANY, Mock

import pytest
from pikadantic.decorators import validate_body
from pikadantic.exceptions import PikadanticValidationError
from pydantic import BaseModel, RootModel


@pytest.fixture
def sample_model() -> type[BaseModel]:
    class SampleModel(BaseModel):
        text: str

    return SampleModel


@pytest.fixture
def sample_root_model() -> type[RootModel]:
    class SampleRootModel(RootModel):
        root: str

    return SampleRootModel


class TestValidateBody:
    def test_when_body_is_valid_then_callback_is_called(self, sample_model: type[BaseModel]):
        callback = Mock()

        decorated = validate_body(sample_model)(callback)
        decorated(ANY, ANY, ANY, b'{"text": "test"}')

        callback.assert_called_once_with(ANY, ANY, ANY, b'{"text": "test"}')

    def test_when_body_is_valid_and_only_model_is_true_then_callback_is_called_with_model(
        self, sample_model: type[BaseModel]
    ):
        callback = Mock()

        decorated = validate_body(sample_model, only_model=True)(callback)
        decorated(ANY, ANY, ANY, b'{"text": "test"}')

        callback.assert_called_once_with(sample_model(text="test"))

    def test_when_body_is_invalid_then_exception_is_raised(self, sample_model: type[BaseModel]):
        callback = Mock()

        decorated = validate_body(sample_model)(callback)

        with pytest.raises(PikadanticValidationError):
            decorated(ANY, ANY, ANY, b'{"text": 1}')

    def test_when_body_is_invalid_and_raise_on_error_is_false_then_callback_is_not_called(
        self,
        sample_model: type[BaseModel],
    ):
        callback = Mock()

        decorated = validate_body(sample_model, raise_on_error=False)(callback)
        decorated(ANY, ANY, ANY, b'{"text": 1}')

        callback.assert_not_called()

    def test_when_body_is_valid_then_callback_is_called_with_root_model(self, sample_root_model: type[RootModel]):
        callback = Mock()

        decorated = validate_body(sample_root_model, json=False)(callback)
        decorated(ANY, ANY, ANY, b"test")

        callback.assert_called_once_with(ANY, ANY, ANY, b"test")

    def test_when_root_model_and_json_is_true_then_exception_is_raised(self, sample_root_model: type[RootModel]):
        callback = Mock()

        decorated = validate_body(sample_root_model, json=True)(callback)

        with pytest.raises(PikadanticValidationError):
            decorated(ANY, ANY, ANY, b'{"root": 1}')

    def test_when_root_model_and_json_is_true_and_raise_on_error_is_false_then_callback_is_not_called(
        self,
        sample_root_model: type[RootModel],
    ):
        callback = Mock()

        decorated = validate_body(sample_root_model, json=True, raise_on_error=False)(callback)
        decorated(ANY, ANY, ANY, b'{"root": 1}')

        callback.assert_not_called()

    def test_when_only_model_is_true_and_json_is_false_then_callback_is_called_with_model(
        self,
        sample_root_model: type[RootModel],
    ):
        callback = Mock()

        decorated = validate_body(sample_root_model, json=False, only_model=True)(callback)
        decorated(ANY, ANY, ANY, b"test")

        callback.assert_called_once_with(sample_root_model(root="test"))

    def test_when_invalid_data_and_json_is_false_then_exception_is_raised(self):
        class SampleRootModel(RootModel):
            root: int

        callback = Mock()
        decorated = validate_body(SampleRootModel, json=False, raise_on_error=True, only_model=True)(callback)

        with pytest.raises(PikadanticValidationError):
            decorated(ANY, ANY, ANY, b"123<<")

    def test_when_invalid_data_and_only_model_is_true_and_raise_on_error_is_false_then_callback_is_not_called(self):
        class SampleRootModel(RootModel):
            root: int

        callback = Mock()
        decorated = validate_body(SampleRootModel, json=False, raise_on_error=False, only_model=True)(callback)

        decorated(ANY, ANY, ANY, b"123<<")
        callback.assert_not_called()
