from datetime import datetime
import json
import os

from flask import Flask

application = Flask(__name__)


@application.context_processor
def inject_now():
    return {'now': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}


@application.context_processor
def inject_year():
    return {'year': datetime.utcnow().year}


db_path = os.path.join(application.static_folder, 'db/db.json')
about_path = os.path.join(application.static_folder, 'db/about.json')
contact_path = os.path.join(application.static_folder, 'db/contact.json')


def get_section_by_id(db, section_id):
    return [s for s in db if s['id'] == section_id][0]


def update_db_file(db_file_path, new_db):
    with open(db_file_path, 'w') as db_write:
        db_write.write(json.dumps(new_db))


def get_image_from_db(db, section_id, image_id):
    section = get_section_by_id(db, section_id)
    return [i for i in section["images"] if i["id"] == image_id][0]


def delete_image_file(filename):
    upload_folder = os.path.join(application.static_folder, 'images/uploads')
    os.remove(os.path.join(upload_folder, filename))