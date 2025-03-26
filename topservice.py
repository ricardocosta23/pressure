from flask import Flask, request, abort, jsonify
import requests
import json

app = Flask(__name__)

# Replace with your actual Monday.com API key
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ0NDgyMTkzNywiYWFpIjoxMSwidWlkIjo1MDUxOTQxNiwiaWFkIjoiMjAyNC0xMi0wNVQxMTo0NDo1MS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTk0MDQyNTAsInJnbiI6InVzZTEifQ.NoFHSo0NrcRf6n-NpVXljfaWXg5wU4uO04wdmKBvHEs"
API_URL = "https://api.monday.com/v2"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            webhook_data = request.get_json()
            print("Received webhook data:", webhook_data)  # Debugging: Print received data

            # Extract board ID and item ID from the webhook (adapt to your webhook's structure)
            board_id = webhook_data.get('event', {}).get('boardId', {})
            item_id = webhook_data.get('event', {}).get('pulseId', {})
            pulse_name = webhook_data.get('event', {}).get('pulseName', {})
            pulse_json = jsonify(pulse_name)
            print("Pulse:", pulse_name)

            if isinstance(pulse_name, str):
                 pulse_name = pulse_name.replace('"', '\\"')

            if not board_id:
                print("Error: Could not extract board_id or item_id from webhook.")
                return jsonify({"error": "Missing board_id or item_id in webhook"}), 400

            # Information you want to send back to Monday.com (Column X)
             # Replace with the actual value

            # Construct the GraphQL mutation to update the column
            headers = {"Authorization": API_KEY, "Content-Type": "application/json"}



            query = f'mutation{{ change_simple_column_value (item_id: {item_id},board_id: {board_id}, column_id: "texto_1_mkn58839", value: "{pulse_name}") {{ id }} }}'
            data = {'query': query}




            response = requests.post(url=API_URL, json=data, headers=headers)

            if response.status_code == 200:
                print("Successfully updated Monday.com column:", response.json())
                return jsonify({"status": "success", "message": "Column updated"}), 200
            else:
                print(f"Error updating Monday.com column: {response.status_code} - {response.text}")
                return jsonify({"error": "Failed to update column", "monday_response": response.text}), response.status_code

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

@app.route('/webhook2', methods=['POST'])
def webhook2():
    if request.method == 'POST':
        try:
            webhook_data = request.get_json()
            print("Received webhook data:", webhook_data)  # Debugging: Print received data

            # Extract board ID and item ID from the webhook (adapt to your webhook's structure)
            board_id = webhook_data.get('event', {}).get('boardId', {})
            item_id = webhook_data.get('event', {}).get('pulseId', {})
            pulse_name = webhook_data.get('event', {}).get('pulseName', {})
            pulse_json = jsonify(pulse_name)
            print("Pulse:", pulse_name)

            if isinstance(pulse_name, str):
                 pulse_name = pulse_name.replace('"', '\\"')

            if not board_id:
                print("Error: Could not extract board_id or item_id from webhook.")
                return jsonify({"error": "Missing board_id or item_id in webhook"}), 400

            # Information you want to send back to Monday.com (Column X)
             # Replace with the actual value

            # Construct the GraphQL mutation to update the column
            headers = {"Authorization": API_KEY, "Content-Type": "application/json"}



            query = f'mutation{{ change_simple_column_value (item_id: {item_id},board_id: {board_id}, column_id: "texto_1_mkn58839", value: "{pulse_name}") {{ id }} }}'
            data = {'query': query}




            response = requests.post(url=API_URL, json=data, headers=headers)

            if response.status_code == 200:
                print("Successfully updated Monday.com column:", response.json())
                return jsonify({"status": "success", "message": "Column updated"}), 200
            else:
                print(f"Error updating Monday.com column: {response.status_code} - {response.text}")
                return jsonify({"error": "Failed to update column", "monday_response": response.text}), response.status_code

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

@app.route('/webhook3', methods=['POST'])
def webhook3():
    if request.method == 'POST':
        try:
            webhook_data = request.get_json()
            print("Received webhook data:", webhook_data)  # Debugging: Print received data

            # Extract board ID and item ID from the webhook (adapt to your webhook's structure)
            board_id = webhook_data.get('event', {}).get('boardId', {})
            item_id = webhook_data.get('event', {}).get('pulseId', {})
            pulse_name = webhook_data.get('event', {}).get('pulseName', {})
            pulse_json = jsonify(pulse_name)
            print("Pulse:", pulse_name)

            if isinstance(pulse_name, str):
                 pulse_name = pulse_name.replace('"', '\\"')

            if not board_id:
                print("Error: Could not extract board_id or item_id from webhook.")
                return jsonify({"error": "Missing board_id or item_id in webhook"}), 400

            # Information you want to send back to Monday.com (Column X)
             # Replace with the actual value

            # Construct the GraphQL mutation to update the column
            headers = {"Authorization": API_KEY, "Content-Type": "application/json"}



            query = f'mutation{{ change_simple_column_value (item_id: {item_id},board_id: {board_id}, column_id: "texto_1_mkn58839", value: "{pulse_name}") {{ id }} }}'
            data = {'query': query}




            response = requests.post(url=API_URL, json=data, headers=headers)

            if response.status_code == 200:
                print("Successfully updated Monday.com column:", response.json())
                return jsonify({"status": "success", "message": "Column updated"}), 200
            else:
                print(f"Error updating Monday.com column: {response.status_code} - {response.text}")
                return jsonify({"error": "Failed to update column", "monday_response": response.text}), response.status_code

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
