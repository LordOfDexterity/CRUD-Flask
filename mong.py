from flask import Flask, request, Response
from database.db import initialize_db
from database.models import Movie

app = Flask(__name__)

# movies = [
#     {
#         "name": "The Shawshank Redemption",
#         "casts": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"],
#         "genres": ["Drama"]
#     },
#     {
#        "name": "The Godfather ",
#        "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
#        "genres": ["Crime", "Drama"]
#     }
# ]


app.config['MONGODB_SETTINGS'] = {
    'host' : 'mongodb://localhost/movie-bag'
}
initialize_db(app)


@app.route('/movies')
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)


@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    movie = Movie(**body).save()
    id = movie.id
    return {'id': str(id)}, 200


@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    body = request.get_json()
    Movie.objects.get(id=id).update(**body)
    return 'kaam kar gaya', 200

@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    Movie.objects.get(id=id).delete()
    return 'delete ho gaya', 200

@app.route('/movies/<id>')
def get_movie(id):
   movies = Movie.objects.get(id=id).to_json()
   return Response(movies, mimetype="application/json", status=200)


if __name__ == '__main__':
    app.run(debug=True)