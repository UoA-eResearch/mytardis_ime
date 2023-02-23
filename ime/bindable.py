from dataclasses import field
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic, Union
import typing
from PyQt5.QtCore import QLine, QObject, QSignalBlocker, pyqtBoundSignal, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit, QWidget

T = TypeVar('T')

class IBindableInput:
    _value_changed_slot: Optional[Callable]
    value_changed: Optional[pyqtBoundSignal]
    def set_input_value(self, value):
        pass

    def get_input_value(self) -> Any:
        return ""

class QLineEditInput(IBindableInput):
    def __init__(self, widget: QLineEdit):
        self.widget = widget
        self.value_changed = typing.cast(pyqtBoundSignal, widget.editingFinished)

    def set_input_value(self, value:str):
        with QSignalBlocker(self.widget):
            self.widget.setText(value)

    def get_input_value(self):
        return self.widget.text()

class QPlainTextEditInput(IBindableInput):
    def __init__(self, widget: QPlainTextEdit):
        self.widget = widget
        self.value_changed = typing.cast(pyqtBoundSignal, widget.textChanged)
    
    def set_input_value(self, value:str):
        with QSignalBlocker(self.widget):
            self.widget.setPlainText(value)

    def get_input_value(self):
        return self.widget.toPlainText()

# Binder
class BoundObject(QObject, Generic[T]):
    _bound_object: T
    _bound_inputs: Dict[str, List[IBindableInput]]
    bound_object_changed = pyqtSignal(object, object)

    def __init__(self):
        super().__init__()
        self._bound_inputs = {}

    def set_object(self, obj: T):
        old_obj = getattr(self, "_bound_object", None)
        self._bound_object = obj
        self.bound_object_changed.emit(old_obj, obj)
        for field_name in self._bound_inputs:
            for input in self._bound_inputs[field_name]:
                self._set_initial_val_and_connect(field_name, input)

    
    def bind_input(self, field_name: str, input: Union[IBindableInput, QWidget]):
        if isinstance(input, IBindableInput):
            return self._bind_field(field_name, input)
        else:
            return self._bind_field_with_default(field_name, input)
    
    def unbind(self):
        for field_name in self._bound_inputs:
            for input in self._bound_inputs[field_name]:
                if input.value_changed is None or getattr(input, "_value_changed_slot", None) is None:
                    continue
                # Disconnect the slot we've created
                input.value_changed.disconnect(input._value_changed_slot)
                input._value_changed_slot = None

    def _bind_field_with_default(self, field_name: str, input: QWidget):
        if isinstance(input, QLineEdit):
            return self._bind_field(field_name, QLineEditInput(input))
        elif isinstance(input, QPlainTextEdit):
            return self._bind_field(field_name, QPlainTextEditInput(input))
        else:
            raise Exception(f"Unsupported input {input}")
    
    def _set_initial_val_and_connect(self, field_name: str, input: IBindableInput):
        val = getattr(self._bound_object, field_name)
        input.set_input_value(val)
        # Connect to signal for value changes.
        if hasattr(input, 'value_changed') and input.value_changed is not None and not hasattr(input, '_value_changed_slot'):
            # Save the slot lambda we've created, so we can disconnect signal later.
            input._value_changed_slot = lambda: self._handle_input_change(input, field_name, input.get_input_value())
            a = input.value_changed.connect(input._value_changed_slot)

    def _bind_field(self, field_name: str, input: IBindableInput):
        if field_name not in self._bound_inputs:
            self._bound_inputs[field_name] = []
        inputs = self._bound_inputs[field_name]
        inputs.append(input)
        # Initialise the input with current value
        if hasattr(self, "_bound_object"):
            self._set_initial_val_and_connect(field_name, input)

    def __del__(self):
        self.unbind()

    def _handle_input_change(self, source: IBindableInput, field_name: str, newval: str):
        setattr(self._bound_object,field_name, newval)
        for input in self._bound_inputs[field_name]:
            if input is source:
                continue
            input.set_input_value(newval)