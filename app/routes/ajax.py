import json

from flask import jsonify, request

from util import application, db_path, delete_image_file, get_image_from_db, get_section_by_id, update_db_file


@application.route('/submitCuration/<string:section_id>/', methods=['POST'])
def submit_curation(section_id):
    db = json.loads(open(db_path, 'r').read())

    images_str = request.form.get('images')
    images = json.loads(images_str)

    for image in images:
        db_image = get_image_from_db(db, section_id, image["id"])
        if db_image != image:
            db_image["top"] = image["top"]
            db_image["left"] = image["left"]
            db_image["width"] = image["width"]

    update_db_file(db_path, db)

    return jsonify({'success': True})


@application.route('/delete_image/', methods=['POST'])
def delete_image():
    section_id = request.form.get('section_id')
    image_id = int(request.form.get('image_id'))

    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    filename = image['url']

    section['images'].remove(image)
    delete_image_file(filename)

    update_db_file(db_path, db)

    return jsonify({'success': True})


@application.route('/cv')
def cv():
    return application.send_static_file('pdf/CV.pdf')


@application.route('/shift_section_position', methods=['POST'])
def shift_section_position():
    db = json.loads(open(db_path, 'r').read())

    section_id = request.form.get('section_id')
    shift = int(request.form.get('shift'))

    section = get_section_by_id(db, section_id)
    section_index = db.index(section)

    if section_index == 0 and shift < 0:  # can't shift up if at top
        return jsonify({'success': False})
    if section_index == len(db) - 1 and shift > 0:  # Can't shift down if at bottom
        return jsonify({'success': False})

    db[section_index], db[section_index + shift] = db[section_index + shift], db[section_index]

    with open(db_path, 'w') as db_write:
        db_write.write(json.dumps(db))

    return jsonify({'success': True})


@application.route('/shift_image_position', methods=['POST'])
def shift_image_position():
    section_id = request.form.get('section_id')
    image_id = int(request.form.get('image_id'))
    shift = int(request.form.get('shift'))

    db = json.loads(open(db_path, 'r').read())

    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    image_index = section['images'].index(image)

    if image_index == 0 and shift < 0:  # can't shift up if at top
        return jsonify({'success': False})
    if image_index == len(section['images']) - 1 and shift > 0:  # Can't shift down if at bottom
        return jsonify({'success': False})

    # swap sections
    tmp = section['images'][image_index]
    section['images'][image_index] = section['images'][image_index + shift]
    section['images'][image_index + shift] = tmp

    update_db_file(db_path, db)

    return jsonify({'success': True})