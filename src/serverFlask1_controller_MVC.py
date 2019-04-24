
from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/')
def hello_amibo():
    return 'hello amibo'

@app.route('/activity/statistic/fall', methods=['POST'])
def register():
    print ("1----------------------\n",request.content_type)
    print ("2----------------------\n",request.headers)
    print ("3----------------------\n",request.json)

    rt = {'4--'+'resp fromServer:':'FlaskServer:'+request.json }
    print (rt)
    return Response(json.dumps(rt),  mimetype='application/json')
    # print ("3----------------------\n",request.form)
    # print ("4----------------------\n",request.form['name'])
    # print ("5----------------------\n",request.form.get('name'))
    # print ("6----------------------\n",request.form.getlist('name'))
    # print ("7----------------------\n",request.form.get('nickname', default='little apple'))
    return "Welcome"

@app.route('/activity/statistic/face_type', methods=['POST'])
def register1():
    print ("1----------------------\n",request.content_type)
    print ("2----------------------\n",request.headers)
    print ("3----------------------\n",request.json)

    rt = {'4--'+'resp fromServer:':'FlaskServer:'+request.json }
    print (rt)
    return Response(json.dumps(rt),  mimetype='application/json')
    # print ("3----------------------\n",request.form)
    # print ("4----------------------\n",request.form['name'])
    # print ("5----------------------\n",request.form.get('name'))
    # print ("6----------------------\n",request.form.getlist('name'))
    # print ("7----------------------\n",request.form.get('nickname', default='little apple'))
    return "Welcome"

@app.route('/json', methods=['POST'])
def my_json():
    print (request.headers)
    print (request.json)
    rt = {'info':'FlaskServer: '+request.json['name']}
    return Response(json.dumps(rt),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)