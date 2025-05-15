from typing import Dict, List, Any, Union, Optional
from ..core.http_client import HttpClient


class QuoteService:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
    
    def get_level1_quote(self, symbols: Union[str, List[str]], 
                         response_camel_case: bool = False,
                         user_name: Optional[str] = None,
                         platform: Optional[str] = None) -> Dict[str, Any]:
        """
        Get level 1 quote data for the specified symbols.
        """
        if isinstance(symbols, list):
            symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        # Add optional parameters if provided
        if user_name:
            params["user_name"] = user_name
            
        if platform:
            params["platform"] = platform
        
        return self.http_client.get("/api/quote/level1", params=params) 
    
    def get_best_quote(self, symbols: Union[str, List[str]], response_camel_case: bool = False,
                      user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get best quote data for the specified symbols."""

        if isinstance(symbols, list): 
            symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: 
            params["user_name"] = user_name
        if platform: 
            params["platform"] = platform
        return self.http_client.get("/api/quote/best-quote", params=params)
    
    def get_nbbo_snapshot(self, symbols: Union[str, List[str]], response_camel_case: bool = False,
                         user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get NBBO Snapshot data for the specified symbols."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/nbbo-snapshot", params=params)
    
    def get_region_quotes(self, symbol: str, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get region quotes for a symbol."""
        params = {"symbol": symbol, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/region-quotes", params=params)

    def get_time_sale(self, symbol: str, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get time and sale data for a symbol."""
        params = {"symbol": symbol, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/time-sale", params=params)

    def get_last_trade(self, symbols: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get last trade data for symbols."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/last-trade", params=params)

    def get_intraday_chart(self, symbol: str, day_minute: str = "D", response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get intraday chart data for a symbol."""
        params = {"symbol": symbol, "day_minute": day_minute, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/intraday-chart", params=params)

    def get_historical_day_chart(self, symbol: str, year: Optional[str] = None, month: int = 0, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get historical day chart for a symbol."""
        params = {"symbol": symbol, "response_camel_case": str(response_camel_case).lower()}
        if year: params["year"] = year
        params["month"] = month
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/historical-day-chart", params=params)

    def get_historical_minute_chart(self, symbol: str, date: str, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get historical minute chart for a symbol and date."""
        params = {"symbol": symbol, "date": date, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/historical-minute-chart", params=params)

    def get_top_20(self, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get top 20 data."""
        params = {"response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/top-20", params=params)

    def get_option_chain_dates(self, symbol: str, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option chain dates for a symbol."""
        params = {"symbol": symbol, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/option-chain-dates", params=params)

    def get_option_chain(self, underlying: str, date: str, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option chain for an underlying and date."""
        params = {"underlying": underlying, "date": date, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/option-chain", params=params)

    def get_option_level1(self, option_names: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option level 1 data for option names."""
        if isinstance(option_names, list): option_names = ",".join(option_names)
        params = {"option_names": option_names, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/option-level1", params=params)

    def get_option_level1_with_greek(self, option_names: Union[str, List[str]], include_greek: bool = False, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option level 1 data with Greek values."""
        if isinstance(option_names, list): option_names = ",".join(option_names)
        params = {"option_names": option_names, "include_greek": str(include_greek).lower(), "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/option-level1-with-greek", params=params)

    def get_option_day_chart(self, symbol: str, year: Optional[str] = None, month: int = 0, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option day chart for a symbol."""
        params = {"symbol": symbol, "response_camel_case": str(response_camel_case).lower()}
        if year: params["year"] = year
        params["month"] = month
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/option-day-chart", params=params)

    def get_equiduct_level1(self, symbols: Union[str, List[str]], realtime: bool = False, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get Equiduct Level 1 data for symbols."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {
            "symbols": symbols,
            "realtime": str(realtime).lower(),
            "response_camel_case": str(response_camel_case).lower()
        }
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/equiduct-level1", params=params)

    def get_bonds(self, isins: Union[str, List[str]], bondPriceType: str = "Percentage", bondQuantityType: str = "Par", response_camel_case: bool = False, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get bonds data for ISINs."""
        if isinstance(isins, list): isins = ",".join(isins)
        params = {
            "isins": isins,
            "bondPriceType": bondPriceType,
            "bondQuantityType": bondQuantityType,
            "response_camel_case": str(response_camel_case).lower()
        }
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/bonds", params=params)

    def search_bonds(self, criteria: str, limit: int = 20, loadQuotes: bool = False, bondPriceType: str = "Percentage", bondQuantityType: str = "Par", response_camel_case: bool = False, platform: Optional[str] = None) -> Dict[str, Any]:
        """Search bonds based on criteria."""
        params = {
            "criteria": criteria,
            "limit": limit,
            "loadQuotes": str(loadQuotes).lower(),
            "bondPriceType": bondPriceType,
            "bondQuantityType": bondQuantityType,
            "response_camel_case": str(response_camel_case).lower()
        }
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/bonds-search", params=params)

    def get_bond_screener_field_values(self) -> Dict[str, Any]:
        """Get bond screener field possible values."""
        return self.http_client.get("/api/quote/bond-screener-field-values")

    def get_bonds_chart(self, isin: str, frequency: str, start: str, end: str, response_camel_case: bool = False, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get bonds historical chart data."""
        params = {
            "isin": isin,
            "frequency": frequency,
            "start": start,
            "end": end,
            "response_camel_case": str(response_camel_case).lower()
        }
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/bonds-chart", params=params)

    def get_mutual_funds(self, symbols: Union[str, List[str]], response_camel_case: bool = False, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get mutual funds data for symbols."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/mutual-funds", params=params)

    def get_quodd_eod(self, symbols: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get QUODD EOD data for symbols."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/quodd-eod", params=params)

    def get_quodd_delay(self, symbols: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get QUODD delay data for symbols."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/quodd-delay", params=params)

    def get_ice_isin(self, isins: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get ICE ISIN data."""
        if isinstance(isins, list): isins = ",".join(isins)
        params = {"isins": isins, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/ice-isin", params=params)

    def get_ice_eod(self, symbols: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get ICE EOD data."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/ice-eod", params=params)

    def get_fx_rate(self, symbols: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get Forex rate data."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/fx-rate", params=params)

    def get_fx_table(self, symbols: Union[str, List[str]], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get Forex table data."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/fx-table", params=params)

    def get_company_profile(self, symbol: str, response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get company profile data."""
        params = {"symbol": symbol, "response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quote/company-profile", params=params)

    def get_equity(self, symbols: Union[str, List[str]], platform: Optional[str] = None) -> Dict[str, Any]:
        """Get full Level 1 equity data for symbols."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols}
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/equity", params=params)

    def get_equity_intraday(self, symbol: str, from_time: Optional[str] = None, to_time: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get intraday and historical minute chart for equity."""
        params = {"symbol": symbol}
        if from_time: params["from"] = from_time
        if to_time: params["to"] = to_time
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/equity/intraday", params=params)

    def get_option_historical(self, symbol: str, start: Optional[str] = None, end: Optional[str] = None, range: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option historical day chart."""
        params = {"symbol": symbol}
        if start: params["start"] = start
        if end: params["end"] = end
        if range: params["range"] = range
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/option/historical", params=params)

    def search_quotes(self, criteria: str, limit: int = 20, loadQuotes: bool = False, platform: Optional[str] = None) -> Dict[str, Any]:
        """Search for quotes based on criteria."""
        params = {
            "criteria": criteria,
            "limit": limit,
            "loadQuotes": str(loadQuotes).lower()
        }
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/search", params=params)

    def get_option(self, symbols: Union[str, List[str]], greeks: bool = False, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option level 1 data."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols, "greeks": str(greeks).lower()}
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/option", params=params)

    def get_option_chain_dates(self, symbol: str, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option chain dates for a symbol."""
        params = {"symbol": symbol}
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/option/chain/dates/{symbol}", params=params)

    def get_option_chain(self, symbol: str, date: str, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get option chain data for a symbol and date."""
        params = {"symbol": symbol, "date": date}
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/option/chain/{symbol}/{date}", params=params)

    def get_equity_historical(self, symbol: str, start: Optional[str] = None, end: Optional[str] = None, range: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get historical day chart for equity."""
        params = {"symbol": symbol}
        if start: params["start"] = start
        if end: params["end"] = end
        if range: params["range"] = range
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/equity/historical", params=params)

    def get_bonds(self, identifiers: Union[str, List[str]], bondPriceType: str = "Percentage", bondQuantityType: str = "Par", platform: Optional[str] = None) -> Dict[str, Any]:
        """Get bonds data for identifiers."""
        if isinstance(identifiers, list): identifiers = ",".join(identifiers)
        params = {
            "identifiers": identifiers,
            "bondPriceType": bondPriceType,
            "bondQuantityType": bondQuantityType
        }
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/bonds", params=params)

    def search_bonds(self, criteria: str, limit: int = 20, loadQuotes: bool = False, bondPriceType: str = "Percentage", bondQuantityType: str = "Par", platform: Optional[str] = None) -> Dict[str, Any]:
        """Search bonds based on criteria."""
        params = {
            "criteria": criteria,
            "limit": limit,
            "loadQuotes": str(loadQuotes).lower(),
            "bondPriceType": bondPriceType,
            "bondQuantityType": bondQuantityType
        }
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/bonds/search", params=params)

    def get_fx(self, symbols: Union[str, List[str]], platform: Optional[str] = None) -> Dict[str, Any]:
        """Get Forex rate data."""
        if isinstance(symbols, list): symbols = ",".join(symbols)
        params = {"symbols": symbols}
        if platform: params["platform"] = platform
        return self.http_client.get("/api/quotes/fx", params=params)

    def symbol_search(self, body: Dict[str, Any], response_camel_case: bool = False, user_name: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        """Symbol screener search."""
        params = {"response_camel_case": str(response_camel_case).lower()}
        if user_name: params["user_name"] = user_name
        if platform: params["platform"] = platform
        return self.http_client.post("/api/quote/symbol-search", params=params, data=body)

    def bond_screener(self, body: Dict[str, Any], response_camel_case: bool = False, platform: Optional[str] = None) -> Dict[str, Any]:
        """Bond screener search."""
        params = {"response_camel_case": str(response_camel_case).lower()}
        if platform: params["platform"] = platform
        return self.http_client.post("/api/quote/bonds-screener", params=params, data=body)
    
    

    
    
    

    