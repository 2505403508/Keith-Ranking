# Keith Ranking

Keith Ranking is a Flask website for browsing and ranking games. Users can search for games and companies, view game information, save favourites and receive game recommendations. The website uses Python, Flask, Jinja, SQLite, HTML and CSS.

## Main Features

- Browse all games and open game detail pages
- Browse developers and publishers
- Search for games and companies
- View the game ranking page
- Receive a random game recommendation without logging in
- Create an account and log in with a username or email
- Save and remove favourite games and companies
- View personal favourites
- Record browsing history for logged-in users
- Receive a personal recommendation based on the most viewed genre
- Clear personal recommendation history
- Custom 404 and 500 error pages
- Responsive design for desktop and mobile screens

## Software Needed

- Windows 10 or Windows 11
- Python 3.12 is recommended
- Command Prompt (CMD)
- A web browser such as Google Chrome

SQLite is included with Python, so a separate SQLite installation is not needed for running this project.

## 1. Install Python

1. Download Python from https://www.python.org/downloads/
2. Open the installer.
3. Select `Add python.exe to PATH` before installing Python.
4. Finish the installation.
5. Open Command Prompt and check the installation:

```cmd
python --version
python -m pip --version
```

If both commands show version numbers, Python and pip are ready.

## 2. Open the Project Folder

Open Command Prompt and move to the folder that contains `app.py`.

If the project is stored somewhere else, replace the path with the correct folder location.

## 3. Create a Python Virtual Environment

Create a virtual environment so the project packages are kept separate from other Python projects.

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

When it is active, `(venv)` should appear at the beginning of the CMD line.

## 4. Install the Requirements

The required packages are listed in `requirements.txt`.

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs Flask and Werkzeug. Flask also installs the packages it needs, including Jinja2.

## 5. Run the Website

Make sure CMD is still inside the project folder and the virtual environment is active. Then run:

```cmd
python app.py
```

CMD should show a local address similar to:

```text
http://127.0.0.1:5000
```

Open this address in a web browser. The Keith Ranking home page should appear.

To stop the server, return to CMD and press:

```text
Ctrl + C
```

To leave the virtual environment, run:

```cmd
deactivate
```

## How to Use the Website

### Browse and Search

Use the navigation bar to open Home, Games, Companies or Ranking. The search boxes can be used to find a game or company. Search text is cleaned and limited to 100 characters.

### Random Recommendation

Open the recommendation page and choose Random Recommendation. This feature works without an account.

### Account and Favourites

Choose Sign Up to create an account. After logging in, open a game or company page and use the favourite button. Saved items appear on the Favourites page.

### Personal Recommendation

Log in and open some game detail pages. Each different game is added to the user's browsing history once. Open Personal Recommendation to receive an unviewed game from the most viewed genre where possible. The history can be removed with the Clear History button.

## Database

The working database is included at:

```text
database/app.db
```

The database structure is stored at:

```text
database/app_schema.sql
```

Run the website from the main project folder because the Python routes use the relative database path `database/app.db`.

## Project Structure

```text
Keith-Ranking/
|-- app.py
|-- requirements.txt
|-- database/
|   |-- app.db
|   `-- app_schema.sql
|-- routes/
|   `-- pages/
|-- templates/
`-- static/
    |-- css/
    `-- images/
```

## Common Problems

### Python is not recognised

Reinstall Python and make sure `Add python.exe to PATH` is selected. Close and reopen CMD after installing it.

### Flask cannot be found

Activate the virtual environment and install the requirements again:

```cmd
venv\Scripts\activate
python -m pip install -r requirements.txt
```

### The database cannot be opened

Check that CMD is inside the folder containing `app.py`, and make sure `database/app.db` has not been moved or deleted.

### The local address does not open

Check that `python app.py` is still running in CMD. Do not close the CMD window while using the website.

## Note

This is a local school project. Flask's development server is suitable for running and demonstrating the website on a local computer.
