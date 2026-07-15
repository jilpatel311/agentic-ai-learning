from app.database.repository.employee_repository import (
    EmployeeRepository,
)


class DatabaseTool:

    def __init__(self):

        self.repository = EmployeeRepository()

    def get_employee_count(self):

        return self.repository.get_employee_count()

    def get_employee_reward_points(
        self,
        employee_name: str,
    ):

        return self.repository.get_employee_reward_points(
            employee_name
        )

    def get_employee_leave_balance(
        self,
        employee_name: str,
    ):

        return self.repository.get_employee_leave_balance(
            employee_name
        )

    def get_highest_salary_employee(self):

        employee = self.repository.get_highest_salary_employee()

        if not employee:
            return None

        return {

            "employee_name": employee.employee_name,

            "salary": employee.salary,

            "designation": employee.designation,

            "department": employee.department,

        }

    def get_employee_by_name(
        self,
        employee_name: str,
    ):

        employee = self.repository.get_employee_by_name(
            employee_name
        )

        if not employee:
            return None

        return {

            "employee_name": employee.employee_name,

            "department": employee.department,

            "designation": employee.designation,

            "salary": employee.salary,

            "reward_points": employee.reward_points,

            "work_from_home_days": employee.work_from_home_days,

            "sick_leave_remaining": employee.sick_leave_remaining,

            "casual_leave_remaining": employee.casual_leave_remaining,

            "privilege_leave_remaining": employee.privilege_leave_remaining,

            "email": employee.email,

        }

    def get_employees_by_department(
        self,
        department: str,
    ):

        employees = self.repository.get_employee_by_department(
            department
        )

        return [

            {

                "employee_name": employee.employee_name,

                "designation": employee.designation,

                "salary": employee.salary,

            }

            for employee in employees

        ]