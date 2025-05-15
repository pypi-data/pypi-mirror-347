from typing import List, Optional
from dataclasses import dataclass
from mdas_python_sdk.helpers.logger import logger

@dataclass
class Quote:
    symbol: Optional[str] = None
    issue_market: Optional[str] = None
    yest_close_px: Optional[float] = None
    volume: Optional[int] = None
    open_px: Optional[float] = None
    high_px: Optional[float] = None
    low_px: Optional[float] = None
    closing_px: Optional[float] = None
    ask_px: Optional[float] = None
    ask_sz: Optional[int] = None
    bid_px: Optional[float] = None
    bid_sz: Optional[int] = None
    last_px: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    column: Optional[int] = None
    trade_region: Optional[str] = None
    trade_region_name: Optional[str] = None
    trade_px: Optional[float] = None
    trade_sz: Optional[int] = None
    condition: Optional[str] = None
    activity_timestamp: Optional[str] = None
    data_source: Optional[str] = None
    chart_date: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Quote':
        """Create a Quote object from a dictionary"""
        return cls(
            symbol=data.get("symbol") if data.get("symbol") is not None else None,
            issue_market=data.get("issue_market") if data.get("issue_market") is not None else None,
            yest_close_px=float(data.get("yest_close_px")) if data.get("yest_close_px") is not None else None,
            volume=int(data.get("volume")) if data.get("volume") is not None else None,
            open_px=float(data.get("open_px")) if data.get("open_px") is not None else None,
            high_px=float(data.get("high_px")) if data.get("high_px") is not None else None,
            low_px=float(data.get("low_px")) if data.get("low_px") is not None else None,
            closing_px=float(data.get("closing_px")) if data.get("closing_px") is not None else None,
            ask_px=float(data.get("ask_px")) if data.get("ask_px") is not None else None,
            ask_sz=int(data.get("ask_sz")) if data.get("ask_sz") is not None else None,
            bid_px=float(data.get("bid_px")) if data.get("bid_px") is not None else None,
            bid_sz=int(data.get("bid_sz")) if data.get("bid_sz") is not None else None,
            last_px=float(data.get("last_px")) if data.get("last_px") is not None else None,
            change=float(data.get("change")) if data.get("change") is not None else None,
            change_percent=float(data.get("change_percent")) if data.get("change_percent") is not None else None,
            column=int(data.get("column")) if data.get("column") is not None else None,
            trade_region=data.get("trade_region"),
            trade_region_name=data.get("trade_region_name"),
            trade_px=float(data.get("trade_px")) if data.get("trade_px") is not None else None,
            trade_sz=int(data.get("trade_sz")) if data.get("trade_sz") is not None else None,
            condition=data.get("condition"),
            activity_timestamp=data.get("activity_timestamp"),
            data_source=data.get("data_source"),
            chart_date=data.get("chart_date"),
            open=float(data.get("open")) if data.get("open") is not None else None,
            high=float(data.get("high")) if data.get("high") is not None else None,
            low=float(data.get("low")) if data.get("low") is not None else None,
            close=float(data.get("close")) if data.get("close") is not None else None

        )


@dataclass
class QuoteResponse:
    data: List[Quote]
    
    @classmethod
    def from_dict(cls, data: any) -> 'QuoteResponse':
        """Create a QuoteResponse object from a dictionary"""

        # if data is a list, return a list of Quote objects
        if isinstance(data, list):
            quotes = [Quote.from_dict(quote_data) for quote_data in data.get('data')]
            return cls(data=quotes)
        elif isinstance(data, dict):
            quote = Quote.from_dict(data)
            return cls(data=[quote])
        else:
            return cls(data=[]) 