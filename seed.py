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
            },
            {
                "title": "Understanding Depression",
                "description": "Learn the signs, symptoms, and coping strategies for depression.",
                "content": "<p>Depression is more than just feeling sad. It is a serious mental health condition that requires understanding and medical intervention when necessary.</p><h3>Coping Mechanisms</h3><ul><li>Establishing a safe daily routine.</li><li>Breaking large tasks into smaller steps.</li><li>Engaging actively with professional therapists.</li></ul>"
            },
            {
                "title": "Overcoming Imposter Syndrome",
                "description": "Strategies to combat feelings of inadequacy and self-doubt in academic and professional capacities.",
                "content": "<p>Imposter syndrome involves feeling like a fraud despite evident success. We break down the internalized fear of being 'found out'.</p><h3>Combating It</h3><ul><li>Acknowledge your personal achievements.</li><li>Separate feelings from absolute facts.</li><li>Develop a healthy response to failure.</li></ul>"
            },
            {
                "title": "Digital Detox for Mental Health",
                "description": "How to manage screen time intentionally to dramatically improve deep emotional well-being.",
                "content": "<p>Constant digital connectivity can unknowingly lead to chronic burnout and pervasive anxiety. Unplugging correctly clears the noise.</p><h3>Detox Strategies</h3><ul><li>Implement strict 'no-screen' zones in your house.</li><li>Turn off non-essential notifications permanently.</li><li>Re-engage realistically with analog hobbies.</li></ul>"
            }
        ]

        for mod_data in modules_data:
            existing_mod = Module.query.filter_by(title=mod_data['title']).first()
            if not existing_mod:
                print(f"Adding module: {mod_data['title']}")
                db.session.add(Module(**mod_data))

        # 3. Support Resources (South African Localized)
        resources_data = [
            {
                "name": "SADAG Suicide Crisis Line",
                "phone_number": "0800 567 567",
                "description": "Available 24/7. Providing dedicated, professional counseling and support to those in crisis."
            },
            {
                "name": "Lifeline South Africa",
                "phone_number": "0861 322 322",
                "description": "Offering 24-hour emotional support and trauma counseling. We are here to listen."
            },
            {
                "name": "Gender-Based Violence Command Centre",
                "phone_number": "0800 428 428",
                "description": "A 24/7 call centre assisting victims of gender-based violence."
            },
            {
                "name": "Childline South Africa",
                "phone_number": "116",
                "description": "Toll-free helpline providing safety for children and families in immediate crisis."
            },
            {
                "name": "SANCA National",
                "phone_number": "011 892 3829",
                "description": "South African National Council on Alcoholism and Drug Dependence. Help for acute substance abuse."
            },
            {
                "name": "Triangle Project",
                "phone_number": "021 712 6699",
                "description": "LGBTQ+ support line offering professional counseling, crisis intervention, and empowerment clinics."
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
