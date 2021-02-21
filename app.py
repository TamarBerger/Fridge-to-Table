from flask import Flask, render_template, request
import requests

app_key = "5803d23bd3962e2f394ab3081bbf235a	"
app_id = "efc3f977"
api_base_url = "https://api.edamam.com/search"
error_statement = "You should enter at least two ingredient so that we will have something to work with."
no_results_statement = "We got no results that matches your search. We recommend either to check your spelling or to try some different ingredients."


app = Flask(__name__)
app.config['SECRET_KEY'] = '08642_fridge_to_table_13579'


class InputLists:
    MAX_NUMBER_OF_INGREDIENTS = 50
    MIN_NUMBER_OF_INGREDIENTS = 2

    def __init__(self) -> None:
        self._list = []

    def _initialize_list(self) -> list:
        self._list = []

    def _add_element_to_list(self, string_to_add) -> list:
        if string_to_add != "" and len(self._list) <= self.MAX_NUMBER_OF_INGREDIENTS:
            self._list.append(string_to_add)
        return self._list

    def _delete_last_element(self) -> list:
        if len(self._list) > 0:
            del self._list[-1]
        return self._list


ings_object = InputLists()
alls_object = InputLists()


@app.route('/')
def forms():
    ings = ings_object._initialize_list()
    alls = alls_object._initialize_list()
    return render_template('index.html', ings=ings, alls=alls)


@app.route('/data', methods=['GET', 'POST'])
def data():
    ingredients = request.form.get("ingredients")
    ings = ings_object._add_element_to_list(ingredients)

    allergies = request.form.get("allergies")
    alls = alls_object._add_element_to_list(allergies)

    return render_template('index.html', ings=ings, alls=alls)


@app.route('/delete/ing', methods=['GET', 'POST'])
def delete_ings():
    ings = ings_object._delete_last_element()
    alls = alls_object._list

    return render_template('index.html', ings=ings, alls=alls)


@app.route('/delete/all', methods=['GET', 'POST'])
def delete_alls():
    ings = ings_object._list
    alls = alls_object._delete_last_element()

    return render_template('index.html', ings=ings, alls=alls)


@app.route('/data/results', methods=['GET', 'POST'])
def result():
    ings = ings_object._list
    alls = alls_object._list

    if len(ings) < ings_object.MIN_NUMBER_OF_INGREDIENTS:
        return render_template("error.html", error_statement=error_statement, alls=alls, ings=ings)

    Limited = request.form.get("Limited")
    if Limited:
        max_number_of_ingredients = len(ings)
    else:
        max_number_of_ingredients = ings_object.MAX_NUMBER_OF_INGREDIENTS

    if len(alls) == 0:
        endpoint_path = f"q={ings}&ingr={max_number_of_ingredients}"
    else:
        allergies_to_exclude = '&excluded='.join(alls)
        endpoint_path = f"q={ings}&excluded={allergies_to_exclude}&ingr={max_number_of_ingredients}"

    endpoint = f"{api_base_url}?app_key={app_key}&app_id={app_id}&{endpoint_path}&to=24"
    r = requests.get(endpoint)
    recipes = r.json()['hits']
    if len(recipes) == 0:
        ings = ings_object._initialize_list()
        alls = alls_object._initialize_list()
        return render_template('error.html', no_results_statement=no_results_statement, alls=alls, ings=ings)
    else:
        return render_template('results.html', recipes=recipes, i=endpoint)


if __name__ == '__main__':
    app.run()
