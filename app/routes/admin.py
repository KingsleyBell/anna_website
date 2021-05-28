import json
import os
import re

from flask import jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from auth import requires_auth
from util import about_path, application, contact_path, db_path, delete_image_file, get_section_by_id, update_db_file


@application.route('/admin/', methods=['GET', 'POST'])
@requires_auth
def admin_sections():
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':  # Delete section
        section_id = request.form.get('section_id')

        section = get_section_by_id(db, section_id)
        for image in section['images']:
            delete_image_file(image['url'])
        db.remove(section)

        update_db_file(db_path, db)

        return jsonify({'success': True})
    else:
        return render_template('admin/edit_sections.html', db=db)


@application.route('/new_section/', methods=['GET', 'POST'])
@requires_auth
def new_section():
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        section_name = request.form.get('section')
        section_id = re.sub('[^A-Za-z0-9]+', '_', section_name).lower()

        image_file = request.files.get('file')
        file_extension = image_file.filename.split('.')[-1]
        upload_folder = os.path.join(application.static_folder, 'images/uploads')
        filename = secure_filename(str(section_id) + '.' + file_extension)
        image_file.save(os.path.join(upload_folder, filename))

        section_dict = {
            'name': section_name,
            'id': section_id,
            "image_url": filename,
            'text': '',
            'images': []
        }
        db.append(section_dict)
        update_db_file(db_path, db)

        return redirect(url_for('admin_sections'))
    else:
        return render_template('admin/new_section.html', db=db)


@application.route('/edit_section/<string:section_id>/', methods=['GET', 'POST'])
@requires_auth
def edit_section(section_id):
    db = json.loads(open(db_path, 'r').read())
    section = get_section_by_id(db, section_id)

    if request.method == 'POST':
        section_name = request.form.get('name')
        section_id = re.sub('[^A-Za-z0-9]+', '_', section_name).lower()
        section_text = request.form.get('text')

        image_file = request.files.get('file')
        file_extension = image_file.filename.split('.')[-1]
        upload_folder = os.path.join(application.static_folder, 'images/uploads')
        filename = secure_filename(str(section_id) + '.' + file_extension)
        image_file.save(os.path.join(upload_folder, filename))

        section['name'] = section_name
        section['id'] = section_id
        section['text'] = section_text
        section["image_url"] = filename

        update_db_file(db_path, db)

        return redirect(url_for('admin_sections'))
    else:
        return render_template('admin/edit_section.html', section=section, db=db)


@application.route('/edit_section_images/<string:section_id>/', methods=['GET'])
@requires_auth
def edit_section_images(section_id):
    db = json.loads(open(db_path, 'r').read())
    section = get_section_by_id(db, section_id)

    return render_template('admin/edit_section_images.html', section=section)


@application.route('/edit_image/<string:section_id>/<int:image_id>/', methods=['GET', 'POST'])
@requires_auth
def edit_image(section_id, image_id):
    db = json.loads(open(db_path, 'r').read())
    section = get_section_by_id(db, section_id)
    image = [i for i in section['images'] if i['id'] == image_id][0]

    if request.method == 'POST':
        section_id = request.form.get('section')
        title = request.form.get('title')
        year = request.form.get('year')
        width = request.form.get('width')
        height = request.form.get('height')
        materials = request.form.get('materials')
        container_width = request.form.get('container_width')
        display_width = request.form.get('display_width')
        align = request.form.get('align')

        db_section = [s for s in db if s['id'] == section_id][0]

        if db_section != section:
            db_section['images'].append(image)
            section['images'].remove(image)

        image["title"] = title
        image["year"] = year
        image["width"] = width
        image["height"] = height
        image["materials"] = materials
        image["container_width"] = container_width
        image["display_width"] = display_width
        image["align"] = align

        update_db_file(db_path, db)

        return redirect(url_for('sections'))
    else:
        sections = [{"name": section["name"], "id": section['id']} for section in db]
        return render_template(
            'admin/edit_image.html',
            image=image,
            section=section['id'],
            sections=sections
        )


@application.route('/upload/<string:section_id>/', methods=['GET', 'POST'])
@requires_auth
def upload(section_id):
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        image_ids = []
        for s in db:
            image_ids += [image['id'] for image in s['images']]
        image_id = max(image_ids + [0]) + 1

        section = get_section_by_id(db, section_id)

        title = request.form.get('title')

        if request.files.get('file').content_length != 0:
            image_type = "image"
            image_file = request.files.get('file')
            file_extension = image_file.filename.split('.')[-1]
            upload_folder = os.path.join(application.static_folder, 'images/uploads')
            filename = secure_filename(str(image_id) + '.' + file_extension)
            image_file.save(os.path.join(upload_folder, filename))
        else:
            image_type = "video"
            filename = request.form.get('link')

        image_dict = {
            "id": image_id,
            "url": filename,
            "type": image_type,
            "title": title,
            "width": 25,
            "top": 0,
            "left": 0
          }

        section['images'].append(image_dict)
        update_db_file(db_path, db)

        return redirect(url_for('admin_sections'))
    else:
        sections = {section['name']: section['id'] for section in db}
        return render_template('admin/upload.html', sections=sections, section=section_id)


@application.route('/admin_about/', methods=['GET', 'POST'])
@requires_auth
def admin_about():
    about_json = json.loads(open(about_path, 'r').read())
    if request.method == 'POST':
        about_heading = request.form.get('heading')
        about_txt = request.form.get('text')

        about_json['heading'] = about_heading
        about_json['text'] = about_txt

        update_db_file(about_path, about_json)

        return redirect(url_for('admin_sections'))
    else:
        return render_template('admin/edit_about.html', about=about_json)


@application.route('/admin_contact/', methods=['GET', 'POST'])
@requires_auth
def admin_contact():
    contact_json = json.loads(open(contact_path, 'r').read())
    if request.method == 'POST':
        contact_txt = request.form.get('text')

        contact_json['text'] = contact_txt

        update_db_file(contact_path, contact_json)

        return redirect(url_for('admin_sections'))
    else:
        return render_template('admin/edit_contact.html', contact=contact_json)


@application.route('/new_home_image/', methods=['GET', 'POST'])
@requires_auth
def new_home_image():
    if request.method == 'POST':
        image_file = request.files.get('file')
        upload_folder = os.path.join(application.static_folder, 'images')
        filename = "home.jpg"
        image_file.save(os.path.join(upload_folder, filename))

        return redirect(url_for('admin_sections'))
    else:
        return render_template('admin/upload_file.html', form_label='New Home Image (must be jpg)')
