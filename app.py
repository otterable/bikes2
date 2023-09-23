import os
from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches


app = Flask(__name__, static_url_path='/static')


# Sample list of items to search from
items = [
"Schutzbleche/Fenders | blatníky set MAX1 Ventura 24\"-28\"",
"Bremsbelag/Bremsklotz (direkter Pin) | brzdová botka dřík MAX1 60mm",
"Bremsbelag/Bremsklotz (mit Gewinde) | brzdová botka závit MAX1 60 mm",
"Bremshebel/Bremsschalter | brzdové páky MAX1 \"V\" Alu",
"Reifen/Pneu | plášť CHAOYANG 26x2,10 (559-52) H-5152 27 tpi černý",
"Reifen/Pneu | plášť KENDA 24x1,5 (507-40) (K-184) černý",
"Reifen/Pneu | plášť KENDA 26x1,95 (559-50) (K-831) černý",
"Reifen/Pneu | plášť KENDA 26x1,95 (559-50) (K-892) černý",
"Reifen/Pneu | plášť KENDA 700x32C (622-32) (K-125) černý",
"Schutzbleche/Fenders | KELLYS Blatníky KLS STORM",
"Kettenreiniger/Kettenputzmittel | KELLYS Čistič řetězu KLS CRYSTAL",
"Fahrradreiniger/Radreinigungsmittel | KELLYS Čistící prostředek KLS BIKE CLEANER náhradní náplň 1000 ml",
"Flaschenhalter/Getränkehalter | Košík na fľašu KLASIK čierny",
"Pedale/Trittflächen | Pedály Extend MTB-825A plastic",
"Sattel/Fahrradsitz | Sedlo SMP MTB 6370 čierne",
"Speichenreflektor/Radreflektor | odrazka do výpletu malá",
"Vorderreflektor/Frontreflektor | odrazka přední s držákem malá \"V\"",
"Rückreflektor/Heckreflektor | odrazka zadní s držákem malá \"V\"",
"Öl/Schmieröl | olej WD-40 400ml",
"Ständer/Fahrradständer | stojánek MAX1 středový stavitelný s podložkou 20-29\" černý",
"Bremsenreiniger/Bremsputzmittel | čistič brzd MAX1 Brake Cleaner 400 ml",
"Fahrradschlauch/Innerreifen | FISCHER Fahrradschlauch mittel in 26 Zoll | ETRO-Norm: 37/57-559 | Auto Ventil",
"Rückleuchte/Hecklampe | Walfort Fahrradrückleuchte",
"Scheinwerfer/Frontlampe | Walfort Fahrrad-Scheinwerfer",
"Beleuchtungsset/Lichtset | Walfort Fahrradbeleuchtungsset",
"Klingel/Fahrradglocke (klein) | Kleine Fahrradklingel",
"Klingel/Fahrradglocke (groß) | Große Fahrradklingel",
"Sattel/Fahrradsitz (komfortabel) | Fahrradsitz, weich und angenehm",
"Sattel/Fahrradsitz (einfach) | Fahrradsitz, einfach",
"Fahrradschlauch/Innerreifen | Walfort Fahrradschlauch 28 x 1 5/8 x 1 3/8 ETRTO: 30-622 // 700 x 35/43c"
]


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    matches = get_close_matches(query, items, n=5, cutoff=0.6)  # Change n=5 to however many results you want to return.
    return jsonify(matches)

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


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join('files', uploaded_file.filename)
            uploaded_file.save(file_path)
            return jsonify(success=True)
    return jsonify(success=False)

@app.route('/galerie')
def bike_galerie():
    return render_template('galerie.html')

@app.route('/ankauf')
def bike_ankauf():
    return render_template('ankauf.html')

@app.route('/success')
def bike_success():
    return render_template('success.html')

@app.route('/reparatur')
def bike_reparatur():
    return render_template('reparatur.html')


if __name__ == '__main__':
    app.run(debug=True)
