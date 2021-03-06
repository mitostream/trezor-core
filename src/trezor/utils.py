import sys
import gc

from trezorutils import halt, memcpy, set_mode_unprivileged, symbol  # noqa: F401


def unimport(genfunc):
    async def inner(*args, **kwargs):
        mods = set(sys.modules)
        try:
            ret = await genfunc(*args, **kwargs)
        finally:
            for mod in sys.modules:
                if mod not in mods:
                    del sys.modules[mod]
            gc.collect()
        return ret
    return inner


def ensure(cond):
    if not cond:
        raise AssertionError()


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def split_words(sentence, width, metric=len):
    line = []
    for w in sentence.split(' '):
        # empty word  -> skip
        if not w:
            continue
        # new word will not fit -> break the line
        if metric(' '.join(line + [w])) >= width:
            yield ' '.join(line)
            line = []
        # word is too wide -> split the word
        while metric(w) >= width:
            for i in range(1, len(w) + 1):
                if metric(w[:-i]) < width:
                    yield w[:-i] + '-'
                    w = w[-i:]
                    break
        line.append(w)
    yield ' '.join(line)


def format_amount(amount, decimals):
    d = pow(10, decimals)
    amount = ('%d.%0*d' % (amount // d, decimals, amount % d)).rstrip('0')
    if amount.endswith('.'):
        amount = amount[:-1]
    return amount


def format_ordinal(number):
    return str(number) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= number % 100 < 20 else number % 10, 'th')


class HashWriter:

    def __init__(self, hashfunc):
        self.ctx = hashfunc()
        self.buf = bytearray(1)  # used in append()

    def extend(self, buf: bytearray):
        self.ctx.update(buf)

    def append(self, b: int):
        self.buf[0] = b
        self.ctx.update(self.buf)

    def get_digest(self, *args) -> bytes:
        return self.ctx.digest(*args)
