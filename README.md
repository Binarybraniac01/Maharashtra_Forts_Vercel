# 🏰 Maharashtra Forts Travel Planner

**Comprehensive web application for efficient Maharashtra’s forts travel planning, offering detailed fort information, route optimization, and itinerary management.**

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://maharashtraforts.vercel.app/)
[![Django](https://img.shields.io/badge/Built%20with-Django-092E20)](https://www.djangoproject.com/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Vercel-000000)](https://vercel.com/)

## 📖 About The Project

**Maharashtra Forts** is a digital travel guide and smart itinerary planner designed for history enthusiasts and trekkers. The platform solves the complexity of planning multi-destination trips by providing route optimization, cost estimation, and detailed information about the majestic forts of Maharashtra.

Whether you are planning a one-day trip or a multi-day expedition, this application helps you organize your journey efficiently using real-time distance data and route optimization algorithms.

## ✨ Key Features

* **🗺️ Smart Route Optimization:**
    * Select multiple forts you wish to visit.
    * The app calculates the most optimal path using the **Routific API** (Vehicle Routing Problem solver).
    * Visualizes the route from your current location to all selected destinations.

* **💰 Trip Cost & Fuel Calculator:**
    * Estimates travel costs based on your vehicle's mileage and current fuel prices.
    * Provides total distance and estimated driving time.

* **🏰 Comprehensive Fort Database:**
    * Search forts by name or district.
    * View detailed information, history, and difficulty levels for each fort.
    * Get personalized recommendations based on your travel history.

* **👤 User Management:**
    * Secure user registration and login.
    * **Guest Access** for quick exploration without sign-up.
    * Dashboard to view and manage past trip plans (`Our Plans`).

* **📍 Location Services:**
    * Integrated geolocation to fetch user coordinates for accurate routing.

* **💬 Feedback System:**
    * Built-in module for users to report issues or share experiences.

## 🛠️ Tech Stack

**Backend:**
* **Framework:** Django 5.1.2 (Python)
* **Database:** PostgreSQL (Production), SQLite (Development)
* **Authentication:** Django Auth System

**Frontend:**
* **Templates:** Django Template Language (DTL)
* **Styling:** Bootstrap 5, Custom CSS
* **Scripting:** jQuery, JavaScript

**External APIs:**
* **Routific API:** For solving the Traveling Salesperson/Vehicle Routing Problem.
* **Distance Matrix AI:** For accurate travel distance and time calculations between locations.

**Deployment:**
* **Platform:** Vercel

## 🚀 Getting Started

Follow these instructions to set up the project locally for development.

### Prerequisites
* Python 3.10+
* PostgreSQL (optional for local dev, can use SQLite)
* API Keys for Routific and Distance Matrix AI

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/binarybraniac01/maharashtra_forts_vercel.git](https://github.com/binarybraniac01/maharashtra_forts_vercel.git)
    cd maharashtra_forts_vercel
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a `.env` file in the root directory (next to `manage.py`) and add the following keys. You will need to obtain your own API keys for the services used.

    ```env
    # Django Settings
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    ALLOWED_HOST=127.0.0.1,localhost

    # Database (If using PostgreSQL locally)
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432

    # External APIs
    ROUTE_API=your_routific_api_token
    DISTANCE_API=your_distance_matrix_api_key

    # Email Service (Gmail SMTP)
    Mail_USERNAME=your_email@gmail.com
    Mail_PASS=your_email_app_password
    ```

5.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Start the Development Server**
    ```bash
    python manage.py runserver
    ```
    Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📂 Project Structure

```text
Maharashtra_Forts_Vercel/
├── core/                  # Project configuration (settings, urls, wsgi)
├── home/                  # Main app: Homepage, Search, Fort Models, Route Logic
├── knowaboutforts/        # App for detailed fort information views
├── recommendations/       # App for user recommendations and trip history
├── user/                  # App for Authentication (Login/Register)
├── feedback/              # App for handling user feedback
├── public/                # Static files (CSS, JS, Images)
├── templates/             # HTML Templates
├── build_files.sh         # Vercel build script
└── requirements.txt       # Python dependencies
