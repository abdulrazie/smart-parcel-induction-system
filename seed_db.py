"""
Database Initialization & Seeding Script
----------------------------------------
This standalone script tests your database connection, creates all required tables,
and seeds initial sample data (students, couriers, and a sample parcel).

Run this with:
    python seed_db.py
"""

from app.database import engine, SessionLocal
from app.models import Base, Student, Courier, Parcel, ParcelStatus


def init_and_seed():
    print("=" * 60)
    print("[INIT] Initializing Smart Parcel Induction System Database...")
    print("=" * 60)

    # Step 1: Create all tables defined in Base.metadata
    print("\n[1/3] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] Tables created successfully (students, couriers, parcels).")

    # Step 2: Open a database session
    db = SessionLocal()

    try:
        # Step 3: Check if already seeded
        existing_couriers = db.query(Courier).count()
        if existing_couriers > 0:
            print("\n[INFO] Database already contains data. Skipping seed step.")
        else:
            print("\n[2/3] Seeding initial sample data...")

            # --- Couriers ---
            couriers = [
                Courier(name="DHL Express"),
                Courier(name="FedEx"),
                Courier(name="PosLaju"),
                Courier(name="J&T Express"),
            ]
            db.add_all(couriers)
            db.flush()  # Flushes changes to populate courier.id for foreign keys

            # --- Students ---
            students = [
                Student(
                    matric_number="A21EC0001",
                    name="Sarah Lee",
                    email="sarah.lee@university.edu",
                    phone_number="+60123456781",
                    dorm_block="Kolej Rahman, Block A-201"
                ),
                Student(
                    matric_number="A21EC0002",
                    name="Adam Haris",
                    email="adam.haris@university.edu",
                    phone_number="+60123456782",
                    dorm_block="Kolej Rahman, Block B-105"
                ),
                Student(
                    matric_number="A21EC0003",
                    name="Nurul Izzati",
                    email="nurul.izzati@university.edu",
                    phone_number="+60123456783",
                    dorm_block="Kolej Tuanku, Block C-304"
                ),
            ]
            db.add_all(students)
            db.flush()  # Flushes changes to populate student.id for foreign keys

            # --- Initial Parcel ---
            sample_parcel = Parcel(
                tracking_number="DHL9876543210",
                student_id=students[0].id,
                courier_id=couriers[0].id,
                shelf_location="Shelf A-02",
                status=ParcelStatus.PENDING
            )
            db.add(sample_parcel)

            # Commit all changes to the database in a single transaction
            db.commit()
            print("[SUCCESS] Initial data seeded successfully!")

        # Step 4: Verify and print the data
        print("\n[3/3] Verifying database records...")
        print("-" * 60)
        
        all_students = db.query(Student).all()
        print(f"Students count: {len(all_students)}")
        for s in all_students:
            print(f"   * [{s.matric_number}] {s.name} ({s.email}) - {s.dorm_block}")

        all_couriers = db.query(Courier).all()
        print(f"\nCouriers count: {len(all_couriers)}")
        for c in all_couriers:
            print(f"   * {c.name} (Active: {c.is_active})")

        all_parcels = db.query(Parcel).all()
        print(f"\nParcels count: {len(all_parcels)}")
        for p in all_parcels:
            print(
                f"   * Tracking: {p.tracking_number} | "
                f"Student: {p.student.name} | "
                f"Courier: {p.courier.name} | "
                f"Shelf: {p.shelf_location} | "
                f"Status: {p.status} | "
                f"Pickup Code: {p.pickup_code}"
            )
        print("-" * 60)
        print("[SUCCESS] Database setup and verification complete!\n")

    except Exception as e:
        db.rollback()  # Rollback transaction on error
        print(f"❌ Error occurred: {e}")
        raise
    finally:
        db.close()  # Always close the session


if __name__ == "__main__":
    init_and_seed()
