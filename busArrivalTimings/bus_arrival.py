class BusArrival:
    def __init__(self, purpose=None, bus_code=None, bus_no=None):
        self._purpose = purpose
        self._bus_code = bus_code
        self._bus_no = bus_no

    @property
    def purpose(self):
        return self._purpose

    @property
    def bus_code(self):
        return self._bus_code

    @property
    def bus_no(self):
        return self._bus_no
