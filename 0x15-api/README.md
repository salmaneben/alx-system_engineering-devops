# 0x15. API

![API](https://img.shields.io/badge/API-REST-blue)
![Python](https://img.shields.io/badge/Python-Requests-green)
![JSON](https://img.shields.io/badge/Format-JSON%2FCSV-orange)

## 📋 Description

This project focuses on working with REST APIs, data collection, and export functionality. You'll practice making HTTP requests, parsing JSON responses, and exporting data to different formats (CSV and JSON). The project uses the JSONPlaceholder REST API for practical exercises.

**Email**: Messsagelordwill@gmail.com

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is a REST API and how it works
- How to make HTTP requests in Python
- How to parse JSON data
- How to export data to CSV and JSON formats
- Best practices for API consumption
- Error handling in API requests
- Data validation and processing

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-gather_data_from_an_API.py` | Python script that returns information about an employee's to-do list progress |
| `1-export_to_CSV.py` | Python script that exports an employee's to-do list information to CSV format |
| `2-export_to_JSON.py` | Python script that exports an employee's to-do list information to JSON format |
| `3-dictionary_of_list_of_dictionaries.py` | Python script that exports all employees' to-do list data to JSON format |

## 🚀 Usage

### Prerequisites
```bash
# Install required packages
pip3 install requests
```

### Running Scripts

```bash
# Display employee TODO progress
python3 0-gather_data_from_an_API.py <employee_id>

# Export to CSV
python3 1-export_to_CSV.py <employee_id>

# Export to JSON
python3 2-export_to_JSON.py <employee_id>

# Export all employees to JSON
python3 3-dictionary_of_list_of_dictionaries.py
```

### Examples

```bash
# Get employee 1's progress
python3 0-gather_data_from_an_API.py 1
# Output: Employee Leanne Graham is done with tasks(5/20):

# Export employee 2's data to CSV
python3 1-export_to_CSV.py 2
# Creates: 2.csv

# Export employee 3's data to JSON
python3 2-export_to_JSON.py 3
# Creates: 3.json

# Export all employees
python3 3-dictionary_of_list_of_dictionaries.py
# Creates: todo_all_employees.json
```

## 🌐 API Reference

### JSONPlaceholder API
Base URL: `https://jsonplaceholder.typicode.com/`

#### Endpoints Used
- **Users**: `/users` - Get all users or specific user
- **Todos**: `/todos` - Get all todos or filter by user

#### Example Responses

**User Data**:
```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz"
}
```

**Todo Data**:
```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

## 🔧 Implementation Details

### Data Gathering (Task 0)
- Fetches user information by ID
- Retrieves all todos for the user
- Calculates completion statistics
- Displays progress in specified format

**Output Format**:
```
Employee <employee_name> is done with tasks(<completed_tasks>/<total_tasks>):
     <task_title>
     <task_title>
     ...
```

### CSV Export (Task 1)
- Exports user's todo data to CSV format
- Filename: `<user_id>.csv`
- Format: `"<user_id>","<username>","<task_completion_status>","<task_title>"`

**CSV Example**:
```csv
"1","Bret","True","delectus aut autem"
"1","Bret","False","quis ut nam facilis"
```

### JSON Export (Task 2)
- Exports user's todo data to JSON format
- Filename: `<user_id>.json`
- Structured as nested JSON object

**JSON Example**:
```json
{
  "1": [
    {
      "task": "delectus aut autem",
      "completed": true,
      "username": "Bret"
    }
  ]
}
```

### All Employees Export (Task 3)
- Exports all users' todo data
- Filename: `todo_all_employees.json`
- Dictionary with user IDs as keys

## 📊 Code Structure

### Basic API Request Pattern
```python
import requests
import json

def get_user_data(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_user_todos(user_id):
    url = f"https://jsonplaceholder.typicode.com/todos"
    params = {"userId": user_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return []
```

### CSV Export Pattern
```python
import csv

def export_to_csv(user_id, username, todos):
    filename = f"{user_id}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for todo in todos:
            writer.writerow([
                user_id,
                username,
                todo['completed'],
                todo['title']
            ])
```

### JSON Export Pattern
```python
import json

def export_to_json(user_id, username, todos):
    filename = f"{user_id}.json"
    data = {
        str(user_id): [
            {
                "task": todo['title'],
                "completed": todo['completed'],
                "username": username
            }
            for todo in todos
        ]
    }
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile)
```

## 🛡️ Error Handling

### Best Practices
```python
try:
    response = requests.get(url)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
```

### Status Code Handling
```python
if response.status_code == 200:
    # Success
    return response.json()
elif response.status_code == 404:
    # Not found
    print("Resource not found")
else:
    # Other errors
    print(f"HTTP {response.status_code}: {response.text}")
```

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- Python 3.8.x
- Must use `requests` module for HTTP requests
- Must handle JSON data properly
- CSV files must be properly quoted
- JSON files must be valid JSON format
- Scripts must be executable
- Must follow PEP 8 style guidelines

## 🎓 Resources

- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)
- [Python Requests Documentation](https://requests.readthedocs.io/)
- [JSON in Python](https://docs.python.org/3/library/json.html)
- [CSV in Python](https://docs.python.org/3/library/csv.html)
- [REST API Best Practices](https://restfulapi.net/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)
- Email: Messsagelordwill@gmail.com

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
