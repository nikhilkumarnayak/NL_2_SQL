import uvicorn
from pyngrok import ngrok
from flask import Flask, jsonify, request
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
import lang_nl2sql as lns
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ''
app.config['ALLOWED_EXTENSIONS'] = {'sql'}
app.config['uploaded_sql'] = {'path': None, 'name': None}
CORS(app)



## Run in local
@app.route('/getsqlwithresult', methods=['POST'])
def get_sqlQueryWithResult():
    try:
        input_data = request.json
        if input_data["question"] == '' and input_data["database_name"] == '':
            return jsonify({'status': 'error', 'message': 'No Question and Database entry found'})
        elif input_data["question"] == '':
            return jsonify({'status': 'error', 'message': 'No Question entry found'})
        elif input_data["database_name"] == '':
            return jsonify({'status': 'error', 'message': 'No Database entry found'})

        qus = input_data["question"]
        db_name = input_data["database_name"]
        question, sql_query, sql_result = lns.get_sql_with_result(qus,db_name)
        sql_query = sql_query.replace('\n', ' ')
        return jsonify({"status": "success", 'message': 'SQL query creation Completed', "question": question,
                        "sql_query": sql_query,
                        "sql_result": sql_result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/getsqlquery', methods=['POST'])
def get_sqlQuery():
    try:
        input_data = request.json
        if input_data["question"] == '' and input_data["database_name"] == '':
            return jsonify({'status': 'error', 'message': 'No Question and Database entry found'})
        elif input_data["question"] == '':
            return jsonify({'status': 'error', 'message': 'No Question entry found'})
        elif input_data["database_name"] == '':
            return jsonify({'status': 'error', 'message': 'No Database entry found'})

        qus = input_data["question"]
        db_name = input_data["database_name"]
        question, sql_query = lns.get_only_sql_query(qus,db_name)
        sql_query = sql_query.replace('\n', ' ')
        return jsonify({"status": "success", 'message': 'SQL query creation Completed', "question": question,
                        "sql_query": sql_query}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/getsqlresult', methods=['POST'])
def get_sqlResult():
    try:
        input_data = request.json
        if input_data["question"] == '' and input_data["database_name"] == '':
            return jsonify({'status': 'error', 'message': 'No Question and Database entry found'})
        elif input_data["question"] == '':
            return jsonify({'status': 'error', 'message': 'No Question entry found'})
        elif input_data["database_name"] == '':
            return jsonify({'status': 'error', 'message': 'No Database entry found'})

        qus = input_data["question"]
        db_name = input_data["database_name"]
        question, sql_result = lns.get_only_sqlquery_result(qus,db_name)
        return jsonify({"status": "success", 'message': 'SQL query creation Completed', "question": question,
                        "sql_result": sql_result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/executesqlfile',methods=['POST'])
def execute_sqlQuery():
    if 'executeSQLFile' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['executeSQLFile']
    print("file", file)

    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        app.config['uploaded_sql'] = {'path': file_path, 'name': filename}

        if filename.lower().endswith('.sql'):
            try:
                lns.execute_mysql_file(file_path)
                os.remove(file_path)
                return jsonify({'status': 'success', 'message': 'File Execution Completed', 'filename': filename}), 200
            except Exception as e:
                os.remove(file_path)
                return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            os.remove(file_path)
            return jsonify({'status': 'error', 'message': 'Unsupported file format'}), 400


    else:
        return jsonify({'status': 'error', 'message': 'File type not allowed or unsupported format'}), 400


@app.route('/get_db_names', methods=['GET'])
def get_db_names():

    db_names = lns.get_all_db_names()

    if db_names:
        return jsonify({'status': 'success', 'database_names': db_names}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to fetch database names'}), 500

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    uvicorn.run(asgi_app, host="127.0.0.1", port=8000, log_level="info")
