from .i2c import I2cDevice


def _parse_rgb_ir_bytes(colour_data):
    measurement = tuple((colour_data[2 * i + 1] << 16) | colour_data[2 * i] for i in range(4))
    total = sum(measurement)
    if total == 0:
        return 0, 0, 0, 0
    measurement = tuple(x / total for x in measurement)
    return measurement[3], measurement[1], measurement[2], measurement[0]


class RgbIrSensor(I2cDevice):
    def self_test(self) -> bool:
        id = self.read(0x06, 1)[0]
        return id == 0xB2

    def configure(self, args: dict) -> None:
        # set light sensor enabled, colour sensing mode.
        self.pack_and_write(0x00, 'B', 0b00000110)
        super().configure(args)

    def measure(self):
        """
        :return: R, G, B and IR Channel readings and a fraction of the total.
        """
        colour_data = self.read_and_unpack(0x0A, '<BHBHBHBH')
        return _parse_rgb_ir_bytes(colour_data)