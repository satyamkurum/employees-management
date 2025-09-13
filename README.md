# Employee Management API & Dashboard

This is a full-stack web application built with **FastAPI** and
**Streamlit** for managing employee records.
The project includes a secure RESTful API backend and an interactive
web-based user interface.

## Features

### Backend (FastAPI)

-   **Full CRUD Operations**: Create, Read, Update, and Delete employee
    records.
-   **Advanced Querying**: Filter by department, search by skill, and
    sort results.
-   **Database Aggregation**: Calculate average salary per department.
-   **Secure**: Endpoints for modifying data are protected using JWT
    authentication.
-   **Scalable**: Features pagination for listing employees.
-   **Robust**: Uses database-level indexing and schema validation for
    performance and data integrity.

### Frontend (Streamlit)

-   **User Authentication**: Secure login/logout functionality.
-   **Multi-Page Interface**: Separate pages for creating, viewing,
    updating, and analyzing employee data.
-   **Interactive Forms & Tables**: Easy-to-use forms for data entry and
    pandas DataFrames for viewing data.
-   **Data Visualization**: Bar chart to display analytics on average
    salaries.

------------------------------------------------------------------------

##  Tech Stack

-   **Backend**: FastAPI, Uvicorn
-   **Database**: MongoDB (deployed on MongoDB Atlas)
-   **Frontend**: Streamlit
-   **Authentication**: JWT (JSON Web Tokens)
-   **Deployment**: Backend on Render, Frontend on Streamlit Cloud,
    Database on MongoDB Atlas

------------------------------------------------------------------------

##  How to Run Locally

### 1. Clone the repository:

``` bash
git clone https://github.com/satyamkurum/employees-management.git
cd employees-management
```

### 2. Create and activate a virtual environment:

``` bash
python -m venv venv
source venv/Scripts/activate   
```

### 3. Install dependencies:

``` bash
pip install -r requirements.txt
```

### 4. Set up your local environment file:

Create a file named `.env` in the root directory and add the following
variables:

``` bash
MONGO_DETAILS="your-mongodb-connection-string"
```

### 5. Run the Backend Server:

``` bash
uvicorn app.main:app --reload
```

### 6. Run the Frontend UI (in a second terminal):

``` bash
streamlit run ui.py
```

## Live Deployed Application

 To make this project interactive, the entire full stack application has been deployed to the cloud. You can test the live version without needing to set up a local environment.

### Access Links

 Live User Interface (Streamlit): [Your-Streamlit-Cloud-or-Hugging-Face-URL]

 Live API Documentation (FastAPI): [Your-Render-Backend-URL]/docs

### Login Credentials

 Username: testuser
 Password: testpassword

### Architecture

 Frontend (UI): Hosted on Streamlit Community Cloud

 Backend (API): Hosted on Render

 Database: Hosted on MongoDB Atlas
