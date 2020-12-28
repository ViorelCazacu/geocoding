from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas, geopy
from geopy.geocoders import Nominatim
import datetime

geolocator = Nominatim(user_agent="app10.py")


app=Flask(__name__)

@app.route("/")
def index ():
    return render_template("index2.html")

@app.route("/success", methods=['POST'])
def success ():
    global file
    global filenamesave
    if request.method=='POST':
        file=request.files["file"]    
        
        df=pandas.read_csv (file.filename)
        df= df.rename(columns=str.lower)
        if 'address' in df:
            df['lat'] = [g.latitude for g in df.address.apply(geolocator.geocode)]
            df['long'] = [g.longitude for g in df.address.apply(geolocator.geocode)]
            df= df.rename(columns=str.capitalize)
            filenamesave=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"+".csv")
            df.to_csv(filenamesave)
           
            print(df)
            print(file)
            print(type(file))
            return render_template("index2.html", btn="download.html", tables=[df.to_html(classes='data')], titles=df.columns.values)
        else:
            return render_template("index2.html", 
                   text="Please make sure you have an address column in your CSV file!")

@app.route("/download")
def download():
    return send_file(filenamesave, attachment_filename="yourfileappended.csv", as_attachment=True)


if __name__ == '__main__':
    app.debug=True
    app.run()
 