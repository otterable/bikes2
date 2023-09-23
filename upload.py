from flask import Flask, render_template, send_from_directory, request
import os

app = Flask(__name__, static_url_path='/static')

def get_art_categories():
    art_categories = []
    art_path = os.path.join(app.static_folder, 'art')
    for folder in os.listdir(art_path):
        if os.path.isdir(os.path.join(art_path, folder)):
            art_categories.append(folder)
    return art_categories

@app.route('/')
def index():
    art_categories = get_art_categories()
    all_images = []

    for category in art_categories:
        category_path = os.path.join(app.static_folder, 'art', category)
        images = [file for file in os.listdir(category_path) if file.lower().endswith(('.jpg', '.png', '.gif'))]
        all_images.extend(images)

    return render_template('index.html', art_categories=art_categories, images=all_images, selected='all')
    
@app.route('/art/all/')
def all_images():
    images = []
    art_categories = get_art_categories()
    
    for category in art_categories:
        category_path = os.path.join(app.static_folder, 'art', category)
        if os.path.exists(category_path) and os.path.isdir(category_path):
            for root, _, filenames in os.walk(category_path):
                for filename in filenames:
                    if filename.lower().endswith(('.jpg', '.png', '.gif')):
                        image_path = os.path.join(root, filename)
                        images.append(image_path.replace(app.static_folder + '/art/', ''))
    
    return render_template('index.html', images=images, art_categories=art_categories)

@app.route('/art/<category>/')
def category_images(category):
    category_path = os.path.join(app.static_folder, 'art', category)
    images = [file for file in os.listdir(category_path) if file.lower().endswith(('.jpg', '.png', '.gif'))]
    return render_template('index.html', art_categories=get_art_categories(), images=images, selected=category)

@app.route('/art/<category>/<filename>')
def view_image(category, filename):
    return send_from_directory(os.path.join('static', 'art', category), filename)
    
@app.route('/price_calculator')
def price_calculator():
    return render_template('index.html', art_categories=get_art_categories(), images=[], selected='all')

if __name__ == '__main__':
    app.run(debug=True)
