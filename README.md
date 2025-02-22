# Pizzabot

Pizzabot is a Python application designed to help users find available reservation times at a specified restaurant. It checks the availability of dates and times based on user-defined filters and notifies users of available slots.

## Features

- **Availability Checking**: The bot checks for available dates and times at the restaurant for the next few months.
- **Customizable Filters**: Users can set filters for days of the week and time ranges to narrow down their search.
- **Notification System**: The bot notifies users of available reservation times and keeps track of already notified times to avoid duplicates.

## Requirements

- Python 3.12 or higher
- Required Python packages listed in `pyproject.toml`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pizzabot.git
   cd pizzabot
   ```

2. Install the required dependencies:
   ```bash
   uv install
   ```

## Configuration

Edit the `config.py` file to set your availability filters, restaurant ID, and number of guests.

## Usage

Run the main script:
```bash
python .
```
