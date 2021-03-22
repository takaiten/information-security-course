import pyforms
from   pyforms.basewidget   import BaseWidget
from   pyforms.controls     import ControlText, ControlFile, ControlButton


class SimpleExample1(BaseWidget):
    def __init__(self):
        super(SimpleExample1, self).__init__('Simple example 1')

        # Definition of the forms fields
        self._firstname = ControlText('First name', 'Default value')
        self._lastname  = ControlText('Lastname name')
        self._button    = ControlButton('Press this button')
        self._file      = ControlFile('Save file', use_save_dialog=True)


# Execute the application
if __name__ == "__main__":
    pyforms.start_app(SimpleExample1)
