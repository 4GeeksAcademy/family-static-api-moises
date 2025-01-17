import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    response = jsonify(jackson_family.get_all_members())
    response.headers['Content-Type'] = 'application/json'
    return response, 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        response = jsonify(member)
        response.headers['Content-Type'] = 'application/json'
        return response, 200
    return jsonify({"message": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    if not request.json:
        return jsonify({"message": "Invalid request body"}), 400
    
    required_fields = ["first_name", "age", "lucky_numbers"]
    for field in required_fields:
        if field not in request.json:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    member = request.json
    added_member = jackson_family.add_member(member)
    response = jsonify(added_member)
    response.headers['Content-Type'] = 'application/json'
    return response, 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    response = jsonify(result)
    response.headers['Content-Type'] = 'application/json'
    return response, 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)