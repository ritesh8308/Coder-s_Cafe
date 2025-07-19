import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.models import MenuItem

def seed_menu_items():
    # Define sample menu items
    sample_menu = [
        MenuItem(name="Masala Dosa", price=40.0, category="South Indian", is_available=True),
        MenuItem(name="Paneer Burger", price=60.0, category="Snack", is_available=True),
        MenuItem(name="Cold Coffee", price=35.0, category="Beverage", is_available=True),
        MenuItem(name="French Fries", price=45.0, category="Side", is_available=True),
        MenuItem(name="Thali (Veg)", price=120.0, category="Combo", is_available=True),
    ]

    try:
        # Check if menu is already populated
        existing_count = MenuItem.query.count()
        if existing_count > 0:
            print(f"⚠️ Skipping insert: {existing_count} items already exist in the MenuItem table.")
            return

        # Bulk insert sample items
        db.session.bulk_save_objects(sample_menu)
        db.session.commit()
        print(f"✅ Success: Inserted {len(sample_menu)} sample items into MenuItem table.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error while populating menu items: {str(e)}")

def main():
    app = create_app()
    with app.app_context():
        seed_menu_items()

if __name__ == "__main__":
    main()
