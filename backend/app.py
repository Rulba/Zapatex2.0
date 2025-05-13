from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db = SQLAlchemy(app)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer)
    sucursal = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock')
def get_stock():
    stock = Stock.query.all()
    return jsonify([{
        'producto': f'Producto {item.producto_id}',
        'sucursal': item.sucursal,
        'cantidad': item.cantidad,
        'precio': item.precio
    } for item in stock])

@app.route('/venta', methods=['POST'])
def vender():
    data = request.json
    sucursal = Stock.query.filter_by(sucursal=data['sucursal_id'], producto_id=data['producto_id']).first()
    if sucursal and sucursal.cantidad >= data['cantidad']:
        sucursal.cantidad -= data['cantidad']
        db.session.commit()
        return jsonify({'mensaje': 'Venta realizada'})
    return jsonify({'mensaje': 'Stock insuficiente'}), 400

if __name__ == '__main__':
    app.run(debug=True)
