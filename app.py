from flask import Flask, render_template, request
import requests

app_key = "5803d23bd3962e2f394ab3081bbf235a	"
app_id = "efc3f977"
api_base_url = "https://api.edamam.com/search"
error_statement = "You should enter at least two ingredient so that we will have something to work with."
no_results_statement = "We got no results that matches your search. We recommend either to check your spelling or to try some different ingredients."


app = Flask(__name__)
app.config['SECRET_KEY'] = '08642_fridge_to_table_13579'

ings = []
alls = []

max_number_of_ingredients = 50


def get_list_as_string(list_name):
    separator = ', '
    string = separator.join(list_name)
    return string


@app.route('/')
def forms():
    ings.clear()
    del ings[:]
    alls.clear()
    del alls[:]
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    ingredients = request.form.get("ingredients")
    if ingredients != "" and len(ings) < max_number_of_ingredients:
        ings.append(ingredients)
    allergies = request.form.get("allergies")
    if allergies != "" and len(ings) < max_number_of_ingredients:
        alls.append(allergies)

    ings_str = get_list_as_string(ings)
    alls_str = get_list_as_string(alls)
    return render_template('index.html', ings=ings_str, alls=alls_str)


@app.route('/delete/ing', methods=['GET', 'POST'])
def delete_ings():
    if len(ings) > 0:
        del ings[-1]
    ings_str = get_list_as_string(ings)
    alls_str = get_list_as_string(alls)
    return render_template('index.html', ings=ings_str, alls=alls_str)


@app.route('/delete/all', methods=['GET', 'POST'])
def delete_alls():
    if len(alls) > 0:
        del alls[-1]
    ings_str = get_list_as_string(ings)
    alls_str = get_list_as_string(alls)
    return render_template('index.html', ings=ings_str, alls=alls_str)


@app.route('/data/results', methods=['GET', 'POST'])
def result():
    if len(ings) < 2:
        ings_str = get_list_as_string(ings)
        alls_str = get_list_as_string(alls)
        return render_template("error.html", error_statement=error_statement, alls=alls_str, ings=ings_str)
    else:
        Returned = request.form.get("Returned")
        if Returned == "1" or Returned == 1:
            max_number_of_ingredients = len(ings)
        else:  # Returned == "None" or Returned is None:
            max_number_of_ingredients = 50
        if len(alls) == 0:
            endpoint_path = f"q={ings}&ingr={max_number_of_ingredients}"
        else:
            allergies_for_endpoint = '&excluded='.join(alls)
            endpoint_path = f"q={ings}&excluded={allergies_for_endpoint}&ingr={max_number_of_ingredients}"
        endpoint = f"{api_base_url}?app_key={app_key}&app_id={app_id}&{endpoint_path}&to=24"
        r = requests.get(endpoint)
        recipes = r.json()['hits']
        if len(recipes) == 0:
            ings_str = get_list_as_string(ings)
            alls_str = get_list_as_string(alls)
            return render_template('error.html', no_results_statement=no_results_statement, alls=alls_str, ings=ings_str)
        else:
            return render_template('results.html', recipes=recipes, i=endpoint)


if __name__ == '__main__':
    app.run()