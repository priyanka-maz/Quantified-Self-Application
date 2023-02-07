Quantified Self-App

Quantified Self-App is a web application that tracks life parameters, logs into each tracker and plots 
trendlines on the basis of the logs. It also emails reports to user.

# Setup using Python virtual environment
After downloading the codebase src/ dir to /path/to/src
```
python3 -m venv /path/to/src
cd /path/to/src
python3 -m pip install -r requirements.txt
# Skip below command if using in a development env
export ENV=production
python3 main.py
```

# Setup on replit.com
After importing the codebase src/ dir into your repl,
```
poetry init
poetry install
# Skip below command if using in a development env
export ENV=production
python main.py
```
