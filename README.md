# DVF

## Clone this repository

```bash
git clone https://github.com/strawhattom/DVF && cd DVF
```

## Running project (Linux)


### Creating a virtual environment

```
python venv .venv
```

### Activating venv

```bash
source .venv/bin/activate
```

### Install python dependencies

```bash
pip install -r requirements.txt
```

### Run development version

```bash
export FLASK_APP=App
export FLASK_ENV=development
flask run
```

## Running project (Windows)

### Creating venv

```bash
py -3 -m venv .venv
```

### Activating venv

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run development version

```bash
$env:FLASK_APP = "App"
$env:FLASK_ENV = "developement"
flask run
```
