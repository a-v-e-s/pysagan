from .i2c import I2cDevice


class Rtc(I2cDevice):
    def self_test(self) -> bool:
        return True

    def configure(self, args: dict) -> None:
        self.write(0x28, [0x80])
        self.write(0x25, [0x20])

    def measure(self):
        time_regs = self.read_and_unpack(0x00, 'B' * 8)
        hundredths_of_seconds = ((time_regs[0] & 0xF0) >> 4) * 10 + (time_regs[0] & 0x0F)
        seconds = ((time_regs[1] & 0x70) >> 4) * 10 + (time_regs[1] & 0x0F)
        minutes = ((time_regs[2] & 0x70) >> 4) * 10 + (time_regs[2] & 0x0F)
        hours = ((time_regs[3] & 0x30) >> 4) * 10 + (time_regs[3] & 0x0F)
        days = ((time_regs[4] & 0x30) >> 4) * 10 + (time_regs[4] & 0x0F)
        week_day = time_regs[5] & 0x07
        month = ((time_regs[6] & 0x10) >> 4) * 10 + (time_regs[6] & 0x0F)
        year = ((time_regs[7] & 0xF0) >> 4) * 10 + (time_regs[7] & 0x0F)

        return year, month, week_day, days, hours, minutes, seconds, hundredths_of_seconds
