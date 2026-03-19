from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.module import Module
from app.models.support import SupportResource
from app.utils.security import hash_password

app = create_app()

def seed_database():
    with app.app_context():
        # 1. Admin User
        admin_email = 'admin@serenity.com'
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            print(f"Creating admin user: {admin_email}")
            admin = User(
                email=admin_email,
                password_hash=hash_password('AdminSecure123!'),
                is_admin=True
            )
            db.session.add(admin)
        else:
            print(f"Admin user {admin_email} already exists.")

        # 2. Educational Modules
        modules_data = [
            {
                "title": "Understanding Anxiety",
                "description": "Learn the biological and psychological mechanisms behind anxiety and how to manage it.",
                "content": "<p>Anxiety is a natural response to stress, but when it becomes overwhelming, it can interfere with daily life. This module covers the basic symptoms, including increased heart rate and racing thoughts.</p><h3>Management Techniques</h3><ul><li>Deep breathing exercises</li><li>Mindfulness meditation</li><li>Cognitive Behavioral Therapy (CBT) basics</li></ul>"
            },
            {
                "title": "Developing Healthy Sleep Habits",
                "description": "Sleep hygiene is critical to mental well-being. Discover actionable tips for better rest.",
                "content": "<p>Quality sleep is foundationally linked to emotional regulation and cognitive function.</p><h3>Tips for Better Sleep</h3><ul><li>Maintain a consistent sleep schedule even on weekends.</li><li>Avoid screens at least 1 hour before bed.</li><li>Ensure a cool, dark, and quiet sleeping environment.</li></ul>"
            },
            {
                "title": "Navigating Burnout",
                "description": "Identify the signs of professional and emotional burnout and steps toward recovery.",
                "content": "<p>Burnout is a state of emotional, physical, and mental exhaustion caused by excessive and prolonged stress.</p><h3>Recovery Strategies</h3><ul><li>Set clear boundaries between work and personal life.</li><li>Prioritize self-care and hobbies.</li><li>Seek support from colleagues or professionals.</li></ul>"
            }
        ]

        for mod_data in modules_data:
            existing_mod = Module.query.filter_by(title=mod_data['title']).first()
            if not existing_mod:
                print(f"Adding module: {mod_data['title']}")
                db.session.add(Module(**mod_data))

        # 3. Support Resources
        resources_data = [
            {
                "name": "National Crisis Hotline",
                "phone_number": "988",
                "description": "Available 24/7. Free and confidential support for people in distress, prevention and crisis resources."
            },
            {
                "name": "Veterans Crisis Line",
                "phone_number": "988 (Press 1)",
                "description": "Connect with the Veterans Crisis Line to reach caring, qualified responders specifically trained to support Veterans."
            },
            {
                "name": "The Trevor Project",
                "phone_number": "1-866-488-7386",
                "description": "Information and support to LGBTQ young people 24/7, all year round."
            }
        ]

        for res_data in resources_data:
            existing_res = SupportResource.query.filter_by(name=res_data['name']).first()
            if not existing_res:
                print(f"Adding support resource: {res_data['name']}")
                db.session.add(SupportResource(**res_data))

        db.session.commit()
        print("Database seeding completed securely.")

if __name__ == '__main__':
    seed_database()
