from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id', type=int,
                        required=True,
                        help="Each item must have a store id!"
                        )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message' : 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return { 'message' : "An item with name '{}' already exists.".format(name)}, 400 # request error

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message" : "an error occurred inserting the item."}, 500 #internal server error
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message' : 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name, data['price'])
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        #return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items' : list (map(lambda x: x.json(), ItemModel.query.all()))}
        # connection =  sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "select name,price from items"
        # result = cursor.execute(query)
        #
        # items=[]
        # for row in result:
        #     items.append(ItemModel(*row).json())
        # connection.close()
        # return {'items': items}
