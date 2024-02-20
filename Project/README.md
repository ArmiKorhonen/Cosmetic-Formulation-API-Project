# Cosmetic Formulation API Project

## Installation

### Prerequisites

Project was created using Python 3.12.1, Flask 3.0.2 and SQLite 3.43.1.

### Dependencies

```bash
pip install -r requirements.txt
```

### Database creation and populating it with ingredients

Create the database and the database tables:

```bash
from db_setup import db,app
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()
exit()
```

Populate the database with some ingredients:

```bash
python populate_ingredients.py
```

You can query the ingredients table to see that the information is there:

```bash
python query_ingredients.py
```