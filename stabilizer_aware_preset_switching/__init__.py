from .stabilizer_aware_preset_switching import StabilizerAwarePresetSwitcher

Krita.instance().addExtension(StabilizerAwarePresetSwitcher(Krita.instance()))
