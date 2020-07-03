from flask import Flask, jsonify, request
from es import query
app = Flask(__name__)


####### REST API #######

@app.route('/', methods=['POST'])
def search_box():
    """
    Example request

    Type: HTTP POST + JSON body
    URL: http://localhost:5000/
    JSON body: 
    
            {
            "search": "ඔබට මා",
            "req_filters":0,
            "filters":  {
                    "artist_si":"මාලනී බුලත්සිංහල"
                }
            }

    """

    args = request.json

    search = args['search']
    filters = args['filters']
    req_filters = args['req_filters']
    
    res = query(search,filters=filters,req_filters=req_filters)

    return res
        

if __name__ == "__main__":
    app.run(debug=True)