import json

from flask import render_template

from util import about_path, contact_path, application, db_path, get_section_by_id


@application.route('/')
def home():
    db = json.loads(open(db_path, 'r').read())
    about = json.loads(open(about_path, 'r').read())

    return render_template(
        'index.html',
        about=about,
        db=db,
    )


@application.route("/contact")
def contact():
    contact_json = json.loads(open(contact_path, 'r').read())['text']
    about = json.loads(open(about_path, 'r').read())

    return render_template(
        'contact.html',
        contact=contact_json,
        about=about
    )


@application.route('/x/<string:section_id>/')
def display_section(section_id):
    db = json.loads(open(db_path, 'r').read())
    about = json.loads(open(about_path, 'r').read())
    section = get_section_by_id(db, section_id)

    return render_template(
        'section.html',
        section=section,
        about=about
    )
