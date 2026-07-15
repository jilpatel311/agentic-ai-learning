from sqlalchemy import select

from app.database.connection import (
    SessionLocal,
    engine,
)
from app.database.models import Base
from app.database.employee_model import Employee


Base.metadata.create_all(
    bind=engine
)


EMPLOYEES = [

    Employee(
        employee_name="Rahul Sharma",
        department="Engineering",
        designation="Senior Software Engineer",
        salary=85000,
        reward_points=2500,
        work_from_home_days=5,
        sick_leave_remaining=4,
        casual_leave_remaining=5,
        privilege_leave_remaining=8,
        email="rahul@company.com",
    ),

    Employee(
        employee_name="Priya Patel",
        department="Human Resources",
        designation="HR Manager",
        salary=90000,
        reward_points=6000,
        work_from_home_days=8,
        sick_leave_remaining=5,
        casual_leave_remaining=6,
        privilege_leave_remaining=10,
        email="priya@company.com",
    ),

    Employee(
        employee_name="Amit Verma",
        department="Engineering",
        designation="Backend Developer",
        salary=78000,
        reward_points=1800,
        work_from_home_days=4,
        sick_leave_remaining=3,
        casual_leave_remaining=4,
        privilege_leave_remaining=7,
        email="amit@company.com",
    ),

    Employee(
        employee_name="Neha Shah",
        department="Finance",
        designation="Finance Manager",
        salary=110000,
        reward_points=9000,
        work_from_home_days=10,
        sick_leave_remaining=6,
        casual_leave_remaining=6,
        privilege_leave_remaining=12,
        email="neha@company.com",
    ),

    Employee(
        employee_name="Karan Mehta",
        department="Engineering",
        designation="DevOps Engineer",
        salary=95000,
        reward_points=5000,
        work_from_home_days=7,
        sick_leave_remaining=5,
        casual_leave_remaining=5,
        privilege_leave_remaining=9,
        email="karan@company.com",
    ),

    Employee(
        employee_name="Jinal Patel",
        department="QA",
        designation="QA Engineer",
        salary=72000,
        reward_points=1400,
        work_from_home_days=6,
        sick_leave_remaining=4,
        casual_leave_remaining=6,
        privilege_leave_remaining=8,
        email="jinal@company.com",
    ),

    Employee(
        employee_name="Vivek Joshi",
        department="Engineering",
        designation="Tech Lead",
        salary=140000,
        reward_points=15000,
        work_from_home_days=10,
        sick_leave_remaining=6,
        casual_leave_remaining=6,
        privilege_leave_remaining=15,
        email="vivek@company.com",
    ),

    Employee(
        employee_name="Sneha Desai",
        department="Support",
        designation="Support Engineer",
        salary=65000,
        reward_points=900,
        work_from_home_days=2,
        sick_leave_remaining=4,
        casual_leave_remaining=5,
        privilege_leave_remaining=6,
        email="sneha@company.com",
    ),

    Employee(
        employee_name="Yash Modi",
        department="Sales",
        designation="Sales Executive",
        salary=70000,
        reward_points=2200,
        work_from_home_days=3,
        sick_leave_remaining=5,
        casual_leave_remaining=5,
        privilege_leave_remaining=7,
        email="yash@company.com",
    ),

    Employee(
        employee_name="Riya Singh",
        department="Marketing",
        designation="Marketing Executive",
        salary=68000,
        reward_points=1700,
        work_from_home_days=4,
        sick_leave_remaining=6,
        casual_leave_remaining=6,
        privilege_leave_remaining=8,
        email="riya@company.com",
    ),

]


def seed():

    session = SessionLocal()

    try:

        employee = session.execute(
            select(Employee)
        ).first()

        if employee:
            print(
                "Database already seeded."
            )
            return

        session.add_all(
            EMPLOYEES
        )

        session.commit()

        print(
            "10 Employees inserted successfully."
        )

    finally:

        session.close()


if __name__ == "__main__":

    seed()