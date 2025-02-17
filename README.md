# HTTP Endpoint Health Check
A program to check the health of a set of HTTP endpoints given a list of HTTP endpoints in YAML format
## Setup
* Assumes Python 3.5 or later
* Assumes UNIX-like CLI (eg bash, zsh)

### 1. Create virtual environment and install dependencies
    
#### Example from base directory of repository:  

    
    python3 -m venv venv 
    source venv/Scripts/activate
    pip install -r requirements.txt

    
### 2. Run `healthcheck.py` and specify the path to the input YAML file

#### Example from base directory of repository using sample input:

    python3 healthcheck.py input.yaml

#### Example from base directory of repository using generic YAML file for input:

    python3 healthcheck.py <PATH_TO_YAML_FILE>

### 3. To exit the program gracefully, use `CTRL+C`

### 4. To exit the virtual environment, use `deactivate`


