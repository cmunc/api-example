## Running a local server instance
### Step 1: Clone the repository
Clone the main branch of the repository and change to project directory:
```bash
git clone https://github.com/cmunc/api-example.git
cd api-example
```

### Step 2: Setup virtual environment
Activate virtual environment, then install all dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Start the API server
Start the flask API server on port 8082
```bash
flask run --host=0.0.0.0 --port 8082
```
