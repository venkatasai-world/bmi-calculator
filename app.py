from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "replace_this_in_prod"

def compute_bmi_metric(weight_kg, height_cm):
    if height_cm == 0:
        return None
    height_m = height_cm / 100.0
    return weight_kg / (height_m * height_m)

def compute_bmi_imperial(weight_lb, height_in):
    if height_in == 0:
        return None
    return 703.0 * weight_lb / (height_in * height_in)

def bmi_category(bmi):
    if bmi is None:
        return ("Invalid", "bad")
    if bmi < 18.5:
        return ("Underweight", "warn")
    elif bmi < 25.0:
        return ("Normal weight", "ok")
    elif bmi < 30.0:
        return ("Overweight", "warn")
    else:
        return ("Obese", "bad")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def bmi():
    units = request.form.get("units", "metric")
    try:
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height"))
    except:
        flash("Please enter valid numeric values for weight and height.")
        return redirect(url_for("index"))

    if units == "metric":
        bmi_val = compute_bmi_metric(weight, height)
        weight_unit = "kg"
    else:
        bmi_val = compute_bmi_imperial(weight, height)
        weight_unit = "lb"

    category, badge_class = bmi_category(bmi_val)

    return render_template(
        "index.html",
        bmi=round(bmi_val, 2) if bmi_val else None,
        category=category,
        badge_class=badge_class,
        units=units,
        weight=weight,
        height=height,
        weight_unit=weight_unit,
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
