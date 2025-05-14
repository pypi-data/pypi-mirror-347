#/home/ubuntu/mcp_server/app.py
from flask import Flask, request, jsonify
import sys
# Add the directory to sys.path to allow direct import of provider modules
from .yahoo_finance_provider import fetch_historical_stock_data
from .akshare_provider import fetch_sse_stock_overview, fetch_szse_industry_transaction_data

app = Flask(__name__)

@app.route("/mcp/marketdata/history", methods=["GET"])
def get_historical_data():
    symbol = request.args.get("symbol")
    frequency = request.args.get("frequency")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not symbol or not frequency:
        return jsonify({"error": {"code": "MISSING_PARAMETERS", "message": "Symbol and frequency are required."}}), 400

    data = fetch_historical_stock_data(symbol, frequency, start_date, end_date)
    if data.get("error"):
        # Distinguish between client errors (e.g., invalid symbol) and server errors
        if data["error"]["code"] in ["INVALID_FREQUENCY", "INVALID_DATE_FORMAT", "YAHOO_FINANCE_ERROR", "NO_DATA_AVAILABLE"]:
            return jsonify(data), 400 # Bad request or not found type errors
        return jsonify(data), 500 # Internal server error for others
    return jsonify(data)

@app.route("/mcp/marketdata/sse/overview", methods=["GET"])
def get_sse_overview():
    data = fetch_sse_stock_overview()
    if data.get("error"):
        return jsonify(data), 500
    return jsonify(data)

@app.route("/mcp/marketdata/szse/industry_transactions", methods=["GET"])
def get_szse_industry_transactions():
    symbol = request.args.get("symbol")
    date_str = request.args.get("date") # Parameter name from design doc is 'date'

    if not symbol or not date_str:
        return jsonify({"error": {"code": "MISSING_PARAMETERS", "message": "Symbol and date are required."}}), 400

    data = fetch_szse_industry_transaction_data(symbol, date_str)
    # Since this is currently a placeholder that returns an error, 
    # we might want to return a specific status code like 501 Not Implemented
    if data.get("error") and data["error"].get("code") == "SZSE_INDUSTRY_DATA_NOT_IMPLEMENTED":
        return jsonify(data), 501
    elif data.get("error"):
        return jsonify(data), 500
        
    return jsonify(data)

if __name__ == "__main__":
    # Note: For deployment, a proper WSGI server like Gunicorn should be used.
    # Listening on 0.0.0.0 to be accessible externally if port is exposed.
    app.run(host="0.0.0.0", port=5000, debug=True)

