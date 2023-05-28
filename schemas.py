from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class DecisionsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(
        PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(
        PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data) -> FileStorage:
        if value is None:
            None
        if not isinstance(value, FileStorage):
            self.fail("invalid")

        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)


class ParcelSchema(Schema):
    id = fields.Str(dump_only=True)
    uid = fields.Str(required=True)
    pci_area = fields.Float(required=True)
    city_code = fields.Str(required=True)
