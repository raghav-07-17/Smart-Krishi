
from pathlib import Path
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(app.instance_path) / "krishi.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    schema = (BASE_DIR / "schema.sql").read_text(encoding="utf-8")
    with get_db() as connection:
        connection.executescript(schema)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            area = float(request.form["area_acres"])
            if not 0 < area <= 10000:
                raise ValueError("Invalid area")

            field_type = request.form["field_type"]
            growth_stage = request.form["growth_stage"]
            symptoms = request.form.getlist("symptoms")

            if field_type not in ("wetland", "dryland"):
                raise ValueError("Select a valid field type")

            if not growth_stage or not symptoms:
                raise ValueError("Complete all required fields")

            with get_db() as connection:
                cursor = connection.execute(
                    """INSERT INTO farm_records
                    (area_acres, field_type, growth_stage)
                    VALUES (?, ?, ?)""",
                    (area, field_type, growth_stage)
                )

                farm_id = cursor.lastrowid

                connection.execute(
                    """INSERT INTO diagnosis_sessions
                    (farm_id, symptoms)
                    VALUES (?, ?)""",
                    (farm_id, ", ".join(symptoms))
                )

            flash("Field details saved successfully.", "success")
            return redirect(url_for("home"))

        except (ValueError, KeyError):
            flash("Please enter valid field details.", "error")

    with get_db() as connection:
        records = connection.execute(
            """SELECT f.*, d.symptoms
            FROM farm_records f
            LEFT JOIN diagnosis_sessions d ON d.farm_id = f.id
            ORDER BY f.id DESC LIMIT 10"""
        ).fetchall()

    return render_template("index.html", records=records)


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    error = None

    if request.method == "POST":
        try:
            acres = float(request.form["acres"])
            rate = float(request.form["rate"])
            pack_size = float(request.form["pack_size"])
            pack_price = float(request.form["pack_price"])

            if not (
                0 < acres <= 10000
                and rate >= 0
                and 0 < pack_size <= 100000
                and 0 <= pack_price <= 100000000
            ):
                raise ValueError("Invalid values")

            quantity = acres * rate
            packs = int((quantity / pack_size) + 0.999999999)
            total_cost = packs * pack_price

            result = {
                "quantity": round(quantity, 2),
                "packs": packs,
                "total_cost": round(total_cost, 2)
            }

        except (ValueError, KeyError):
            error = "Please enter valid numbers."

    return render_template(
        "calculator.html", result=result, error=error
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)