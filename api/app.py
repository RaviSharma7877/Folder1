from flask import Flask, jsonify, g, request
from flask_pymongo import MongoClient
from bson import ObjectId, json_util

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/NovaNotions'

# Specify the allowed keys in the JSON data
ALLOWED_KEYS = ['title', 'desc', 'time', 'img']

def get_db():
    if 'db' not in g:
        g.db = MongoClient(app.config['MONGO_URI'])
    
    return g.db

@app.route('/', methods=['GET'])
def get_data():
    db = get_db()
    data = list(db.NovaNotions.BlogPosts.find())

    # Use json_util.dumps to serialize the data, including handling ObjectId
    return json_util.dumps(data)

@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        db = get_db()
        new_data = request.json

        
        for key in new_data.keys():
            if key not in ALLOWED_KEYS:
                return jsonify({'Error': f'Invalid key: {key}'}), 400

        result = db.NovaNotions.BlogPosts.insert_one(new_data)
        
        return jsonify({'message': 'data added successfully', 'inserted_id': str(result.inserted_id)})
    
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

@app.route('/delete_data/<string:data_id>', methods=['DELETE'])
def delete_data(data_id):
    try:
        db = get_db()

        # Delete the data from the MongoDB collection
        result = db.NovaNotions.BlogPosts.delete_one({'_id': ObjectId(data_id)})

        if result.deleted_count > 0:
            return jsonify({'message': 'Data deleted successfully'})
        else:
            return jsonify({'message': 'No data found for the given ID'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.teardown_appcontext
def teardown_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
