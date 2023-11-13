from dataclasses import field
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic, Union
import typing
from PyQt6.QtCore import QLine, QObject, QSignalBlocker, pyqtBoundSignal, pyqtSignal
from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit, QWidget

T = TypeVar('T')

class IBindableInput:
    """
    Interface for a bindable input. Subclasses must implement `set_input_value` and `get_input_value`.
    """
    _value_changed_slot: Optional[Callable]
    value_changed: Optional[pyqtBoundSignal]
    def set_input_value(self, value: str) -> None:
        """Abstract function for setting the input value.

        Args:
            value (str): The value that should be set on this input.
        """
        pass

    def get_input_value(self) -> str:
        """Abstract function for getting the input value.

        Returns:
            str: The value on this input.
        """
        return ""

class QLineEditInput(IBindableInput):
    """
    A bindable input for QLineEdit widgets.
    """
    def __init__(self, widget: QLineEdit) -> None:
        self.widget = widget
        self.value_changed = typing.cast(pyqtBoundSignal, widget.editingFinished)

    def set_input_value(self, value:str) -> None:
        """Concrete function that sets the value of the line edit widget.

        Args:
            value (str): The value for this widget.
        """
        with QSignalBlocker(self.widget):
            self.widget.setText(value)

    def get_input_value(self) -> str:
        """Concrete function that gets the line edit widget value.

        Returns:
            str: The value of the widget.
        """
        return self.widget.text()

class QPlainTextEditInput(IBindableInput):
    """
    A bindable input for QPlainTextEdit widgets.
    """
    def __init__(self, widget: QPlainTextEdit):
        self.widget = widget
        self.value_changed = typing.cast(pyqtBoundSignal, widget.textChanged)
    
    def set_input_value(self, value:str) -> None:
        """Concrete function that sets the value of the plain text edit widget.

        Args:
            value (str): The value for this widget.
        """
        with QSignalBlocker(self.widget):
            self.widget.setPlainText(value)

    def get_input_value(self) -> str:
        """Concrete function that gets the value of the plain text edit widget.

        Returns:
            str: The value for this widget.
        """
        return self.widget.toPlainText()

# Binder
class BoundObject(QObject, Generic[T]):
    """
    Binds a QObject to a Python object. Allows binding of input widgets to object attributes.
    """
    _bound_object: T
    _bound_inputs: Dict[str, List[IBindableInput]]
    bound_object_changed = pyqtSignal(object, object)

    def __init__(self) -> None:
        super().__init__()
        self._bound_inputs = {}

    def set_object(self, obj: T) -> None:
        """
        Binds the given object to this BoundObject. Triggers `bound_object_changed` signal.

        Args:
            obj (T): The object to bind to this BoundObject.
        """
        old_obj = getattr(self, "_bound_object", None)
        self._bound_object = obj
        self.bound_object_changed.emit(old_obj, obj)
        for field_name in self._bound_inputs:
            for input in self._bound_inputs[field_name]:
                self._set_initial_val_and_connect(field_name, input)

    
    def bind_input(self, field_name: str, input: Union[IBindableInput, QWidget]) -> None:
        """
        Binds the given input to the given field of the bound object.

        Args:
            field_name: The name of the field to bind the input to.
            input: The input to bind.
        
        Returns:
            Nothing.
        """
        if isinstance(input, IBindableInput):
            return self._bind_field(field_name, input)
        else:
            return self._bind_field_with_default(field_name, input)
    
    def unbind(self) -> None:
        """
        Unbinds all input widgets from their bound object attributes.

        Args:
            None.
        
        Returns:
            Nothing.
        """
        for field_name in self._bound_inputs:
            for input in self._bound_inputs[field_name]:
                if input.value_changed is None or getattr(input, "_value_changed_slot", None) is None:
                    continue
                # Disconnect the slot we've created
                assert input._value_changed_slot is not None
                input.value_changed.disconnect(input._value_changed_slot)
                input._value_changed_slot = None

    def _bind_field_with_default(self, field_name: str, input: QWidget) -> None:
        """
        Binds a field with a default input widget.

        Args:
            field_name: Name of the field to be bound.
            input: Input widget to bind the field with.

        Raises:
            ValueError: If the input widget type is unsupported.
        """
        if isinstance(input, QLineEdit):
            return self._bind_field(field_name, QLineEditInput(input))
        elif isinstance(input, QPlainTextEdit):
            return self._bind_field(field_name, QPlainTextEditInput(input))
        else:
            raise ValueError(f"Unsupported input {input}")
    
    def _set_initial_val_and_connect(self, field_name: str, input: IBindableInput) -> None:
        """
        Sets the initial value for the input widget and connects it to its value_changed signal.

        Args:
            field_name: Name of the field being bound.
            input: The input widget being bound.

        """
        val = getattr(self._bound_object, field_name)
        input.set_input_value(val)
        # Connect to signal for value changes.
        if hasattr(input, 'value_changed') and input.value_changed is not None and not hasattr(input, '_value_changed_slot'):
            # Save the slot lambda we've created, so we can disconnect signal later.
            input._value_changed_slot = lambda: self._handle_input_change(input, field_name, input.get_input_value())
            a = input.value_changed.connect(input._value_changed_slot)

    def _bind_field(self, field_name: str, input: IBindableInput) -> None:
        """
        Binds a field to an input widget.

        Args:
            field_name: Name of the field to be bound.
            input: Input widget to bind the field with.

        """
        if field_name not in self._bound_inputs:
            self._bound_inputs[field_name] = []
        inputs = self._bound_inputs[field_name]
        inputs.append(input)
        # Initialise the input with current value
        if hasattr(self, "_bound_object"):
            self._set_initial_val_and_connect(field_name, input)

    def __del__(self) -> None:
        """Destructor method to unbind all inputs."""
        self.unbind()

    def _handle_input_change(self, source: IBindableInput, field_name: str, newval: str) -> None:
        """
        Handle changes to an input field and propagate the change to other bound input fields.

        :param source: The input object that triggered the change.
        :param field_name: The name of the Python object field to update.
        :param newval: The new value of the input field.
        """
        setattr(self._bound_object,field_name, newval)
        for input in self._bound_inputs[field_name]:
            if input is source:
                continue
            input.set_input_value(newval)
