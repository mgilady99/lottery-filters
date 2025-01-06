# Lottery Number Filter

A web application for filtering lottery number combinations based on various criteria.

## Features

- Generate all possible combinations for any lottery format
- Filter by number of odd numbers
- Filter by range between first and last number
- Filter by differences between adjacent numbers
- Filter by sum of numbers
- Filter by must-include numbers
- Random selection of combinations
- Export results to CSV

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

```bash
python app.py
```

Visit `http://localhost:5000` in your web browser.

## Deployment

This application is ready to deploy to Render.com:

1. Create a new account on Render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

## Environment Variables

- `PORT`: Port number (default: 5000)
- `SECRET_KEY`: Flask secret key for session management

## License

MIT License
