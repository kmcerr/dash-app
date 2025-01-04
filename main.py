import logging
from dash import Dash
from data_utils import load_data_from_db
from layout import create_layout
from callbacks import register_callbacks

def main():
    data = load_data_from_db()
    if data.empty:
        logging.error("Failed to load data from the database.")
        return

    app = Dash(__name__)
    app.layout = create_layout(data)
    register_callbacks(app, data)
    app.run_server(port=8053, debug=True)

if __name__ == "__main__":
    main()
