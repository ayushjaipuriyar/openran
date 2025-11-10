import random


def mmap(x=None, p=None):
    if x is None:
        x = random.uniform(0, 1)
    if p is None:
        p = random.uniform(0.25, 0.5)
    xn = x
    if x >= 0 and x <= 0.5:
        xn = (x / p) * (2 - (x / p))
    if x > 0.5 and x <= 1:
        xn = ((1 - x) / p) * (2 - ((1 - x) / p))
    pn = 0.25 + ((p + x) % 0.25)
    return xn, pn


class MMapGenerator:
    def __init__(self, seed=None, p=None):
        self.x = seed if seed is not None else random.uniform(0, 1)
        self.p = p if p is not None else random.uniform(0.25, 0.5)
        self._initial_seed = self.x

    @property
    def seed(self):
        return self._initial_seed

    def next(self):
        self.x, self.p = mmap(self.x, self.p)
        return self.x


def generate_channel_parameters(generator):
    """Generate random channel parameters for RAN experiments"""
    params = {
        "snr_db": round(generator.next() * 20 + 10, 2),  # 10 to 30 dB
        "delay_ms": round(generator.next() * 10, 2),  # 0 to 10 ms
        "path_loss_db": round(generator.next() * 30 + 50, 2),  # 50 to 80 dB
        "doppler_hz": round(generator.next() * 100, 2),  # 0 to 100 Hz
    }
    return params
