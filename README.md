# Concesionario Django Project

Welcome to the **Concesionario Django Project**! This web application, developed as part of the ITEC Río Cuarto program, is designed to manage a car dealership. The project explores the full capabilities of Django using the Model-Template-View (MTV) architecture.

**Please note that this project is currently in development and is not intended for production use.** It serves as a course assignment, with the primary goal of showcasing Django's features in a controlled environment.

## Table of Contents

- Features
- Installation
- Usage
- Project Structure
- Configuration
- Technical Details
- Disclaimer
- Credits
- License

## Key Features

- **App Structure**: The project is organized into four main Django apps: `Vehicles`, `Comments`, `Users`, and `Media`, each handling different aspects of the application.
- **No JavaScript**: The project is built purely using Django's Model-Template-View architecture with Python and HTML, without any JavaScript.
- **Image Management**: Images are stored with unique filenames generated using UUIDs to avoid conflicts and ensure consistency.
- **Admin Capabilities**: Admin users have full management capabilities, including uploading and managing images through both the frontend interface and the Django admin backend.
- **User Roles**: The application supports different user roles, each with varying permissions.
- **User Registration and Authentication**: Secure user registration, login, and logout processes.
- **Vehicle Management**: Admins can add, update, and delete vehicles, and upload images.
- **Commenting System**: Users can leave comments on vehicles, with admins and moderators managing these comments.
- **Vehicle Following**: Users can follow specific vehicles and view them in their profiles.
- **Dynamic Filtering**: In the admin panel, vehicles can be filtered by various criteria such as brand, price, and year of manufacture.
- **Context Processors**: Custom context processors dynamically inject user status into templates.


## Installation

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10 or higher
- Django 5.1 or higher
- A virtual environment tool like `venv`
- Git for version control

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Did11/oliva-django-concesionario.git
    cd oliva-django-concesionario
    ```

2. **Set Up the Virtual Environment**

    ```bash
    python3 -m venv entorno
    source entorno/bin/activate  # On Windows use `entorno\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

The project will be available at `http://127.0.0.1:8000`.

*Note: The project comes with a pre-populated database, including admin users and demo data, so no need to create a new superuser or apply migrations.*


## Usage

- **Admin Panel**: Access the admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials. From here, you can manage vehicles, images, comments, and user roles with full control.
- **Vehicle Listings**: Explore the comprehensive list of vehicles by visiting the cars section at `http://127.0.0.1:8000/vehicles/`. Users can filter vehicles by various criteria, view detailed information, and interact with features like commenting and following vehicles.
- **User Profile**: After logging in, users can access their profile at `http://127.0.0.1:8000/profile/` to manage their followed vehicles, edit their comments, and update their account details.

## Configuration



## Credits

- **Developed by**: Oliva, Didier. 

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
