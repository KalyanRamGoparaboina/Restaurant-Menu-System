import io
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
db = client['restaurant']  # Your database name
tablebook_collection = db['tablebook'] 
contact_collection = db['contact']
orders_collection = db['orders']

# Routes for main pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

# Routes for menu items
@app.route('/food')
def food():
    return render_template('food.html')  # Tomato Soup

@app.route('/vegsoup')
def vegsoup():
    return render_template('vegsoup.html')  # Veg Soup

@app.route('/chickensoup')
def chickensoup():
    return render_template('chickensoup.html') 

@app.route('/specialChickenBiryani')
def specialChickenBiryani():
    return render_template('specialChickenBiryani.html')  
@app.route('/dum')
def dum():
    return render_template('dum.html')  # Dum Biryani

@app.route('/eggbiryani')
def eggbiryani():
    return render_template('eggbiryani.html')  # Egg Biryani

@app.route('/muttonBiryanii')
def muttonBiryanii():
    return render_template('muttonBiryanii.html')  # Mutton Biryani

@app.route('/prawns')
def prawns():
    return render_template('prawns.html')  # Prawns Biryani

@app.route('/vegBiryani')
def vegBiryani():
    return render_template('vegBiryani.html')  # Veg Biryani

@app.route('/paneer')
def paneer():
    return render_template('paneer.html')  # Paneer Biryani

@app.route('/mushroom')
def mushroom():
    return render_template('mushroom.html')  # Mushroom Biryani

@app.route('/ChocolateStrawberryCrumble')
def ChocolateStrawberryCrumble():
    return render_template('Chocolate Strawberry-Crumble.html')  # Chocolate Strawberry-Crumble

@app.route('/RedVelVetCake')
def RedVelVetCake():
    return render_template('RedVelVetCake.html')  # Red Velvet Cake

@app.route('/gulab')
def gulab():
    return render_template('gulab.html')  # Gulab Jamun

@app.route('/orders')
def orders():
    return render_template('orders.html') 
@app.route('/dragonChicken')
def dragonChicken():
    return render_template('dragonChicken.html')  # Dragon Chicken

@app.route('/PaneerTikka')
def PaneerTikka():
    return render_template('Paneer Tikka.html')  

@app.route('/veg')
def veg():
    return render_template('veg.html')  



@app.route('/qr')
def qr():
    return render_template('qr.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    # Retrieve form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    booking_datetime = request.form['booking_datetime']
    number_of_people = request.form['number_of_people']
    email = request.form['email']
    phone = request.form['phone']
    food_orders = request.form.getlist('food_order')

    # Create a reservation document
    reservation = {
        'first_name': first_name,
        'last_name': last_name,
        'booking_datetime': booking_datetime,
        'number_of_people': number_of_people,
        'email': email,
        'phone': phone,
        'food_orders': food_orders
    }

    # Insert reservation into MongoDB
    tablebook_collection.insert_one(reservation)

    # Create a text file with reservation details
    text_content = f"""
    Reservation Details:
    First Name: {first_name}
    Last Name: {last_name}
    Booking DateTime: {booking_datetime}
    Number of People: {number_of_people}
    Email: {email}
    Phone: {phone}
    Food Orders: {', '.join(food_orders)}
    """

    output = io.BytesIO(text_content.encode())
    output.seek(0)

    return send_file(output, mimetype='text/plain', as_attachment=True, download_name='reservation.txt')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/confirmation')
def confirmation():
    return render_template('paymentconfirm.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    # Extract form data
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    # Store form data in MongoDB
    data = {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    }
    contact_collection.insert_one(data)
    return redirect(url_for('contacts'))



@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        order_data = request.json

        # Extract data from the request
        user_details = order_data.get('userDetails')
        order_items = order_data.get('orderItems')
        total_cost = order_data.get('totalCost')
        payment_method = order_data.get('paymentMethod')

        # Store the order in MongoDB
        order_document = {
            'user_details': user_details,
            'order_items': order_items,
            'total_cost': total_cost,
            'payment_method': payment_method
        }

        orders_collection.insert_one(order_document)

        return jsonify({'success': True})

    return render_template('payment.html')
    
    

if __name__ == "__main__":
    app.run(debug=True)

    
