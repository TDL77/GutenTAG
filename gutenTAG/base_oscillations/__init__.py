from enum import Enum
from typing import Optional, Any, List
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import neurokit2 as nk
from ..anomalies import Anomaly
from .comut import CorrelatedMultivarGenerator

from .cylinder_bell_funnel import generate_pattern_data


def get_or_error(name: str, value: Optional[Any]) -> Any:
    if value is None:
        raise ValueError(f"Parameter {name} for the base-oscillation must be set!")
    return value


class BaseOscillation(Enum):
    Sinus = "sinus"
    RandomWalk = "random_walk"
    CylinderBellFunnel = "cylinder_bell_funnel"
    ECG = "ecg"
    CoMuT = "comut"

    def __init__(self, *args, **kwargs):
        super().__init__(args, **kwargs)
        self.anomalies: Optional[List[Anomaly]] = None

    def inject_anomaly(self, anomalies: List[Anomaly]):
        self.anomalies = anomalies

    def generate(self, length: int, frequency: float = 10., amplitude: float = 1., channels: int = 1,
                 variance: float = 1, avg_pattern_length: int = 10, variance_pattern_length: int = 10, heart_rate: int = 60) -> np.ndarray:
        if self == BaseOscillation.Sinus:
            end = 2 * np.pi * frequency
            base_ts = np.arange(0, end, end / length).reshape(length, 1)
            base_ts = np.repeat(base_ts, repeats=channels, axis=1)
            return np.sin(base_ts) * amplitude
        elif self == BaseOscillation.RandomWalk:
            origin = np.zeros((1, channels))
            steps = np.random.choice([-1., 0., 1.], size=(length, channels))
            ts = np.concatenate([origin, steps]).cumsum(0)
            return MinMaxScaler(feature_range=[-amplitude, amplitude]).fit_transform(ts / np.abs(ts).max())
        elif self == BaseOscillation.CylinderBellFunnel:
            ts = []
            for channel in range(channels):
                ts.append(generate_pattern_data(length, avg_pattern_length, amplitude,
                default_variance=variance, variance_pattern_length=variance_pattern_length))
            return np.column_stack(ts)
        elif self == BaseOscillation.ECG:
            ts = []
            for channel in range(channels):
                ecg = nk.ecg_simulate(duration=int(frequency),
                                      sampling_rate=length // int(frequency),
                                      heart_rate=heart_rate)
                ts.append(ecg)
            return np.column_stack(ts)
        elif self == BaseOscillation.CoMuT:
            #CorrelatedMultivarGenerator(
             #   length=length,
             #   dimensions=channels,
             #   step_length=int(frequency),
             #   value_diff=int(amplitude),
             #   value_offset=,
             #   dimensions_involved=,
             #   std=
            #)
            pass
        else:
            raise ValueError(f"The Base Oscillation '{self.name}' is not yet supported! Guten Tag!")
