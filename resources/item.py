from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="wajib"
    )

    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Store ID Wajib"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {'message': 'Item not found'}, 404


    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "an name '{}' has been exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except TypeError as e:
            print(e)
            return {'message': "gagal"}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Oke delete"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['name']

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    @jwt_required()
    def get(self):
        return {
            'items': [ x.json() for x in ItemModel.query.all() ]
        }
