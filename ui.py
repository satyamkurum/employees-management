import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuration 
API_BASE_URL = "https://employees-management-backend-9jey.onrender.com"

# Authentication Function
def login_user(username, password):
    """Logs in the user and stores the token in the session state."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/token",
            data={"username": username, "password": password},
            timeout=5
        )
        response.raise_for_status()  
        st.session_state['token'] = response.json()['access_token']
        st.success("Logged in successfully!")
        st.rerun()
    except requests.exceptions.RequestException as e:
        st.error(f"Login failed: {e}")
        if 'token' in st.session_state:
            del st.session_state['token']

def get_auth_headers():
    """Returns authorization headers if the user is logged in."""
    if 'token' in st.session_state:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}

# UI Layout
st.set_page_config(page_title="Employee Dashboard", layout="wide")
st.title("Employee Management System")

# Authentication UI 
st.sidebar.title("Authentication")
if 'token' not in st.session_state:
    with st.sidebar.form("login_form"):
        username = st.text_input("Username", value="testuser")
        password = st.text_input("Password", type="password", value="testpassword")
        submitted = st.form_submit_button("Login")
        if submitted:
            login_user(username, password)
else:
    st.sidebar.success(f"Logged in as **testuser**")
    if st.sidebar.button("Logout"):
        del st.session_state['token']
        st.rerun()

# Main Application
if 'token' not in st.session_state:
    st.warning("Please log in to access the application.")
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Create Employee", "View & Search Employees", "Update & Delete Employee", "Department Analytics"]
    )

    # Page 1: Create Employee 
    if page == "Create Employee":
        st.header("Create a New Employee Record")
        with st.form("create_employee_form", clear_on_submit=True):
            employee_id = st.text_input("Employee ID (e.g., E123)")
            name = st.text_input("Full Name")
            department = st.text_input("Department")
            salary = st.number_input("Salary", min_value=0.0, format="%.2f")
            joining_date = st.date_input("Joining Date", value=datetime.now().date())
            skills = st.text_input("Skills (comma-separated)", "Python, FastAPI")

            submitted = st.form_submit_button("Add Employee")
            if submitted:
                skills_list = [skill.strip() for skill in skills.split(',')]
                employee_data = {
                    "employee_id": employee_id, "name": name, "department": department,
                    "salary": salary, "joining_date": joining_date.isoformat(), "skills": skills_list
                }
                headers = get_auth_headers()
                response = requests.post(f"{API_BASE_URL}/employees/", json=employee_data, headers=headers)
                if response.status_code == 201:
                    st.success("Employee created successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

    # Page 2: View & Search Employees 
    elif page == "View & Search Employees":
        st.header("View and Search Employee Records")

        # Search by Skill
        with st.expander("Search by Skill"):
            skill_search = st.text_input("Enter a skill to search for")
            if st.button("Search Skill"):
                response = requests.get(f"{API_BASE_URL}/employees/search/?skill={skill_search}")
                if response.status_code == 200:
                    st.dataframe(pd.DataFrame(response.json()))
                else:
                    st.error("Could not fetch data.")

        st.divider()

        # List all employees with filters and pagination
        st.subheader("All Employees")
        department_filter = st.text_input("Filter by Department (optional)")

        if 'page_num' not in st.session_state:
            st.session_state.page_num = 0

        limit = 10
        skip = st.session_state.page_num * limit

        params = {"skip": skip, "limit": limit}
        if department_filter:
            params["department"] = department_filter

        response = requests.get(f"{API_BASE_URL}/employees/", params=params)
        if response.status_code == 200:
            employees = response.json()
            if employees:
                df = pd.DataFrame(employees)
                st.dataframe(df)
            else:
                st.info("No more employees to display.")

            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ Previous Page"):
                        st.session_state.page_num -= 1
                        st.rerun()
            with col2:
                if len(employees) == limit:
                    if st.button("Next Page"):
                        st.session_state.page_num += 1
                        st.rerun()
        else:
            st.error("Could not fetch employee list.")


    # Page 3: Update & Delete Employee
    elif page == "Update & Delete Employee":
        st.header("Update or Delete an Employee")
        employee_id_to_manage = st.text_input("Enter Employee ID to manage")

        if employee_id_to_manage:
            response = requests.get(f"{API_BASE_URL}/employees/{employee_id_to_manage}")
            if response.status_code == 200:
                employee_data = response.json()
                st.success(f"Loaded data for {employee_data['name']}")

                with st.form("update_employee_form"):
                    name = st.text_input("Full Name", value=employee_data['name'])
                    department = st.text_input("Department", value=employee_data['department'])
                    salary = st.number_input("Salary", min_value=0.0, value=float(employee_data['salary']), format="%.2f")
                    joining_date = st.date_input("Joining Date", value=datetime.fromisoformat(employee_data['joining_date']).date())
                    skills = st.text_input("Skills (comma-separated)", value=", ".join(employee_data['skills']))
                    
                    submitted = st.form_submit_button("Update Employee")
                    if submitted:
                        skills_list = [skill.strip() for skill in skills.split(',')]
                        update_data = {
                            "name": name, "department": department, "salary": salary,
                            "joining_date": joining_date.isoformat(), "skills": skills_list
                        }
                        headers = get_auth_headers()
                        response = requests.put(f"{API_BASE_URL}/employees/{employee_id_to_manage}", json=update_data, headers=headers)
                        if response.status_code == 200:
                            st.success("Employee updated successfully!")
                            st.json(response.json())
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                
                st.divider()
                st.subheader("Delete Employee")
                if st.checkbox(f"I confirm I want to delete employee {employee_id_to_manage}"):
                    if st.button("DELETE EMPLOYEE RECORD", type="primary"):
                        headers = get_auth_headers()
                        response = requests.delete(f"{API_BASE_URL}/employees/{employee_id_to_manage}", headers=headers)
                        if response.status_code == 200:
                            st.success("Employee deleted successfully.")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")

            else:
                st.error("Employee not found.")


    #  Page 4: Get Employees Avg Salary by Department
    elif page == "Department Analytics":
        st.header("Department Analytics")
        if st.button("Generate Report"):
            response = requests.get(f"{API_BASE_URL}/employees/avg-salary/by-department")
            if response.status_code == 200 and response.json():
                data = response.json()
                st.success("Report generated!")
                
                df = pd.DataFrame(data)
                df = df.set_index("department")

                st.subheader("Average Salary by Department")
                st.dataframe(df)

                st.subheader("Salary Comparison Chart")
                st.bar_chart(df['avg_salary'])
            else:
                st.warning("No data available to generate a report.")
