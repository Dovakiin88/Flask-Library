from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Inventory, invens_schema, inven_schema

api= Blueprint('api', __name__, url_prefix= '/api')

#adds book to the database
@api.route('/stock', methods= ['POST'])
@token_required
def add_book(current_user_token):
    author= request.json['author']
    title= request.json['title']
    genre= request.json['genre']
    isbn= request.json['isbn']
    copies= request.json['copies']
    user_token= current_user_token.token

    print(f'TEST: {current_user_token.token}')

    book= Inventory(author, title, genre, isbn, copies, user_token= user_token)

    db.session.add(book)
    db.session.commit()

    response= inven_schema.dump(book)
    return jsonify(response)

@api.route('/stock', methods= ['GET'])
@token_required
def get_item(current_user_token):
    a_user= current_user_token.token
    items= Inventory.query.filter_by(user_token= a_user).all()
    response= invens_schema.dump(items)
    return jsonify(response)

#updates the books
@api.route('/item/<id>', methods= ['POST', 'PUT'])
@token_required
def update_stock(current_user_token, id):
    books= Inventory.query.get(id)
    books.author= request.json['author']
    books.title= request.json['title']
    books.genre= request.json['genre']
    books.isbn= request.json['isnb']
    books.copies= request.json['copies']
    books.user_token= current_user_token.token

    db.session.commit()
    response= inven_schema.dump(books)
    return jsonify(response)

#delete book from library
@api.route('/items/<id>', methods= ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book= Inventory.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response= inven_schema.dump(book)
    return jsonify(response)
    


