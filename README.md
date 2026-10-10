# Fake Bill Detection Using Machine Learning

A Django web application that accepts six manually entered banknote measurements and uses a Decision Tree classifier to predict whether a bill is genuine or fake. The project combines a web interface with a scikit-learn model.

## Features
- Form-based entry of banknote measurements: diagonal, left/right height, lower/upper margin, and length
- Decision Tree classification with scikit-learn
- Django web interface
- User sign-up/login pages and project information pages

## Tech Stack
- Python
- Django
- Pandas
- scikit-learn (Decision Tree)
- SQLite (default local database)
- HTML/CSS

## Important: Training Data Required
The bill measurements are entered manually through the web form, but the classifier must first learn from labelled training examples. The original code referred to a local `fake_bills.csv` file that was not included in the supplied project ZIP. Therefore, predictions will not work until you provide the original training CSV. This repository does **not** include a dataset or claim to make valid predictions without one.

The CSV is expected to contain these columns:
`diagonal`, `height_left`, `height_right`, `margin_low`, `margin_up`, `length`, `is_genuine`.

Place `fake_bills.csv` in the project root (beside `manage.py`) or set the `FAKE_BILLS_DATASET` environment variable to its location. Keep the dataset out of GitHub unless you have permission to redistribute it.

## Setup
Requires Python 3.10 or later.

1. Clone the repository and open its folder.
2. Create and activate a virtual environment:

   **Windows (PowerShell)**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. Open `http://127.0.0.1:8000/Predict/`.

## Project Structure
- `manage.py` — Django management utility
- `Fakebill/` — Django project settings and URL configuration
- `basics/` — application views, models, migrations, and HTML templates

## Limitations
- Prediction depends on the original labelled training CSV; it is not included in this repository.
- The Django development server and sample secret key are for local development only, not production deployment.
- The sign-up form and authentication flow should be reviewed before production use.

## Project Type
Academic machine-learning and web-development project.
