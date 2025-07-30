from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "King" 


contacts = []

def search_contacts(keyword):
    keyword = keyword.lower()
    return [c for c in contacts if keyword in c["name"].lower() or keyword in c["phone"]]


@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("search", "")
    filtered = search_contacts(query) if query else contacts
    return render_template("index.html", contacts=filtered, search=query)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    phone = request.form["phone"].strip()
    email = request.form["email"].strip()
    address = request.form["address"].strip()

    if not name or not phone:
        flash("Name and Phone Number are required!")
        return redirect(url_for("index"))

    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    flash("Contact added successfully!")
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(contacts):
        del contacts[index]
        flash("Contact deleted!")
    else:
        flash("Invalid contact selected!")
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        email = request.form["email"].strip()
        address = request.form["address"].strip()
        if not name or not phone:
            flash("Name and Phone Number are required!")
            return redirect(url_for("edit", index=index))
        if 0 <= index < len(contacts):
            contacts[index] = {"name": name, "phone": phone, "email": email, "address": address}
            flash("Contact updated!")
        return redirect(url_for("index"))
    else:
        if 0 <= index < len(contacts):
            return render_template("edit.html", contact=contacts[index], index=index)
        flash("Invalid contact.")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
