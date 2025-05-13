from quantybt.strategy import Strategy
from quantybt.stats import Stats
from quantybt.utils import Utils
from quantybt.plots import _PlotBacktest
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import vectorbt as vbt
import pandas as pd
import warnings

class Analyzer:
    def __init__(
        self,
        strategy: Strategy,
        params: Dict[str, Any],
        full_data: pd.DataFrame,
        timeframe: str,
        price_col: str = "close",
        test_size: float = 0,
        init_cash: float = 1000.0,
        fees: float = 0.0002,
        slippage: float = 0.000,
        trade_side: Optional[str] = 'longonly',
        tp_stop: Optional[float] = None,
        sl_stop: Optional[float] = None
    ):
        self.s = Stats(price_col=price_col)
        self.util = Utils()
        self.strategy = strategy
        self.params = params
        self.timeframe = timeframe
        self.test_size = test_size
        self.init_cash = float(init_cash)
        self.fees = fees
        self.slippage = slippage
        self.tp_stop = tp_stop
        self.sl_stop = sl_stop

        self.full_data = self.util.validate_data(full_data)

        if not isinstance(self.full_data.index, pd.DatetimeIndex):
            warnings.warn("Data index is not datetime-based. Time-based features may not work as expected.", stacklevel=2)

        if test_size > 0:
            self.train_df, self.test_df = self.util.time_based_split(self.full_data, test_size)
            self.train_df = self.strategy.preprocess_data(self.train_df.copy(), params)
        else:
            self.train_df = self.strategy.preprocess_data(self.full_data.copy(), params)
            self.test_df = None

        self.signals = self.strategy.generate_signals(self.train_df, **params)
        self._validate_signals()

        portfolio_kwargs = dict(
            close=self.train_df[self.s.price_col],
            entries=self.signals['entries'],
            exits=self.signals['exits'],
            freq=self.timeframe,
            init_cash=self.init_cash,
            fees=self.fees,
            slippage=self.slippage,
            direction=trade_side
        )

        if 'short_entries' in self.signals and self.signals['short_entries'] is not None:
            portfolio_kwargs['short_entries'] = self.signals['short_entries']
        if 'short_exits' in self.signals and self.signals['short_exits'] is not None:
            portfolio_kwargs['short_exits'] = self.signals['short_exits']
        if self.tp_stop is not None:
            portfolio_kwargs['tp_stop'] = self.tp_stop
        if self.sl_stop is not None:
            portfolio_kwargs['sl_stop'] = self.sl_stop

        self.pf = vbt.Portfolio.from_signals(**portfolio_kwargs)

    def _validate_signals(self):
        for k in ['entries', 'exits']:
            if not isinstance(self.signals[k], pd.Series):
                raise ValueError(f"Signal {k} is not a pandas Series.")
            if self.signals[k].dtype != bool:
                self.signals[k] = self.signals[k].astype(bool)

        if not self.signals['entries'].any():
            raise ValueError("No entry signals generated")
        if self.signals['entries'].index.difference(self.train_df.index).any():
            raise ValueError("Signal/data index mismatch")

    def oos_test(self) -> Optional[vbt.Portfolio]:
        if self.test_df is None or self.test_df.empty:
            return None

        test_df = self.strategy.preprocess_data(self.test_df.copy(), self.params)
        test_signals = self.strategy.generate_signals(test_df, **self.params)

        portfolio_kwargs = dict(
            close=test_df[self.s.price_col],
            entries=test_signals['entries'],
            exits=test_signals['exits'],
            freq=self.timeframe,
            init_cash=self.init_cash,
            fees=self.fees,
            slippage=self.slippage,
            direction='longonly'
        )

        if 'short_entries' in test_signals and test_signals['short_entries'] is not None:
            portfolio_kwargs['short_entries'] = test_signals['short_entries']
        if 'short_exits' in test_signals and test_signals['short_exits'] is not None:
            portfolio_kwargs['short_exits'] = test_signals['short_exits']
        if self.tp_stop is not None:
            portfolio_kwargs['tp_stop'] = self.tp_stop
        if self.sl_stop is not None:
            portfolio_kwargs['sl_stop'] = self.sl_stop

        return vbt.Portfolio.from_signals(**portfolio_kwargs)

    def backtest_results(self) -> pd.DataFrame:
        return self.s.backtest_summary(self.pf, self.timeframe)

    def plot_backtest(self, title: str = 'Backtest Results') -> go.Figure:
        plotter = _PlotBacktest(self)
        return plotter.plot_backtest(title=title)

#