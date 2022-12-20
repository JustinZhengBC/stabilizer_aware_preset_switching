from krita import *
from PyQt5.QtWidgets import QMessageBox

ERASE_ACTION = "erase_action"

PRESET_CHANGING_ACTIONS = [
    ERASE_ACTION,
    "previous_preset",
    "previous_favorite_preset",
    "next_favorite_preset"
]

class StabilizerAwarePresetSwitcher(Extension):
    enabled: bool
    enabled_once: bool

    def __init__(self, parent):
        self.enabled = False
        self.enabled_once = False
        super().__init__(parent)

    def _is_not_erasing(self):
        return not Krita.instance().action(ERASE_ACTION).isChecked() and not "erase" in Krita.instance().activeWindow().activeView().currentBrushPreset().name().lower()

    def _update_stabilizer(self, *args):
        if not self.enabled:
            return
        if self._is_not_erasing():
            action_name = "set_stabilizer_brush_smoothing"
        else:
            action_name = "set_simple_brush_smoothing"
        Krita.instance().action(action_name).trigger()

    def _initialize(self):
        for action_name in PRESET_CHANGING_ACTIONS:
            Krita.instance().action(action_name).triggered.connect(self._update_stabilizer)

    def _on_click(self):
        if self.enabled:
            self.enabled = False
        else:
            if not self.enabled_once:
                self._initialize()
                self.enabled_once = True
            self.enabled = True
        messageBox = QMessageBox()
        messageBox.setText("Stabilizer Aware Preset Switching")
        messageBox.setInformativeText("Enabled!" if self.enabled else "Disabled!")
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setStandardButtons(QMessageBox.Close)
        messageBox.exec()

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("stabilizer_aware_preset_switching", "Stabilizer-Aware Preset Switching")
        action.triggered.connect(self._on_click)
