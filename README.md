# CSV to JSON Converter with Age Group Analysis

This is a Django-based web application where you can upload a CSV file, and it will process the file, extract the user data, store it in the database, and also generate an **Age Group Distribution Report**.  
It can also handle nested CSV keys like `name.firstName` or `address.city` by flattening them, and even store extra info in JSON format.

---

## Features

- Upload a CSV file from Postman or any API client.
- Extracts specific fields like Name, Age, Address.
- Handles nested column names from CSV.
- Stores extra/unknown columns in `additional_info`.
- Calculates Age Group percentage report:
  - `<20`
  - `20-40`
  - `40-60`
  - `>60`
- Saves everything into the database.
- Admin Panel view with charts (pie/bar) for age groups.

---

## Project Structure

```bash
  project_name/
  │
  ├── app_name/
  │ ├── migrations/
  │ ├── init.py
  │ ├── admin.py
  │ ├── models.py
  │ ├── serializers.py
  │ ├── utils.py
  │ ├── views.py
  │ └── urls.py
  │
  ├── project_name/
  │ ├── init.py
  │ ├── settings.py
  │ ├── urls.py
  │ └── wsgi.py
  │
  └── manage.py
  ```

---

## Requirements

Make sure Python and pip are installed.  
Install the required packages using:

```bash
pip install django djangorestframework django-admincharts
```

## How to Run
Clone the repo
```bash
git clone <repo_url>
cd <repo_folder>
```

Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser
```bash
python manage.py createsuperuser
```

Run the server
```bash
python manage.py runserver
```

Login to Admin
```bash
Go to: http://127.0.0.1:8000/admin
```

## API Endpoints (Postman)
1. Upload CSV & Get Report

    POST /upload-csv/

    Body (form-data):
    
    file → Select .csv file
    
    Response Example:
    ```bash
    
    {
      "message": "CSV processed successfully!",
      "age_distribution": {
        "<20": "20.00%",
        "20-40": "40.00%",
        "40-60": "20.00%",
        ">60": "20.00%"
      }
    }
    ```

3. Get All Users

   GET /users/

   Returns a list of all saved users in JSON format.

## Admin Charts

Using django-admincharts, the age group data is shown in Pie or Bar chart format in Admin, on endpoint:
```bash
   admin/
```



