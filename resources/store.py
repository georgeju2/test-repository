from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_id', type=int,
                        required=True,
                        help="Each item must have a store id!"
                        )
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message' : 'Store not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message', 'A store with name {} already exist.'.format(name)}, 400
        data = Store.parser.parse_args()
        print (data)
        store =StoreModel(name, data['store_id'])
        try:
            store.save_to_db()
        except:
            return {'message' : 'An error occurred while creating the store.'}, 500

        return store.json(), 201  # crea`ted


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message' : "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {'stores' : [store.json() for store in StoreModel.query.all()]}
