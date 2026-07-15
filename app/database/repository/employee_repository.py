from sqlalchemy import func
from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.employee_model import Employee


class EmployeeRepository:

    def __init__(self):

        self.session = SessionLocal()

    def get_all_employees(self):

        return self.session.scalars(
            select(Employee)
        ).all()

    def get_employee_by_name(
        self,
        employee_name: str,
    ):

        return self.session.scalar(

            select(Employee)

            .where(
                Employee.employee_name == employee_name
            )
        )

    def get_employee_count(self):

        return self.session.scalar(

            select(
                func.count(Employee.employee_id)
            )

        )

    def get_employee_by_department(
        self,
        department: str,
    ):

        return self.session.scalars(

            select(Employee)

            .where(
                Employee.department == department
            )

        ).all()

    def get_highest_salary_employee(self):

        return self.session.scalar(

            select(Employee)

            .order_by(
                Employee.salary.desc()
            )

            .limit(1)

        )

    def get_employee_reward_points(
        self,
        employee_name: str,
    ):

        employee = self.get_employee_by_name(
            employee_name
        )

        if not employee:
            return None

        return employee.reward_points

    def get_employee_leave_balance(
        self,
        employee_name: str,
    ):

        employee = self.get_employee_by_name(
            employee_name
        )

        if not employee:
            return None

        return {

            "sick_leave": employee.sick_leave_remaining,

            "casual_leave": employee.casual_leave_remaining,

            "privilege_leave": employee.privilege_leave_remaining,

        }

    def close(self):

        self.session.close()