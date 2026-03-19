# Mental Health Platform

A production-ready mental health platform designed to educate users and provide accessible support.

## 🛠 Technology Stack & Architecture
- **Backend**: Python Flask (Application Factory Pattern)
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic
- **Production Environment**: Gunicorn + Nginx
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript

## 🎨 UI/UX Design & Aesthetics
- **Theme**: Minimalist, professional, and elegant (Crisp White backgrounds, Deep Black text, Dusty Bronze/Gold accents)
- **Responsiveness**: Strictly Mobile-first approach, fluid across all screens
- **Accessibility**: strict adherence to WCAG 2.1 AA standards featuring proper ARIA labels and high contrast

## 🔒 Security & Data Protection
- Defense against OWASP Top 10 vulnerabilities
- Strong password hashing (Argon2 / bcrypt)
- Secure, HttpOnly, and SameSite session cookies
- Rigorous input validation and sanitization
- HTTPS/SSL, strict CSP, and Rate Limiting (Flask-Limiter)

## ⚡ Technical SEO & Performance
- Sub-second loading speeds via asset minification and caching
- Dynamic meta tags, semantic HTML5, Schema.org structured data, clean URL routing
- Secure error tracking and monitoring

## 🚀 Features
- Secure Registration, Login, and Session Management
- Scalable Educational Mental Health Modules
- Support Directory & Contact Interface for Crisis Resources

## 💻 Running the Application Locally

1. **Clone the Repository**
   ```bash
   git clone git@github.com:thulanesigasa/mental_health.git
   cd mental_health
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   *If starting fresh, run the following to apply migrations. Note: SQLite is used as the default fallback locally.*
   ```bash
   export FLASK_APP=run.py
   flask db upgrade
   ```

5. **Run the Development Server**
   ```bash
   flask run
   ```
   *The application will securely serve your local instance at `http://127.0.0.1:5000`.*
