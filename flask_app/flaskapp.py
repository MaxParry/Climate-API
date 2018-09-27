from flask import Flask, jsonify
import pandas as pd

# initialize app
app = Flask(__name__)

# outline filepath for CSVs
csv1 = ("../Output/measurements_clean.csv")
csv2 = ("../Output/stations_clean.csv")

# read in CSVs for later manipulation
measurements = pd.DataFrame(pd.read_csv(csv1))
stations = pd.DataFrame(pd.read_csv(csv2))

# isolate date and precipitation, convert to dict to prepare for delivery
prcp_dict = measurements[['date', 'prcp']].set_index('date').to_dict()

# convert station dataframe to dictionary
stat_dict = stations.to_dict(orient='index')

# convert temperature information to dictionary
temp_dict = measurements[['date', 'tobs']].set_index('date').to_dict()

# convert date field in measurements to make searchable
new_measurements = measurements
new_measurements.date = new_measurements.date.map(lambda x: x.replace("-", "")).astype(int)

@app.route("/api/v1.0")
def index():
    print('Someone has visited the index page')
    return "Welcome to the index page."

@app.route("/api/v1.0/precipitation")
def precipitation():
    print('Someone has visited the precipitation page')
    return jsonify(prcp_dict['prcp'])

@app.route("/api/v1.0/stations")
def stations():
    print('Someone has visited the stations page')
    return jsonify(stat_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    print('Someone has visited the temperature page')
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    print('Someone has visited the start page')
    parsed_start = int(start.replace('-', ''))
    parsed_end = new_measurements.date.max()
    subset_meas = new_measurements[(new_measurements.date >= parsed_start) & (new_measurements.date <= parsed_end)]
    maxtemp = subset_meas.tobs.max()
    mintemp = subset_meas.tobs.min()
    avgtemp = subset_meas.tobs.mean()
    print('For date range selected, the:\nMax temp is: ', maxtemp, '\nMin temp is: ', mintemp, '\nAverage temp is: ', avgtemp)
    return jsonify({"Maximum Temperature": str(maxtemp),
                    "Minimum Temperature": str(mintemp),
                    "Average Temperature": str(avgtemp)})

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Someone has visited the start/end page")
    parsed_start = int(start.replace('-', ''))
    parsed_end = int(end.replace('-', ''))
    subset_meas = new_measurements[(new_measurements.date >= parsed_start) & (new_measurements.date <= parsed_end)]
    maxtemp = subset_meas.tobs.max()
    mintemp = subset_meas.tobs.min()
    avgtemp = subset_meas.tobs.mean()
    print('For date range selected, the:\nMax temp is: ', maxtemp, '\nMin temp is: ', mintemp, '\nAverage temp is: ', avgtemp)
    return jsonify({"Maximum Temperature": str(maxtemp),
                    "Minimum Temperature": str(mintemp),
                    "Average Temperature": str(avgtemp)})



if __name__ == "__main__":
    app.run(debug=True)

