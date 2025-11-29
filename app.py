from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

DB_CONFIG = {
    "host": "localhost",
    "user": "murulihp",
    "password": "4709",
    "database": "portfolio_cms"
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}


@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sections WHERE name = 'about'")
    about = cursor.fetchone()

    cursor.execute("SELECT * FROM skills ORDER BY level DESC, name ASC")
    skills = cursor.fetchall()

    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", about=about, skills=skills, projects=projects)


@app.route("/project/<int:project_id>")
def project_detail(project_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.close()
    conn.close()
    if not project:
        return redirect(url_for("home"))
    return render_template("project_detail.html", project=project)


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name").strip()
    email = request.form.get("email").strip()
    message = request.form.get("message").strip()

    if name and email and message:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (name, email, message, created_at) VALUES (%s, %s, %s, %s)",
            (name, email, message, datetime.now()),
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for("home"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if "admin_id" in session:
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin and check_password_hash(admin["password"], password):
            session["admin_id"] = admin["id"]
            session["admin_name"] = admin["name"]
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid email or password"

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS count FROM projects")
    project_count = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM skills")
    skill_count = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM messages")
    message_count = cursor.fetchone()["count"]

    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC LIMIT 5")
    recent_messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        project_count=project_count,
        skill_count=skill_count,
        message_count=message_count,
        recent_messages=recent_messages,
        admin_name=session.get("admin_name"),
    )


@app.route("/admin/about", methods=["GET", "POST"])
def admin_about():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        content = request.form.get("content")
        cursor.execute("SELECT * FROM sections WHERE name = 'about'")
        about = cursor.fetchone()
        if about:
            cursor.execute(
                "UPDATE sections SET content=%s WHERE name='about'",
                (content,),
            )
        else:
            cursor.execute(
                "INSERT INTO sections (name, content) VALUES ('about', %s)",
                (content,),
            )
        conn.commit()

    cursor.execute("SELECT * FROM sections WHERE name = 'about'")
    about = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("admin_about.html", about=about, admin_name=session.get("admin_name"))


@app.route("/admin/projects", methods=["GET", "POST"])
def admin_projects():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        title = request.form.get("title").strip()
        short_desc = request.form.get("short_desc").strip()
        description = request.form.get("description").strip()
        tech_stack = request.form.get("tech_stack").strip()
        github_link = request.form.get("github_link").strip()
        live_link = request.form.get("live_link").strip()

        if title and short_desc:
            cursor.execute(
                "INSERT INTO projects (title, short_desc, description, tech_stack, github_link, live_link, created_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (title, short_desc, description, tech_stack, github_link, live_link, datetime.now()),
            )
            conn.commit()

    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_projects.html", projects=projects, admin_name=session.get("admin_name"))


@app.route("/admin/projects/delete/<int:project_id>", methods=["POST"])
def admin_delete_project(project_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id=%s", (project_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("admin_projects"))


@app.route("/admin/skills", methods=["GET", "POST"])
def admin_skills():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form.get("name").strip()
        level = request.form.get("level")
        if name and level:
            cursor.execute(
                "INSERT INTO skills (name, level) VALUES (%s, %s)",
                (name, int(level)),
            )
            conn.commit()

    cursor.execute("SELECT * FROM skills ORDER BY level DESC, name ASC")
    skills = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_skills.html", skills=skills, admin_name=session.get("admin_name"))


@app.route("/admin/skills/delete/<int:skill_id>", methods=["POST"])
def admin_delete_skill(skill_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skills WHERE id=%s", (skill_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("admin_skills"))


@app.route("/admin/messages")
def admin_messages():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin_messages.html", messages=messages, admin_name=session.get("admin_name"))


if __name__ == "__main__":
    app.run(debug=True)
