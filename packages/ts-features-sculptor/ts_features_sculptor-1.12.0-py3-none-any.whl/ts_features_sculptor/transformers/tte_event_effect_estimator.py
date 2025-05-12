import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin

@dataclass
class TteEventEffectEstimator(BaseEstimator, TransformerMixin):
    """
    Оценивает влияние интервального события на TTE (time to event).

    Ограничиваемся случаем, когда событие принято, Помогаем модели
    определится с предсказанием целевой переменной внутри события.

    Выходные признаки:
      - {event_name}_inside_tte_avg
      - {event_name}_outside_tte_avg
      - {event_name}_tte_uplift
    """

    events_df: pd.DataFrame
    event_name: str = "event"
    fallback_uplift: float = np.nan
    shift: int = 1

    starts_: np.ndarray = field(init=False, repr=False)
    ends_:   np.ndarray = field(init=False, repr=False)
    ends_sorted_: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        ev = self.events_df.sort_values("start").reset_index(drop=True)
        self.starts_ = ev["start"].to_numpy()
        self.ends_   = ev["end"].to_numpy()
        self.ends_sorted_ = np.sort(self.ends_)

    def fit(self, X, y=None):
        return self


    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out_df = df.copy()
        times = out_df["time"].to_numpy()
        tte   = out_df["tte"].to_numpy()

        tte_shift = np.roll(tte, self.shift)
        if self.shift:
            tte_shift[: self.shift] = np.nan
        interval_end = out_df["time"] + pd.to_timedelta(tte_shift, unit="D")
        interval_end = interval_end.fillna(out_df["time"]).to_numpy()

        started_cnt = np.searchsorted(self.starts_, times, side="right")
        cur_idx = started_cnt - 1
        cur_idx[cur_idx < 0] = -1

        in_running = (cur_idx >= 0) & (times <= self.ends_[cur_idx])
        full_inside = in_running & (interval_end <= self.ends_[cur_idx])
        inside_shift = full_inside

        valid = ~np.isnan(tte_shift)
        tte_for_sum = np.where(valid, tte_shift, 0.0)

        inside_sum  = np.cumsum(np.where(
            inside_shift & valid, tte_for_sum, 0.0))
        inside_cnt  = np.cumsum(np.where(
            inside_shift & valid, 1, 0))
        outside_sum = np.cumsum(np.where(
            ~inside_shift & valid, tte_for_sum, 0.0))
        outside_cnt = np.cumsum(np.where(
            ~inside_shift & valid, 1, 0))

        inside_avg = (
            inside_sum  / np.where(inside_cnt  > 0, inside_cnt,  np.nan))
        outside_avg = (
            outside_sum / np.where(outside_cnt > 0, outside_cnt, np.nan))

        uplift = inside_avg / outside_avg
        no_data = (inside_cnt == 0) | (outside_cnt == 0) | (outside_avg == 0)
        uplift[no_data] = self.fallback_uplift

        p = self.event_name
        out_df[f"{p}_inside_tte_avg"]  = inside_avg
        out_df[f"{p}_outside_tte_avg"] = outside_avg
        out_df[f"{p}_tte_uplift"]      = uplift

        return out_df
