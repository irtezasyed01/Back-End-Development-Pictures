from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # Find the picture URL with the given id in the data list
    picture = next((item for item in data if item['id'] == id), None)

    if picture:
        # If the picture with the given id is found, return it as a JSON response
        return jsonify(picture)
    else:
        # If the picture with the given id is not found, return a 404 error response
        return jsonify({'error': 'Picture not found'}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route('/picture/<int:id>', methods=['POST'])
def create_picture(id):
    # Extract picture data from the request body (Assuming the data is in JSON format)
    picture_data = request.json

    # Check if a picture with the given id already exists in the data list
    for item in data:
        if item['id'] == id:
            # If picture with given id already exists, send a 302 response with an error message
            return jsonify({"Message": f"Picture with id {id} already present"}), 302

    # Append the new picture data to the data list
    picture_data['id'] = id
    data.append(picture_data)

    # Return a success message and the updated data list as JSON response
    return jsonify({"Message": "Picture created successfully", "Data": data, "id": id}), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route('/picture/<int:id>', methods=['PUT'])
def update_picture(id):
    # Get the picture by id from the data list
    picture = next((item for item in data if item['id'] == id), None)

    if picture is None:
        # If picture with given id does not exist, return a 404 response
        return jsonify({"Message": f"Picture with id {id} not found"}), 404

    # Update the picture data with the new data from the request body
    picture_data = request.json
    picture.update(picture_data)

    # Return a success message and the updated picture data as JSON response
    return jsonify({"Message": f"Picture with id {id} updated successfully", "Data": picture}), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route('/picture/<int:id>', methods=['DELETE'])
def delete_picture(id):
    # Get the index of the picture with the given id from the data list
    index = next((index for index, item in enumerate(data) if item['id'] == id), None)

    if index is None:
        # If picture with given id does not exist, return a 404 response
        return jsonify({"Message": f"Picture with id {id} not found"}), 404

    # Remove the picture from the data list
    data.pop(index)

    # Return a success message with a 204 status code (No Content)
    return "", 204
