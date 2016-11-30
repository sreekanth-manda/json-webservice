from flask import Flask, jsonify, abort, Response, request, Blueprint, make_response
import json

webservice = Blueprint('webservice', __name__)


# A method to filter shows which has got drm true and episodeCount is greater than 0 and to remove unwanted keys
def process_shows(shows_info):
    try:
        # Filtered dict to hold filtered shows which has got drm true and episodeCount is greater than 0
        filtered_shows = []
        # Loop over payload to retrieve shows
        for show in shows_info["payload"]:
            if show.has_key("drm"):
                # Process the dict only if drm is true and episode count is greater than 0
                if show["drm"] and show["episodeCount"] > 0:
                    # Select only image, slug and title keys from the matched dict
                    final_dict = {your_key: show[your_key] for your_key in ["image","slug","title"]}
                    filtered_shows.append(final_dict)

        # Remove the showImage key from the image key's value to retain only the value
        for filtered_show in filtered_shows:
            filtered_show["image"] = filtered_show["image"]["showImage"]

        # Make the response a dict
        response = {"response": filtered_shows}

        return response
    except Exception as e:
        print(e)


# A route to home page to handle the json request
@webservice.route("/", methods=['POST'])
def filter_shows():
    try:
        # Get the json from the request
        posted_shows = request.get_json(silent=True)

        # Process the json object only when retireved successfully from request
        if posted_shows:
            # Filter the json as per the requirement
            filtered_shows = process_shows(posted_shows)
            # Return a jsonified response to the requester
            return jsonify(filtered_shows)
        else:
            return make_response(jsonify({"error": "Could not decode request: JSON parsing failed"}), 400)
    except Exception as e:
        print(e)


@webservice.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}), 404)


