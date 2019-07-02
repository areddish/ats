class BarBuilder:
    def __init__(self, desired_timeframe, incoming_timeframe_in_seconds=5):
        self.expected_count = desired_timeframe.seconds / incoming_timeframe_in_seconds
        self.bars = [None] * self.expected_count

    def add(self, bar):
        # find timestamp
        timestemp = bar.timestamp
        # find the index in the list
        index = timestamp.seconds / 5 # HARDCODED
        if bars[index]:
            raise ValueError("Duplicate data")
        bars[index] = bar

    def build(self):
        high = max(map(lambda x: x.high, bars))
        low = min(map(lambda x: x.low, bars)
        open = bars[0].open
        close = bars[-1].close
        volume = sum(map(lambda x: x.volume, bars))
        timestamp = bars[0].timestamp
        # create bar
        return bar
        