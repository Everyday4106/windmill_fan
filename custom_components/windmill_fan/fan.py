from homeassistant.components.fan import FanEntity

class WindmillFan(FanEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator):
        self._is_on = False
        
