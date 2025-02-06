# Audio Archive

Audio Archive is a podcast streaming website built with Flask. It allows users to create, explore, and listen to podcasts. Users can also comment on episodes and follow their favorite shows.

## Features

- User authentication (sign up, log in, log out)
- Create and manage podcasts and episodes
- Explore podcasts by category
- Comment on episodes
- Follow podcasts
- Responsive design

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/audio-archive.git
    cd audio-archive
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    flask db upgrade
    ```

5. Run the application:
    ```sh
    flask run
    ```

## Usage

- Visit `http://127.0.0.1:5000/` to access the home page.
- Sign up for a new account or log in with an existing account.
- Create new podcasts and episodes.
- Explore podcasts by category.
- Comment on episodes and follow your favorite shows.
