# ☕ Cafe Spotter

Discover the best cafes in London tailored to your needs. Whether you're looking for a place with ample seating, reliable Wi-Fi, or the perfect ambiance to make calls, Cafe Spotter has got you covered.

🔗 **Live Demo:** [https://cafespotter.onrender.com](https://cafespotter.onrender.com)

---

## 📸 Screenshots

![Home Page]![image](https://github.com/user-attachments/assets/ecfeabff-ab7a-40e4-812d-461a3128e464)


![Cafe Details]![image](https://github.com/user-attachments/assets/37668dd8-7975-43ae-a5ea-6773a1b5a0e2)




---

## 🚀 Features

- 📍 **Comprehensive Cafe Listings**: View detailed information about various cafes in London.
- 🔍 **Search Functionality**: Find cafes based on location or specific amenities.
- 🖼️ **Visual Appeal**: Each listing includes images to give you a glimpse of the cafe's ambiance.
- 📱 **Responsive Design**: Optimized for both desktop and mobile devices.
- 🧾 **User Authentication**: Sign up and log in to personalize your experience.

---

## 🛠️ Built With

- **Python 3** / **Flask**: Backend framework.
- **Jinja2**: Templating engine.
- **SQLite**: Lightweight database for storing cafe information.
- **Bootstrap 5**: Frontend framework for responsive design.
- **Render**: Deployment platform.

---

## 📦 Installation (Local Setup)

To run this project locally, follow the steps below:

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/cafe-spotter.git
cd cafe-spotter

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate
On Windows: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Set up environment variables
Create a .env file in the root directory and add:
SECRET_KEY and your_flask_secret_key

# 5. Initialize the database
flask db init
flask db migrate
flask db upgrade

# 6. Run the Flask development server
flask run
