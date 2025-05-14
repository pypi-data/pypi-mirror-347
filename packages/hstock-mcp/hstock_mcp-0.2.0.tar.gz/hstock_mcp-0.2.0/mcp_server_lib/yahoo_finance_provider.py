#/home/ubuntu/mcp_server/yahoo_finance_provider.py
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient
from datetime import datetime, timedelta, timezone

client = ApiClient()

def datetime_to_epoch_seconds(dt_str, is_end_date=False):
    """Converts YYYY-MM-DD string to Unix epoch seconds."""
    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d")
    if is_end_date:
        # For period2, Yahoo Finance expects the start of the *next* day 
        # to include the end_date itself.
        dt_obj = dt_obj + timedelta(days=1)
    return int(dt_obj.replace(tzinfo=timezone.utc).timestamp())

def epoch_seconds_to_datetime_str(epoch_seconds):
    """Converts Unix epoch seconds to YYYY-MM-DD string."""
    if epoch_seconds is None:
        return None
    return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc).strftime("%Y-%m-%d")

def fetch_historical_stock_data(symbol: str, frequency: str, start_date_str: str = None, end_date_str: str = None):
    """
    Fetches historical stock data from YahooFinance API based on the design in 
    api_design_historical_data.md.
    """
    query_params = {
        "symbol": symbol,
        "includeAdjustedClose": True
    }

    # Map frequency to interval
    if frequency == "daily":
        query_params["interval"] = "1d"
    elif frequency == "weekly":
        query_params["interval"] = "1wk"
    elif frequency == "monthly":
        query_params["interval"] = "1mo"
    else:
        return {
            "symbol": symbol,
            "frequency": frequency,
            "data": [],
            "error": {"code": "INVALID_FREQUENCY", "message": f"Invalid frequency: {frequency}"}
        }

    # Handle date parameters
    if start_date_str and end_date_str:
        try:
            query_params["period1"] = str(datetime_to_epoch_seconds(start_date_str))
            query_params["period2"] = str(datetime_to_epoch_seconds(end_date_str, is_end_date=True))
        except ValueError:
            return {
                "symbol": symbol, 
                "frequency": frequency,
                "data": [],
                "error": {"code": "INVALID_DATE_FORMAT", "message": "Date format should be YYYY-MM-DD"}
            }
    elif start_date_str:
        try:
            query_params["period1"] = str(datetime_to_epoch_seconds(start_date_str))
            # Set period2 to today + 1 day if only start_date is provided
            today_plus_one = datetime.now(timezone.utc) + timedelta(days=1)
            query_params["period2"] = str(int(today_plus_one.timestamp()))
        except ValueError:
            return {
                "symbol": symbol, 
                "frequency": frequency,
                "data": [],
                "error": {"code": "INVALID_DATE_FORMAT", "message": "Start date format should be YYYY-MM-DD"}
            }
    elif end_date_str:
        try:
            query_params["period2"] = str(datetime_to_epoch_seconds(end_date_str, is_end_date=True))
            # Set period1 to end_date - 1 year if only end_date is provided
            end_dt_obj = datetime.strptime(end_date_str, "%Y-%m-%d")
            start_dt_obj = end_dt_obj - timedelta(days=365)
            query_params["period1"] = str(int(start_dt_obj.replace(tzinfo=timezone.utc).timestamp()))
        except ValueError:
            return {
                "symbol": symbol, 
                "frequency": frequency,
                "data": [],
                "error": {"code": "INVALID_DATE_FORMAT", "message": "End date format should be YYYY-MM-DD"}
            }
    else:
        # Default to 1 year range if no dates are provided
        query_params["range"] = "1y"

    # Call YahooFinance API
    try:
        api_response = client.call_api("YahooFinance/get_stock_chart", query=query_params)
    except Exception as e:
        return {
            "symbol": symbol,
            "frequency": frequency,
            "data": [],
            "error": {"code": "API_CALL_ERROR", "message": str(e)}
        }

    # Process API response
    if (api_response and api_response.get("chart") and 
        api_response["chart"].get("result") and 
        len(api_response["chart"]["result"]) > 0):
        
        result = api_response["chart"]["result"][0]
        meta = result.get("meta", {})
        timestamps = result.get("timestamp", [])
        indicators = result.get("indicators", {})
        quote = indicators.get("quote", [{}])[0] if indicators.get("quote") else {}
        adjclose_list = indicators.get("adjclose", [{}])[0].get("adjclose", []) if indicators.get("adjclose") and indicators["adjclose"][0].get("adjclose") else []

        if not timestamps or not quote.get("open") :
             return {
                "symbol": symbol,
                "frequency": frequency,
                "currency": meta.get("currency"),
                "exchange_name": meta.get("exchangeName"),
                "exchange_timezone_name": meta.get("exchangeTimezoneName"),
                "instrument_type": meta.get("instrumentType"),
                "data_granularity": meta.get("dataGranularity"),
                "data": [],
                "error": {"code": "NO_DATA_AVAILABLE", "message": "No historical data found for the given parameters."}
            }

        formatted_data = []
        for i, ts in enumerate(timestamps):
            data_point = {
                "timestamp": ts,
                "date": epoch_seconds_to_datetime_str(ts),
                "open": quote.get("open", [])[i] if i < len(quote.get("open", [])) else None,
                "high": quote.get("high", [])[i] if i < len(quote.get("high", [])) else None,
                "low": quote.get("low", [])[i] if i < len(quote.get("low", [])) else None,
                "close": quote.get("close", [])[i] if i < len(quote.get("close", [])) else None,
                "adj_close": adjclose_list[i] if i < len(adjclose_list) else None,
                "volume": quote.get("volume", [])[i] if i < len(quote.get("volume", [])) else None,
            }
            # Filter out points where essential data might be null (especially from Yahoo Finance for some intervals)
            if all(v is not None for v in [data_point["open"], data_point["high"], data_point["low"], data_point["close"]]):
                 formatted_data.append(data_point)

        return {
            "symbol": meta.get("symbol", symbol),
            "frequency": frequency,
            "currency": meta.get("currency"),
            "exchange_name": meta.get("exchangeName"),
            "exchange_timezone_name": meta.get("exchangeTimezoneName"),
            "instrument_type": meta.get("instrumentType"),
            "data_granularity": meta.get("dataGranularity"), # This is from Yahoo, e.g. 1d, 1wk, 1mo
            "data": formatted_data,
            "error": None
        }
    elif api_response and api_response.get("chart") and api_response["chart"].get("error"):
        return {
            "symbol": symbol,
            "frequency": frequency,
            "data": [],
            "error": {"code": "YAHOO_FINANCE_ERROR", "message": str(api_response["chart"]["error"]) }
        }
    else:
        return {
            "symbol": symbol,
            "frequency": frequency,
            "data": [],
            "error": {"code": "UNKNOWN_API_RESPONSE", "message": "Unknown or empty response from YahooFinance API."}
        }

if __name__ == "__main__":
    # Example Usage (for testing, not part of the final server)
    # print("Testing Ping An Bank (000001.SZ) daily for 1 month...")
    # data_pa = fetch_historical_stock_data(symbol="000001.SZ", frequency="daily", end_date_str="2024-04-30", start_date_str="2024-04-01")
    # import json
    # print(json.dumps(data_pa, indent=2, ensure_ascii=False))

    # print("\nTesting SSE Composite Index (000001.SS) weekly for last year...")
    # data_sse = fetch_historical_stock_data(symbol="000001.SS", frequency="weekly")
    # print(json.dumps(data_sse, indent=2, ensure_ascii=False))

    # print("\nTesting invalid symbol...")
    # data_invalid = fetch_historical_stock_data(symbol="INVALID.SYMBOL", frequency="daily")
    # print(json.dumps(data_invalid, indent=2, ensure_ascii=False))
    pass

