from apiflask import Schema, fields


class TranslationSchema(Schema):
    language = fields.String(required=True)
    title = fields.String(required=True)
    message = fields.String(required=True)


class SendSchema(Schema):
    title = fields.String(required=True)
    message = fields.String(required=True)
    name = fields.String()
    image = fields.String()
    action = fields.String()
    scheduled_at = fields.DateTime()
    repeat = fields.Boolean()
    repeat_interval = fields.Integer()
    recipients = fields.String()
    translations = fields.List(fields.Nested(TranslationSchema))


class SendOutputSchema(Schema):
    id = fields.Integer()
    hash = fields.String()
    name = fields.String()
    default_title = fields.String()
    default_message = fields.String()
    image = fields.String()
    action = fields.String()
    recipients = fields.List(fields.String())
    translations = fields.List(fields.Nested(TranslationSchema))
    repeat = fields.Boolean()
    repeat_interval = fields.Integer()
    delivered = fields.Boolean()
    delivery_percentage = fields.Integer()
    sent = fields.Boolean()
    live = fields.Boolean()
    scheduled = fields.Boolean()
    scheduled_at = fields.DateTime()
    created_at = fields.DateTime()


class ValueSchema(Schema):
    key = fields.String(required=True)
    value = fields.String(required=True)


class EventSchema(Schema):
    event = fields.String(required=True)
