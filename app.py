from flask import Flask, request, abort, jsonify
import requests
from datetime import datetime, timedelta
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace with your actual Monday.com API key
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQxMDM1MDMyNiwiYWFpIjoxMSwidWlkIjo1NTIyMDQ0LCJpYWQiOiIyMDI0LTA5LTEzVDExOjUyOjQzLjAwMFoiLCJwZXIiOiJtZTp3cml0ZSIsImFjdGlkIjozNzk1MywicmduIjoidXNlMSJ9.hwTlwMwtbhKdZsYcGT7UoENBLZUAxnfUXchj5RZJBz4"
API_URL = "https://api.monday.com/v2"

#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    print("Welcome")
    return "Welcome to the API!"

@app.route('/webhook', methods=['POST'])
def webhook():

        if request.method == 'POST':
            try:
                webhook_data = request.get_json()
                print("Received webhook data:",
                      webhook_data)  # Debugging: Print received data

                # Extract board ID and item ID from the webhook (adapt to your webhook's structure)
                board_id = webhook_data.get('event', {}).get('boardId', {})
                item_id = webhook_data.get('event', {}).get('pulseId', {})
                pulse_name = webhook_data.get('event', {}).get('pulseName', {})
                pulse_json = jsonify(pulse_name)
                print("Pulse:", pulse_name)

                if isinstance(pulse_name, str):
                    pulse_name = pulse_name.replace('"', '\\"')

                if not board_id:
                    print(
                        "Error: Could not extract board_id or item_id from webhook."
                    )
                    return jsonify(
                        {"error": "Missing board_id or item_id in webhook"}), 400

                # Information you want to send back to Monday.com (Column X)
                # Replace with the actual value

                # Construct the GraphQL mutation to update the column
                headers = {
                    "Authorization": API_KEY,
                    "Content-Type": "application/json"
                }

                query = f'mutation{{ change_simple_column_value (item_id: {item_id},board_id: {board_id}, column_id: "texto_1_mkn58839", value: "{pulse_name}") {{ id }} }}'
                data = {'query': query}

                response = requests.post(url=API_URL, json=data, headers=headers)

                if response.status_code == 200:
                    print("Successfully updated Monday.com column:",
                          response.json())
                    return jsonify({
                        "status": "success",
                        "message": "Column updated"
                    }), 200
                else:
                    print(
                        f"Error updating Monday.com column: {response.status_code} - {response.text}"
                    )
                    return jsonify({
                        "error": "Failed to update column",
                        "monday_response": response.text
                    }), response.status_code

            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing webhook data: {e}")
                return jsonify({"error": "Error processing webhook data"}), 400
            except requests.exceptions.RequestException as e:
                print(f"Error communicating with Monday.com API: {e}")
                return jsonify(
                    {"error": "Error communicating with Monday.com API"}), 500
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return jsonify({"error": "An unexpected error occurred"}), 500
        else:
            abort(400)


#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------


@app.route('/set_subitem_date', methods=['POST'])
def set_subitem_date():
    if request.method == 'POST':
        try:
            webhook_data = request.get_json()
            print("Received webhook data:",
                  webhook_data)  # Debugging: Print received data

            # Extract board ID and item ID from the webhook (adapt to your webhook's structure)
            item_id = webhook_data.get('event', {}).get('parentItemId', {})
            board_id = webhook_data.get('event',
                                        {}).get('parentItemBoardId', {})
            subitem_board_id = webhook_data.get('event', {}).get('boardId', {})
            subitem_id = webhook_data.get('event', {}).get('pulseId', {})
            subitem_number = webhook_data.get('event',
                                             {}).get('n_meros_mkm9dpdt', {})
            subitem_offset = webhook_data.get('event',
                                              {}).get('n_meros_mkmx3p62',
                                                      {}).get('value')
            subitem_json = jsonify(subitem_id)
            subitem_json = jsonify(subitem_number)
            n_meros_mkmx3p62_value = webhook_data.get('event', {}).get(
                'n_meros_mkmx3p62', {}).get('value', None)

            import time

            # ... (other code)

            time.sleep(2)  # Wait for 2 seconds (just for testing!)

            numbers_column = webhook_data.get('event',
                                              {}).get('n_meros_mkmx3p62')

            #if isinstance(pulse_name, str):
            #pulse_name = pulse_name.replace('"', '\\"')

            if not subitem_board_id:
                print(
                    "Error: Could not extract board_id or item_id from webhook."
                )
                return jsonify(
                    {"error": "Missing board_id or item_id in webhook"}), 400

            # Information you want to send back to Monday.com (Column X)
            # Replace with the actual value

            # Construct the GraphQL mutation to update the column
            headers = {
                "Authorization": API_KEY,
                "Content-Type": "application/json"
            }

            # First query to get the date
            date_query = f"""
            query {{items (ids: [{item_id}]) {{
                column_values {{
                    ... on DateValue {{
                        date
                    }}
                }}
            }}}}"""

            response = requests.post(url=API_URL,
                                     json={'query': date_query},
                                     headers=headers)
            date_data = response.json()

            # Extract the date value from response
            try:
                date_value = ""
                column_values = date_data['data']['items'][0]['column_values']
                for column in column_values:
                    if 'date' in column:
                        date_value = column['date']
                        break
            except (KeyError, IndexError):
                date_value = ""

            # Convert string date to datetime, add days, then format back to string
            current_date = datetime.strptime(date_value, '%Y-%m-%d')

            offset_days = int(list(subitem_offset)[0]) if subitem_offset else 0
            new_date = (current_date +
                        timedelta(days=offset_days)).strftime('%Y-%m-%d')

            # Second query to update with the extracted
            number_query = f"""
                query {{items (ids: [{subitem_id}]) {{
                    column_values {{
                        ... on NumbersValue {{
                            number
                              }}
                          }}
                      }}}}"""

            response = requests.post(url=API_URL,
                                     json={'query': number_query},
                                     headers=headers)
            number_data = response.json()

            try:
                number_value = ""
                column_values = number_data['data']['items'][0][
                    'column_values']
                for column in column_values:
                    if 'number' in column:
                        number_value = column['number']
                        break
            except (KeyError, IndexError):
                number_value = ""
                print("number value is:", number_value)

            # Convert string date to datetime, add days, then format back to string
            current_date = datetime.strptime(date_value, '%Y-%m-%d')

            offset_days = int(list(subitem_offset)[0]) if subitem_offset else 0
            new_date = (current_date +
                        timedelta(days=offset_days)).strftime('%Y-%m-%d')

            date_data = response.json()

            update_query = f'mutation{{ change_simple_column_value (item_id: {subitem_id}, board_id: {subitem_board_id}, column_id: "dup__of_data_mkmx6xcr", value: "{date_value}") {{ id }} }}'
            data = {'query': update_query}

            response = requests.post(url=API_URL, json=data, headers=headers)

            if number_value == 1:

                updateid_query = f'mutation{{ change_simple_column_value (item_id: {item_id}, board_id: {board_id}, column_id: "texto_1_mkncnqc9", value: "{subitem_id}") {{ id }} }}'
                data = {'query': updateid_query}

            response = requests.post(url=API_URL, json=data, headers=headers)

            if number_value == 1:

                updateboardid_query = f'mutation{{ change_simple_column_value (item_id: {item_id}, board_id: {board_id}, column_id: "texto_mknc26v7", value: "{subitem_board_id}") {{ id }} }}'
                data = {'query': updateboardid_query}

            response = requests.post(url=API_URL, json=data, headers=headers)

            if number_value == 2:

                updateid2_query = f'mutation{{ change_simple_column_value (item_id: {item_id}, board_id: {board_id}, column_id: "texto_2_mkncg9ba", value: "{subitem_id}") {{ id }} }}'
                data = {'query': updateid2_query}

            response = requests.post(url=API_URL, json=data, headers=headers)



            if response.status_code == 200:
                print("Successfully updated Monday.com column:",
                      response.json())
                return jsonify({
                    "status": "success",
                    "message": "Column updated"
                }), 200
            else:
                print(
                    f"Error updating Monday.com column: {response.status_code} - {response.text}"
                )
                return jsonify({
                    "error": "Failed to update column",
                    "monday_response": response.text
                }), response.status_code

        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error processing webhook data: {e}")
            return jsonify({"error": "Error processing webhook data"}), 400
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Monday.com API: {e}")
            return jsonify(
                {"error": "Error communicating with Monday.com API"}), 500
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return jsonify({"error": "An unexpected error occurred"}), 500
    else:
        abort(400)


#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------


@app.route('/change_subitem_date', methods=['POST'])
def change_subitem_date():
    if request.method == 'POST':
        webhook_data = request.get_json()
        print("Received webhook data:", webhook_data)

        try:
            board_id = webhook_data.get('event', {}).get('boardId', {})
            item_id = webhook_data.get('event', {}).get('pulseId', {})
            pulse_name = webhook_data.get('event', {}).get('pulseName', {})
            print("Pulse:", pulse_name)

            if isinstance(pulse_name, str):
                pulse_name = pulse_name.replace('"', '\\"')

            if not board_id:
                print("Error: Could not extract board_id or item_id from webhook.")
                return jsonify({"error": "Missing board_id or item_id in webhook"}), 400

            headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

            print("item é:", item_id)

            subitem1_query = f"""query {{ items (ids: ["{item_id}"]) {{ column_values (ids: ["texto_1_mkncnqc9"]) {{ ... on TextValue {{ text }} }} }} }}"""
            response = requests.post(url=API_URL, json={'query': subitem1_query}, headers=headers)
            subitem1 = response.json()
            subitem1_value = int(subitem1['data']['items'][0]['column_values'][0]['text'])
            
            print("Coluna subitem 1 é:", subitem1_value)
            

            subitem2_query = f"""query {{ items (ids: ["{item_id}"]) {{ column_values (ids: ["texto_2_mkncg9ba"]) {{ ... on TextValue {{ text }} }} }} }}"""
            response = requests.post(url=API_URL, json={'query': subitem2_query}, headers=headers)
            subitem2 = response.json()
            subitem2_value = int(subitem2['data']['items'][0]['column_values'][0]['text'])
            print("Coluna subitem 2 é:", subitem2_value)

            subitemboard_query = f"""query {{ items (ids: ["{item_id}"]) {{ column_values (ids: ["texto_mknc26v7"]) {{ ... on TextValue {{ text }} }} }} }}"""
            response = requests.post(url=API_URL, json={'query': subitemboard_query}, headers=headers)
            subitemboard = response.json()
            subitemboard_value = int(subitemboard['data']['items'][0]['column_values'][0]['text'])
            print("Subitem board é:", subitemboard_value)

            date_query = f"""query {{items (ids: [{item_id}]) {{ column_values {{ ... on DateValue {{ date }} }} }}}}"""
            response = requests.post(url=API_URL, json={'query': date_query}, headers=headers)
            date_data = response.json()

            
            try:
                date_value = ""
                column_values = date_data['data']['items'][0]['column_values']
                for column in column_values:
                    if 'date' in column:
                        date_value = column['date']
                        break
            except (KeyError, IndexError):
                date_value = ""
                print ("datevalue: " , date_value)
            

            current_date = datetime.strptime(date_value, '%Y-%m-%d')
            print ("currenttime:" , current_date)

            update_query = f"""
            mutation {{
              change_multiple_column_values (
                item_id: {subitem1_value},
                board_id: {subitemboard_value},
                column_values: "{{\\\"dup__of_data_mkmx6xcr\\\": \\\"{date_value}\\\", \\\"label_mkncg3sn\\\": \\\"Update date\\\"}}"
              ) {{
                id
              }}
            }}
            """
            data = {'query': update_query}
            response = requests.post(url=API_URL, json=data, headers=headers)


           
            update_query = f"""
            mutation {{
              change_multiple_column_values (
                item_id: {subitem2_value},
                board_id: {subitemboard_value},
                column_values: "{{\\\"dup__of_data_mkmx6xcr\\\": \\\"{date_value}\\\", \\\"label_mkncg3sn\\\": \\\"Update date\\\"}}"
              ) {{
                id
              }}
            }}
            """
            data = {'query': update_query}
            response = requests.post(url=API_URL, json=data, headers=headers)

            return jsonify({"success": True})

        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error processing webhook data: {e}")
            return jsonify({"error": "Error processing webhook data"}), 400
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Monday.com API: {e}")
            return jsonify({"error": "Error communicating with Monday.com API"}), 500
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return jsonify({"error": "An unexpected error occurred"}), 500
    else:
        abort(400)

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI1OTU3MDMyMiwiYWFpIjoxMSwidWlkIjozNDE4MzA0NCwiaWFkIjoiMjAyMy0wNS0zMFQyMzo0NTo0MS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTMzMzU3NzgsInJnbiI6InVzZTEifQ.wo708JzzeAC1eqo1Gfq1yiPtB4tgppDhKqSPfjToRf8"
API_URL = "https://api.monday.com/v2"
TARGET_BOARD_ID = 6712850239
SOURCE_BOARD_ID = 6501400021
SOURCE_LINKED_COLUMN_ID = "conectar_quadros9__1"
SOURCE_COLUMN_ID_TEXT_1 = "texto_11__1"
SOURCE_COLUMN_ID_TEXT_2 = "texto__1"
TARGET_COLUMN_ID_TEXT_1 = "texto_1_mkmqamdc"
TARGET_COLUMN_ID_TEXT_2 = "texto_1_mkn4dmy7"
TARGET_COLUMN_ID_NAME = "text_mkpdbm8b"  # Corrected column ID

def update_monday_item(item_id, board_id, column_values, api_key, api_url, logger):
    """
    Updates a Monday.com item with the provided column values
    """
    try:
        # Ensure keys in column_values are strings
        stringified_column_values = {str(k): v for k, v in column_values.items()}
        column_values_json = json.dumps(stringified_column_values).replace('"', '\\"')

        # Create the GraphQL mutation
        mutation = f"""
        mutation {{
          change_multiple_column_values (
            item_id: {item_id},
            board_id: {board_id},
            column_values: "{column_values_json}"
          ) {{
            id
          }}
        }}
        """

        logger.debug(f"Mutation: {mutation}")

        # Make the API call
        headers = {"Authorization": api_key, "Content-Type": "application/json"}
        payload = {'query': mutation}

        response = requests.post(url=api_url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        logger.debug(f"Update response: {result}")

        # Check if the update was successful
        if result.get('data', {}).get('change_multiple_column_values', {}).get('id'):
            return True
        else:
            logger.error(f"Failed to update item {item_id} on board {board_id}. Response: {result}")
            return False

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error updating Monday.com item {item_id}: {str(e)}")
        if response is not None:
            logger.error(f"Response content: {response.text}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in update response for item {item_id}: {str(e)}")
        if response is not None:
            logger.error(f"Response content: {response.text}")
        return False
    except Exception as e:
        logger.error(f"Error updating Monday.com item {item_id}: {str(e)}")
        return False

@app.route('/pressure-copy-items-to-txt', methods=['POST'])
def pressure_copy_items_to_txt():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if 'challenge' in data:
                challenge = data['challenge']
                print("Received challenge:", challenge)
                return jsonify({'challenge': challenge}), 200

            webhook_data = data
            print("Received webhook data:", webhook_data)

            # Extract the triggering item ID
            triggering_item_id = webhook_data.get('event', {}).get('pulseId')

            # Extract the linked item ID from the payload
            linked_pulse_ids = webhook_data.get('event', {}).get('value', {}).get('linkedPulseIds')

            linked_item_id = None
            if linked_pulse_ids and isinstance(linked_pulse_ids, list) and linked_pulse_ids:
                linked_item_id = linked_pulse_ids[0].get('linkedPulseId')

            if linked_item_id:
                print(f"Extracted Linked Item ID: {linked_item_id}")
                print(f"Triggering Item ID: {triggering_item_id}")

                headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

                # --- Query to get the NAME of the linked item ---
                query_get_linked_item_name = f"""
                    query {{
                      items (ids: [{linked_item_id}]) {{
                        name
                      }}
                    }}
                """
                data_get_linked_item_name = {'query': query_get_linked_item_name}
                monday_response_get_name = requests.post(url=API_URL, json=data_get_linked_item_name, headers=headers)
                monday_data_get_name = monday_response_get_name.json()

                linked_item_name = None
                if monday_response_get_name.status_code == 200 and monday_data_get_name.get('data') and monday_data_get_name['data'].get('items') and monday_data_get_name['data']['items']:
                    linked_item_name = monday_data_get_name['data']['items'][0].get('name')
                    print(f"Name of linked item (ID: {linked_item_id}): {linked_item_name}")
                else:
                    logger.error(f"Error fetching name of linked item (ID: {linked_item_id}): {monday_response_get_name.status_code} - {monday_response_get_name.text}")
                    # Decide how to proceed if the name cannot be fetched
                    linked_item_name = "" # Or handle the error differently

                # --- Query to get other column values from the linked item ---
                query_get_linked_item_data = f"""
                    query {{
                      items (ids: [{linked_item_id}]) {{
                        column_values (ids: ["{SOURCE_COLUMN_ID_TEXT_1}", "{SOURCE_COLUMN_ID_TEXT_2}"]) {{
                          id
                          text
                        }}
                      }}
                    }}
                """
                data_get_linked_item_data = {'query': query_get_linked_item_data}
                monday_response_get_data = requests.post(url=API_URL, json=data_get_linked_item_data, headers=headers)
                monday_data_get_data = monday_response_get_data.json()

                linked_item_text_1_value = ""
                linked_item_text_2_value = ""

                if monday_response_get_data.status_code == 200 and monday_data_get_data.get('data') and monday_data_get_data['data'].get('items') and monday_data_get_data['data']['items']:
                    linked_item = monday_data_get_data['data']['items'][0]
                    linked_item_text_1_value = next((cv.get('text') for cv in linked_item.get('column_values', []) if cv.get('id') == SOURCE_COLUMN_ID_TEXT_1), "")
                    linked_item_text_2_value = next((cv.get('text') for cv in linked_item.get('column_values', []) if cv.get('id') == SOURCE_COLUMN_ID_TEXT_2), "")

                    print(f"Value of '{SOURCE_COLUMN_ID_TEXT_1}': {linked_item_text_1_value}")
                    print(f"Value of '{SOURCE_COLUMN_ID_TEXT_2}': {linked_item_text_2_value}")

                    # Prepare the column values to update, including the linked item's name
                    column_values_to_update = {
                        TARGET_COLUMN_ID_TEXT_1: linked_item_text_1_value,
                        TARGET_COLUMN_ID_TEXT_2: linked_item_text_2_value,
                        TARGET_COLUMN_ID_NAME: linked_item_name
                    }

                    # Update the Monday.com item using the new function
                    if update_monday_item(triggering_item_id, TARGET_BOARD_ID, column_values_to_update, API_KEY, API_URL, logger):
                        print(f"Successfully updated columns '{TARGET_COLUMN_ID_TEXT_1}', '{TARGET_COLUMN_ID_TEXT_2}', and '{TARGET_COLUMN_ID_NAME}'.")
                        return jsonify({"message": f"Columns '{TARGET_COLUMN_ID_TEXT_1}', '{TARGET_COLUMN_ID_TEXT_2}', and '{TARGET_COLUMN_ID_NAME}' updated."}), 200
                    else:
                        logger.error(f"Failed to update item {triggering_item_id} on board {TARGET_BOARD_ID} with values: {column_values_to_update}")
                        return jsonify({"error": f"Failed to update columns on Monday.com. Check server logs for details."}), 500
                else:
                    error_message = f"Error fetching data from linked item (ID: {linked_item_id}) on board {SOURCE_BOARD_ID}: {monday_response_get_data.status_code} - {monday_response_get_data.text}"
                    logger.error(error_message)
                    return jsonify({"error": error_message}), monday_response_get_data.status_code
            else:
                logger.info("'linkedPulseIds' not found in the webhook data (likely a removal). Skipping processing.")
                return jsonify({"message": "'linkedPulseIds' not found, skipping processing."}), 200

        except Exception as e:
            logger.error(f"Error processing webhook data: {str(e)}")
            return jsonify({"error": f"Error processing webhook data: {str(e)}"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405


@app.route('/pressure-rename-subitem', methods=['POST'])
def pressure_rename_subitem():
    if request.method == 'POST':
        try:
            webhook_data = request.get_json()
            linked_pulse_ids = webhook_data.get('event', {}).get('value', {}).get('linkedPulseIds')
            triggering_pulse_id = webhook_data.get('event', {}).get('pulseId')
            triggering_board_id = webhook_data.get('event', {}).get('boardId') # Extract boardId

            if not triggering_pulse_id:
                print("Error: Triggering pulse ID not found in the payload.")
                return jsonify({"error": "Triggering pulse ID not found"}), 400

            if not triggering_board_id:
                print("Error: Triggering board ID not found in the payload.")
                return jsonify({"error": "Triggering board ID not found"}), 400

            if linked_pulse_ids and isinstance(linked_pulse_ids, list) and linked_pulse_ids:
                linked_pulse_id = linked_pulse_ids[0].get('linkedPulseId')
                print(f"Liked pulse id is: {linked_pulse_id}")
                print(f"Triggering pulse id is: {triggering_pulse_id}")
                print(f"Triggering board id is: {triggering_board_id}") # Print the extracted board ID

                monday_board_id = 6437270183
                column_id_to_retrieve = "texto90__1"
                headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

                # Query to get the value from the linked item
                query_get_value = f"""
                    query {{
                        items (ids: [{linked_pulse_id}]) {{
                            column_values (ids: ["{column_id_to_retrieve}"]) {{
                                text
                            }}
                        }}
                    }}
                """
                data_get_value = {'query': query_get_value}
                response_get_value = requests.post(url=API_URL, json=data_get_value, headers=headers)
                response_get_value.raise_for_status()
                monday_data_get_value = response_get_value.json()

                column_value = None
                if monday_data_get_value.get('data', {}).get('items') and monday_data_get_value['data']['items']:
                    item_data = monday_data_get_value['data']['items'][0]
                    if item_data.get('column_values'):
                        for col in item_data['column_values']:
                            if col.get('text') is not None:
                                column_value = col['text']
                                break

                print(f"Value of column '{column_id_to_retrieve}' for item {linked_pulse_id}: {column_value}")
                print("Received payload:", request.get_json())
                if column_value is not None:
                    # Mutation to update the name of the triggering pulse ID
                    new_name_for_subitem = column_value # Use the fetched value as the new name
                    mutation_rename = f"""
                        mutation {{
                            change_simple_column_value (item_id: {triggering_pulse_id}, board_id: {triggering_board_id}, column_id: "name", value: "{new_name_for_subitem}") {{
                                id
                            }}
                        }}
                    """
                    data_rename = {'query': mutation_rename}
                    print("Rename API Payload:", json.dumps(data_rename))  # Debugging line
                    response_rename = requests.post(url=API_URL, json=data_rename, headers=headers)
                    response_rename.raise_for_status()
                    monday_data_rename = response_rename.json()
                    print("Rename response:", monday_data_rename)

                    if monday_data_rename.get('data', {}).get('change_item_name', {}).get('id'):
                        print(f"Successfully renamed item {triggering_pulse_id} to '{column_value}'.")
                        return jsonify({"status": "success", "linkedPulseId": linked_pulse_id, "columnValue": column_value, "renamedItemId": triggering_pulse_id, "newName": column_value}), 200
                    else:
                        error_message_rename = monday_data_rename.get('errors', [{}])[0].get('message', 'Failed to rename item')
                        print(f"Error renaming item {triggering_pulse_id}: {error_message_rename}")
                        return jsonify({"status": "processed", "linkedPulseId": linked_pulse_id, "columnValue": column_value, "renameError": error_message_rename}), 500
                else:
                    print(f"Value not found in column '{column_id_to_retrieve}' for item {linked_pulse_id}.")
                    return jsonify({"status": "processed", "linkedPulseId": linked_pulse_id, "columnValue": None, "renameStatus": "value_not_found"}), 200

            else:
                print("Liked pulse IDs not found or is not a valid list in the payload.")
                return jsonify({"status": "skipped", "message": "Liked pulse IDs not found"}), 200

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Monday.com API: {e}")
            if 'response_rename' in locals() and hasattr(response_rename, 'text'):  # Use response_rename here
                print(f"Response content: {response_rename.text}")
            return jsonify({"error": f"API communication error: {e}"}), 500
        except Exception as e:
            print(f"Error processing payload: {e}")
            return jsonify({"error": f"Error processing payload: {e}"}), 400
    else:
        abort(400)
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
