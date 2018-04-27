from flask import Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import AStar as solver
import graph as drawer
import _thread

app = Flask(__name__, template_folder=".")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDgYW0EwKsjVRVA2-XlA56Xbv8UijALFdk";

GoogleMaps(app)

@app.route("/")
def mapView():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    );
    return render_template('map.html', mymap=mymap);

@app.route("/search-route", methods=['POST'])
def searchRoute():
	data = request.get_json(force=True); 

	distance = data.get("distance");
	adjacency = data.get("adjacency");
	start = data.get("start");
	goal = data.get("goal");

	solver.init(len(distance), distance, adjacency);
	result = solver.solve(start, goal);
	_thread.start_new_thread(drawer.createmapgraph, (distance, adjacency, ) )

	return jsonify(routes=result['routes'], distance=result['distance']);

if __name__ == "__main__":
    app.run(debug=True)