from flask import Blueprint, render_template, request, redirect, url_for, flash
from webdata import app
from webdata.models import Result
import requests

import base64
import uuid
import os
from PIL import Image
from io import BytesIO

from webdata import db, this_config

main = Blueprint('main', __name__)

def colorize_image(image_data):
    api_key = 'YOUR_DEEPAI_API_KEY'  # Replace with your DeepAI API key
    response = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={'image': image_data},
        headers={'api-key': this_config.API_KEY}
    )
    print(response.json())
    if response.status_code == 200:
        result = response.json()
        output_url = result['output_url']
        return requests.get(output_url).content
    else:
        return None
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/intro')
def intro():
    return render_template('intro.html')

@main.route('/add_photo', methods=['GET', 'POST'])
def add_photo():
    if request.method == 'POST':
        data = None
        file_data = None
        if request.form.get('captured_image_data'):
            data = request.form.get('captured_image_data')
            data = data.split(',')[1]
            import base64
            import uuid
            import os
            from PIL import Image
            from io import BytesIO
            
            
            im = Image.open(BytesIO(base64.b64decode(data)))
            filename = str(uuid.uuid4()) + '.png'
            uncolorized_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            im.save(uncolorized_path)
            
            with open(uncolorized_path, 'rb') as f:
                colorized_image_data = colorize_image(f)
            
            if colorized_image_data:
                filename = str(uuid.uuid4()) + '.png'
                colorized_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(colorized_path, 'wb') as f:
                    f.write(colorized_image_data)
                
                result = Result(source_link=uncolorized_path, result_link=colorized_path)
                db.session.add(result)
                db.session.commit()
                
                return redirect(url_for('main.add_photo_transition', id=result.id))
            
            else :
                flash('Failed to colorize image', 'danger')
                return redirect(url_for('main.add_photo'))
            
            
        if request.files['imported_image_data'].filename != '':
            print('anjay')
            file_data = request.files['imported_image_data']
            import os 
            import uuid
            
            filename = str(uuid.uuid4())+ '.png'
            uncolorized_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_data.save(uncolorized_path)
            
            with open(uncolorized_path, 'rb') as f:
                colorized_image_data = colorize_image(f)
                
            if colorized_image_data:
                filename = str(uuid.uuid4()) + '.png'
                colorized_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(colorized_path, 'wb') as f:
                    f.write(colorized_image_data)
                
                result = Result(source_link=uncolorized_path, result_link=colorized_path)
                db.session.add(result)
                db.session.commit()
                
                return redirect(url_for('main.add_photo_transition', id=result.id))
            else: 
                flash('Failed to colorize image', 'danger')
                return redirect(url_for('main.add_photo'))
            
    return render_template('add_photo.html')

@main.route('/add_photo_transition/<int:id>', methods=['GET', 'POST'])
def add_photo_transition(id):
    results = Result.query.filter_by(id=id).first()
    print(results)
    return render_template('add_photo_transition.html', results=results)

@main.route('/photo_library', methods=['GET', 'POST'])
def photo_library():
    results = Result.query.all()
    total = 9 - len(results)
    return render_template('photo_library.html', results=results, total=total)

@main.route('/photo_details/<int:id>', methods=['GET', 'POST'])
def photo_details(id):
    result = Result.query.filter_by(id=id).first()
    return render_template('photo_details.html', result=result)