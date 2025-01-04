import logging
from dash import Dash
from data_utils import load_data_from_db
from layout import create_layout
from callbacks import register_callbacks
from config import init_ngrok

def main():
    # Initialize ngrok
    public_url = init_ngrok(port=8055)

    # Load data from the database
    data = load_data_from_db()
    if data.empty:
        logging.error("Failed to load data from the database.")
        return

    # Initialize Dash app
    app = Dash(__name__)
    app.layout = create_layout(data)
    register_callbacks(app, data)

    # Run the app
    print(f"App running at: {public_url}")
    app.run_server(port=8055, debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
