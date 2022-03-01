from APP import app
from datetime import timedelta
from flask import flash, session, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required
from .forms import AdminLoginForm, NewAdminForm, UserPostsForm, check_errors
from .models import AdminTable, Posts, db_add_and_commit
from werkzeug.security import generate_password_hash


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route('/complaints', methods=["GET", "POST"])
def make_posts_page():
    form = UserPostsForm()
    if form.validate_on_submit():
        # initialising new post
        post = Posts(category=form.post_category.data, content=form.text.data, reply_email=form.email.data)

        # user-defined function: adds the new post to the session and commits the change to the database
        db_add_and_commit(post)

        # flash message telling the user about the success of his/her post operation
        flash(f'The {form.post_category.data} has been uploaded, your {form.post_category.data} would be looked into '
              f'shortly. You would receive a mail via the email you provided regarding the status of your complaint.')
        return redirect(url_for("make_posts_page"))

    # user-defined function: checking for errors in the form
    check_errors(form=form)
    return render_template("C_and_S.html", form=form)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login_page():
    form = AdminLoginForm()

    if form.validate_on_submit():
        # querying the db using the username sent from the login form
        attempted_user = AdminTable.query.filter_by(username=form.username.data.lower()).first()

        # validating user and password using a user-defined function "check_password()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):

            # logging in user
            login_user(attempted_user)
            flash(f'You are logged in as {attempted_user.username}', category="success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("invalid credentials", category="danger")
    return render_template("login.html", form=form)


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    no_of_complaints = Posts.query.filter_by(post_category="Complaints").count()
    no_of_suggestions = Posts.query.filter_by(post_category="Suggestions").count()
    return render_template("dashboard.html", no_of_complaints=no_of_complaints, no_of_suggestions=no_of_suggestions)


@app.route("/admin/new-admin", methods=["GET", "POST"])
@login_required
def add_new_admin_page():
    # creating form to be rendered on the the "/admin/new-admin" route
    form = NewAdminForm()
    if form.validate_on_submit():

        new_admin = AdminTable(fname=form.name.data, sname=form.surname.data, username=form.username.data.lower(),
                               email_add=form.email.data,
                               password=generate_password_hash(form.password.data, method="sha512"))

        # adding new admin into the admin table  and commiting to database
        db_add_and_commit(new_admin)
        flash(f'new user {new_admin.username} created successfully')
        return redirect(url_for("add_new_admin_page"))

    # user-defined function: checking for errors in the form
    check_errors(form=form)
    return render_template("add-admin.html", form=form)


@app.route("/admin/view-report")
@login_required
def view_reports_page():
    posts = Posts.query.order_by(Posts.date_created.desc()).all()
    return render_template("view-reports.html", posts=posts)


@app.route("/admin/generate-report")
@login_required
def download_report():
    pass


@app.route("/admin/delete-post")
@login_required
def remove_post():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin_login_page"))


@app.before_request
def before_request():
    # sets session time from login to 1 hr
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)
