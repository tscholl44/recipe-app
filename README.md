# Recipe App

A Django-based web application for managing and organizing recipes.

## Project Structure

```
recipe-app/
├── src/
│   ├── manage.py
│   ├── recipe_project/          # Main Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── recipes/                 # Recipe app
│       ├── models.py           # Recipe data models
│       ├── views.py            # Application views
│       ├── admin.py            # Django admin configuration
│       ├── tests.py            # Unit tests
│       └── migrations/         # Database migrations
├── db.sqlite3                  # SQLite database
└── README.md
```

## Features

- Create, read, update, and delete recipes
- Recipe difficulty calculation based on cooking time and ingredients
- Ingredient management
- Cooking time tracking

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.x

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd recipe-app
```

2. Create a virtual environment:
```bash
python -m venv recipe-env
recipe-env\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install django
```

4. Navigate to the project directory:
```bash
cd src
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Running Tests

To run the test suite:

```bash
cd src
python manage.py test recipes
```

## Usage

- Access the Django admin panel at `/admin/` to manage recipes
- Use the web interface to browse and manage your recipe collection

## Models

### Recipe
- **name**: Recipe name (max 120 characters)
- **cooking_time**: Cooking time in minutes (positive integer)
- **ingredients**: Comma-separated list of ingredients
- **difficulty**: Auto-calculated based on cooking time and ingredient count

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## License

This project is for educational purposes.