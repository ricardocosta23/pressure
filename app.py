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
        data = request.get_json()
        challenge = data['challenge']

        return jsonify({'challenge': challenge})

        # print(request.json)
        # return 'success', 200
    else:
        abort(400)
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
