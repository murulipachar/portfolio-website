# Personal Portfolio CMS

A personal portfolio website with a simple CMS-style admin panel, built with **Flask**, **MySQL**, **Bootstrap**, and basic CSS.

## Features

- Public portfolio site:
  - About section
  - Skills list
  - Projects listing & project detail page
  - Contact form (messages saved in DB)
- Admin panel:
  - Admin login/logout
  - Edit About section
  - Add/Delete skills
  - Add/Delete projects
  - View contact messages
  - Dashboard with quick counts

## Tech Stack

- Backend: Python, Flask
- Database: MySQL
- Frontend: HTML, Bootstrap, custom CSS

## Default Admin Login

After running the SQL schema, a default admin is created:

- Email: `admin@example.com`
- Password: `admin123` (you should change this in production)

## Setup Instructions

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create the MySQL database and tables:

- Open MySQL and run:

```sql
SOURCE schema.sql;
```

3. Update DB credentials if needed in `app.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "murulihp",
    "password": "4709",
    "database": "portfolio_cms"
}
```

4. Run the app:

```bash
python app.py
```

5. Open in browser:

- Public site: `http://127.0.0.1:5000/`
- Admin login: `http://127.0.0.1:5000/admin/login`

Login with the default admin credentials above, then:

- Edit About content
- Add skills & projects
- Check messages
