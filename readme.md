# OpenClassrooms | Python | P9

## Setup

### 1. Clone the project from Github
`git clone https://github.com/0ddbird/OC_Python_P9.git`

### 2. Go to the repo root  
`cd OC_Python_P9/`

### 3. Create a virtual environment  
`python -m venv <name_of_the_venv>`  

### 4. Activate the virtual environment  
`source <name_of_the_venv>/bin/activate`  

### 5. Install the requirements  
`pip install -r requirements.txt`  

### 6. Generate a SECRET_KEY and copy it  
`python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
### 7. Create a .env file
`nano .env`

### 8. Add these 2 lines:
```
SECRET_KEY=<your_generated_key>
DEBUG=True
```
Save and exit.

### 9. Start the server
`python manage.py runserver`

### 10. Navigate to http://127.0.0.1:8000
