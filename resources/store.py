from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {'message': 'Store not found'}, 404


    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "an name '{}' has been exists".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except TypeError as e:
            print(e)
            return {'message': "gagal"}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Oke delete"}


class StoreList(Resource):

    @jwt_required()
    def get(self):
        return {
            'store': [ store.json() for store in StoreModel.query.all() ]
        }
