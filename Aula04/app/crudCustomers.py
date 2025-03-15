from flask import Flask, request, jsonify
import Util.bd as bd
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/customers', methods=['POST'])
def create_customer():
    app.logger.info('POST request to /customers')
    data = request.get_json()
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO customers (customer_id, company_name, contact_name, contact_title, adress, city, region, postal_code, country, phone, fax)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data['customer_id'], data['company_name'], data.get('contact_name'), data.get('contact_title'), data.get('adress'), data.get('city'), data.get('region'), data.get('postal_code'), data.get('country'), data.get('phone'), data.get('fax'))
        )
        conn.commit()
        return jsonify({"message": "Customer created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
        
@app.route('/customers', methods=['GET'])
def list_customers():
    app.logger.info('GET request to /customers')
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        if not customers:
            return jsonify({"error": "No customers found"}), 404
        return jsonify(
            [
                {
                    "customer_id": customer[0],
                    "company_name": customer[1],
                    "contact_name": customer[2],
                    "contact_title": customer[3],
                    "adress": customer[4],
                    "city": customer[5],
                    "region": customer[6],
                    "postal_code": customer[7],
                    "country": customer[8],
                    "phone": customer[9],
                    "fax": customer[10]
                } for customer in customers
            ]
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/customers/<int:customer_id>', methods=['GET'])
def read_customer(customer_id):
    app.logger.info(f'GET request to /customers/{customer_id}')
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if customer is None:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify({
            "customer_id": customer[0],
            "company_name": customer[1],
            "contact_name": customer[2],
            "contact_title": customer[3],
            "adress": customer[4],
            "city": customer[5],
            "region": customer[6],
            "postal_code": customer[7],
            "country": customer[8],
            "phone": customer[9],
            "fax": customer[10]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    app.logger.info(f'PUT request to /customers/{customer_id}')
    data = request.get_json()
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE customers
            SET company_name = %s, contact_name = %s, contact_title = %s, adress = %s, city = %s, region = %s, postal_code = %s, country = %s, phone = %s, fax = %s
            WHERE customer_id = %s
            """,
            (data['company_name'], data.get('contact_name'), data.get('contact_title'), data.get('adress'), data.get('city'), data.get('region'), data.get('postal_code'), data.get('country'), data.get('phone'), data.get('fax'), customer_id)
        )
        conn.commit()
        return jsonify({"message": "Customer updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    app.logger.info(f'DELETE request to /customers/{customer_id}')
    conn = bd.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        conn.commit()
        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)