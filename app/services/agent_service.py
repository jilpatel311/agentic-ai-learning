from app.mcp_server.tools.calculator import CalculatorTool
from app.mcp_server.tools.database import DatabaseTool

from app.services.groq_service import GroqService
from app.services.search_service import SearchService


class AgentService:

    def __init__(self):

        self.groq_service = GroqService()

        self.calculator_tool = CalculatorTool()

        self.database_tool = DatabaseTool()

        self.search_service = SearchService()

    def process_question(
        self,
        question: str,
    ):

        plan = self.groq_service.create_execution_plan(
            question
        )
        print("plannnnn", plan)
        tool = plan.get("tool")

        if tool == "calculator":

            return self._execute_calculator(
                plan
            )

        if tool == "database":

            return self._execute_database(
                plan
            )

        return self._execute_rag(
            question
        )

    def _execute_calculator(
        self,
        plan: dict,
    ):

        expression = plan.get(
            "expression",
            "",
        )

        result = self.calculator_tool.calculate(
            expression
        )

        return {

            "tool_used": "calculator",

            "answer": str(result),

            "sources": []

        }

    def _execute_database(
        self,
        plan: dict,
    ):

        action = plan.get("action")

        if action == "employee_count":

            count = self.database_tool.get_employee_count()

            return {

                "tool_used": "database",

                "answer": f"There are {count} employees in the company.",

                "sources": []

            }

        if action == "highest_salary":

            employee = self.database_tool.get_highest_salary_employee()

            return {

                "tool_used": "database",

                "answer": (
                    f"{employee['employee_name']} has the highest salary "
                    f"of ₹{employee['salary']}."
                ),

                "sources": []

            }

        if action == "employee_salary":

            employee = self.database_tool.get_employee_by_name(
                plan["employee_name"]
            )

            return {

                "tool_used": "database",

                "answer": (
                    f"{employee['employee_name']}'s salary is "
                    f"₹{employee['salary']}."
                ),

                "sources": []

            }

        if action == "employee_reward_points":

            reward_points = self.database_tool.get_employee_reward_points(
                plan["employee_name"]
            )

            return {

                "tool_used": "database",

                "answer": (
                    f"{plan['employee_name']} has "
                    f"{reward_points} reward points."
                ),

                "sources": []

            }

        if action == "employee_leave_balance":

            leave = self.database_tool.get_employee_leave_balance(
                plan["employee_name"]
            )

            return {

                "tool_used": "database",

                "answer": (
                    f"{plan['employee_name']} has "
                    f"{leave['casual_leave']} Casual Leave, "
                    f"{leave['sick_leave']} Sick Leave and "
                    f"{leave['privilege_leave']} Privilege Leave remaining."
                ),

                "sources": []

            }

        if action == "employees_by_department":

            employees = self.database_tool.get_employees_by_department(
                plan["department"]
            )

            employee_names = [

                employee["employee_name"]

                for employee in employees

            ]

            return {

                "tool_used": "database",

                "answer": (
                    f"{plan['department']} department employees: "
                    + ", ".join(employee_names)
                ),

                "sources": []

            }

        return {

            "tool_used": "database",

            "answer": "Unsupported database action.",

            "sources": []

        }

    def _execute_rag(
        self,
        question: str,
    ):

        response = self.search_service.search(
            session_id="default",
            question=question,
        )

        return {

            "tool_used": "rag",

            "answer": response["answer"],

            "sources": response["sources"]

        }