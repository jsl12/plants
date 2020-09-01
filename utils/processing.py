import pandas as pd


def get_codes(scan_data: pd.Series, code_length: int = None):
    # extracts the coded signal as a hex string
    return [
        convert_code(group)
        for threshold, group in signal_groups(scan_data)
        if code_length is None or group.shape[0] == code_length
    ]


def signal_groups(scan_data: pd.Series):
    # groups the signals by which ones occur between the long pauses
    pulses = process_pulses(scan_data, 1)
    return pulses.groupby(pd.cut(pulses.index, long_pauses(scan_data).index.values))


def process_pulses(scan_data: pd.Series, val: int = 1) -> pd.Series:
    # TimedeltaIndex, int value post-change
    value_changes = scan_data.loc[scan_data.shift() != scan_data]

    # TimedeltaIndex, timedelta64[ns] length of pulse
    pulses = value_changes.index.to_series().diff().shift(-1).loc[value_changes == val]

    # convert values to floats
    pulses = pulses.apply(lambda v:v.total_seconds())

    return pulses


def long_pauses(scan_data: pd.Series, threshold: float = .004) -> pd.Series:
    # Finds the long pauses between signals
    offs = process_pulses(scan_data, 0)
    return offs[offs >= threshold]


def convert_code(signal_group: pd.Series):
    # converts a group of pulses into a hex string
    bin = convert_to_binary(signal_group)
    res = int(''.join(map(str, bin.values)), 2)
    return f'{res:x}'


def convert_to_binary(pulses: pd.Series, threshold: float = .0003) -> pd.Series:
    # converts the pulses to binary values based on being above/below the threshold length
    res = pulses.copy()
    ones = res[res < threshold].index
    zeroes = res[res > threshold].index
    res.loc[ones] = 1
    res.loc[zeroes] = 0
    return res.dropna().apply(int)

def pulse_lengths(scan_data: pd.Series):
    pulses = process_pulses(scan_data, 1)
    pauses = process_pulses(scan_data, 0)

    period = signal_groups(scan_data).apply(lambda df: df.index.to_series().diff().mean()).mean().total_seconds()
    digits = len(str(period)) - 2

    short = round(pulses[(pulses <= .0003)&(pulses >= .0001)].mean(), digits)
    long = round(pulses[(pulses >= .0003)&(pulses <= .001)].mean(), digits)
    pause = round(pauses[pauses >= .001].mean(), digits)

    return period, short, long, pause
