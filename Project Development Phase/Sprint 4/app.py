from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        arr.append(1)
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("index"))
            arr.append(float(val))
       # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        API_KEY = "CTGlYcSCkcFcIwbHI5fF2a-1qPwnpVszfMZg_hAwk_Ff"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        payload_scoring = {
            "input_data": [{"fields":[  'Serial No.',
                                        'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], 
                            "values": [arr]
                            }]
                        }

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1ecff247-604d-45ad-a420-b4d8ede8a8fa/predictions?version=2022-11-06', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print(response_scoring)
        predictions = response_scoring.json()
        predict = predictions['predictions'][0]['values'][0][0]
        print("Final prediction :",predict)
        
        if  predict > 0.5:
            return redirect(url_for('chance', percent=int(predict*100)))
        else:
            return redirect(url_for('no_chance', percent=int(predict*100)))
    else:
        return redirect(url_for("demo"))


@app.route("/home")
def demo():
    return render_template("index.html")

@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)