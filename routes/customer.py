from flask import jsonify, request

from app import app, connection, text, render_template


@app.route('/admin/customer')
def indexCustomer():
    return render_template(
        'admin/customer/index.html',
        module='customer',
    )


@app.route('/api/customer')
def getAllCustomer():
    result = connection.execute(text("SELECT * FROM customer"))
    customer_arr = []
    for item in result:
        customer_arr.append({
            'id': item.id,
            'name': item.name,
            'image': item.image,
            'status': item.status,
        })
    return jsonify(customer_arr)


@app.route('/api/customer', methods=['POST'])
def addCustomer():
    try:
        data = request.get_json()

        # Retrieve data from the request JSON
        name = data.get('name')
        image = data.get('image')
        status = data.get('status')

        # Perform the database insertion
        result = connection.execute(
            text("INSERT INTO customer (name, image, status) VALUES (:name, :image, :status)"),
            {'name': name, 'image': image, 'status': status}
        )

        # Get the ID of the newly inserted record
        new_customer_id = result.lastrowid

        # Fetch the newly added customer for response
        new_customer = connection.execute(
            text("SELECT * FROM customer WHERE id = :id"),
            {'id': new_customer_id}
        ).fetchone()

        # Construct the response data
        response_data = {
            'id': new_customer.id,
            'name': new_customer.name,
            'image': new_customer.image,
            'status': new_customer.status,
        }

        return jsonify(response_data), 201  # HTTP status code 201 indicates successful resource creation

    except Exception as e:
        # Handle any exceptions that might occur during the process
        return jsonify({'error': str(e)}), 500  # Internal Server Error


@app.route('/api/customer/<int:id>', methods=['DELETE'])
def deleteCustomer(id):
    try:
        # Delete the category from the database based on the provided ID
        connection.execute(text("DELETE FROM customer WHERE id = :id"), {'id': id})
        return jsonify({'success': True, 'message': 'Category deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/customer/<int:id>', methods=['PUT'])
def editCustomer(id):
    try:
        data = request.get_json()

        # Retrieve data from the request JSON
        new_name = data.get('name')
        new_image = data.get('image')
        new_status = data.get('status')
        # Retrieve other fields as needed

        # Perform the database update
        connection.execute(
            text("UPDATE customer SET name = :name, image = :image, status = :status WHERE id = :id"),
            {'name': new_name, 'image': new_image, 'status': new_status, 'id': id}
        )

        # Fetch the updated customer for response
        updated_customer = connection.execute(
            text("SELECT * FROM customer WHERE id = :id"),
            {'id': id}
        ).fetchone()

        # Construct the response data
        response_data = {
            'id': updated_customer.id,
            'name': updated_customer.name,
            'image': updated_customer.image,
            'status': updated_customer.status,
            # Include other fields as needed
        }

        return jsonify(response_data), 200  # HTTP status code 200 indicates success

    except Exception as e:
        # Handle any exceptions that might occur during the process
        return jsonify({'error': str(e)}), 500  # Internal Server Error
