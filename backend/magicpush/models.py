import jwt
import uuid
import datetime
from flask_login import UserMixin

from magicpush import db
from magicpush.helpers.encryption import Encryption


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)
    email_verified = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.DateTime)
    password = db.Column(db.String)
    business_name = db.Column(db.String)
    country = db.Column(db.String)
    website_url = db.Column(db.String)
    vat_number = db.Column(db.String)
    referral_hash = db.Column(db.String)
    access_level = db.Column(db.Integer, default=0)  # 0 = free, 1 = pro, 2 = pro+
    play_subscription_id = db.Column(db.String)
    play_purchase_token = db.Column(db.String)
    stripe_subscription_id = db.Column(db.String)
    stripe_customer_id = db.Column(db.String)
    lemonsqueezy_customer_id = db.Column(db.String)
    lemonsqueezy_subscription_id = db.Column(db.String)
    subscription_status = db.Column(db.String)
    has_purchased_deal = db.Column(db.Boolean, default=False)
    has_active_subscription = db.Column(db.Boolean, default=False)
    banned = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    early_access = db.Column(db.Boolean, default=False)
    last_active_at = db.Column(db.DateTime)
    last_billed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.last_active_at = datetime.datetime.utcnow()
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'name': self.name,
            'email': self.email,
            'email_verified': self.email_verified,
            'business_name': self.business_name,
            'country': self.country,
            'website_url': self.website_url,
            'vat_number': self.vat_number,
            'has_purchased_deal': self.has_purchased_deal if self.has_purchased_deal else False,
            'has_active_subscription': self.has_active_subscription,
            'is_admin': self.is_admin if self.is_admin else False,
            'last_active_at': self.last_active_at.isoformat() if self.last_active_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class App(db.Model):
    __tablename__ = 'apps'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    icon = db.Column(db.String)
    name = db.Column(db.String)
    languages = db.Column(db.Integer, default=1)
    has_ios = db.Column(db.Boolean, default=False)
    has_android = db.Column(db.Boolean, default=False)
    has_web = db.Column(db.Boolean, default=False)
    apple_key_file = db.Column(db.String)
    apple_key_id = db.Column(db.String)
    apple_team_id = db.Column(db.String)
    apple_bundle_id = db.Column(db.String)
    firebase_service_account_file = db.Column(db.String)
    hms_package_name = db.Column(db.String)
    hms_app_id = db.Column(db.String)
    hms_client_secret = db.Column(db.String)
    website_url = db.Column(db.String)
    widget_color = db.Column(db.String, default='#8b5cf6')
    vapid_public_key = db.Column(db.String)
    vapid_private_key = db.Column(db.String)
    api_key = db.Column(db.String)
    events = db.relationship('AppEvent')
    keys = db.relationship('AppUserKey')
    notification_groups = db.Column(db.String, default='functional,marketing')
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.last_active_at = datetime.datetime.utcnow()

        private_key_pem, public_key_pem = Encryption.generate_vapid_keys()
        self.vapid_public_key = public_key_pem
        self.vapid_private_key = private_key_pem

        self.created_at = datetime.datetime.utcnow()

    # get all available languages using bitwise and operator and turn into readable list of ISO codes
    def get_languages(self):
        lst = []
        if self.languages:
            if self.languages & 1:
                lst.append('en')
            if self.languages & 2:
                lst.append('nl')
            if self.languages & 4:
                lst.append('fr')
            if self.languages & 8:
                lst.append('de')
            if self.languages & 16:
                lst.append('es')
            if self.languages & 32:
                lst.append('it')
            if self.languages & 64:
                lst.append('pt')
            if self.languages & 128:
                lst.append('pl')
            if self.languages & 256:
                lst.append('ru')
            if self.languages & 512:
                lst.append('tr')
            if self.languages & 1024:
                lst.append('ar')
            if self.languages & 2048:
                lst.append('zh')
            if self.languages & 4096:
                lst.append('ja')
            if self.languages & 8192:
                lst.append('ko')
            if self.languages & 16384:
                lst.append('hi')
            if self.languages & 32768:
                lst.append('th')
            if self.languages & 65536:
                lst.append('vi')
            if self.languages & 131072:
                lst.append('id')
            if self.languages & 262144:  # Next binary flag value
                lst.append('cs')  # Czech
            if self.languages & 524288:
                lst.append('sv')  # Swedish
            if self.languages & 1048576:
                lst.append('fi')  # Finnish
            if self.languages & 2097152:
                lst.append('da')  # Danish
            if self.languages & 4194304:
                lst.append('no')  # Norwegian
            if self.languages & 8388608:
                lst.append('hu')  # Hungarian
        else:
            lst.append('en')
        return lst

    # set languages using bitwise or operator
    def set_languages(self, languages):
        self.languages = 0
        for language in languages:
            if language == 'en':
                self.languages |= 1
            if language == 'nl':
                self.languages |= 2
            if language == 'fr':
                self.languages |= 4
            if language == 'de':
                self.languages |= 8
            if language == 'es':
                self.languages |= 16
            if language == 'it':
                self.languages |= 32
            if language == 'pt':
                self.languages |= 64
            if language == 'pl':
                self.languages |= 128
            if language == 'ru':
                self.languages |= 256
            if language == 'tr':
                self.languages |= 512
            if language == 'ar':
                self.languages |= 1024
            if language == 'zh':
                self.languages |= 2048
            if language == 'ja':
                self.languages |= 4096
            if language == 'ko':
                self.languages |= 8192
            if language == 'hi':
                self.languages |= 16384
            if language == 'th':
                self.languages |= 32768
            if language == 'vi':
                self.languages |= 65536
            if language == 'id':
                self.languages |= 131072
            if language == 'cs':
                self.languages |= 262144
            if language == 'sv':
                self.languages |= 524288
            if language == 'fi':
                self.languages |= 1048576
            if language == 'da':
                self.languages |= 2097152
            if language == 'no':
                self.languages |= 4194304
            if language == 'hu':
                self.languages |= 8388608

    def get_default_events(self):
        return [
            'subscribed'
        ]

    def get_default_keys(self):
        return [
            {'name': 'current_date', 'type': 'date'},
            {'name': 'user.created_at', 'type': 'date'}
        ]

    def to_json(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'icon': self.icon,
            'name': self.name,
            'languages': self.get_languages(),
            'has_web': self.has_web,
            'has_ios': self.has_ios,
            'has_android': self.has_android,
            'apple_key_file': self.apple_key_file,
            'apple_key_id': self.apple_key_id,
            'apple_team_id': self.apple_team_id,
            'apple_bundle_id': self.apple_bundle_id,
            'firebase_service_account_file': self.firebase_service_account_file,
            'hms_package_name': self.hms_package_name,
            'hms_app_id': self.hms_app_id,
            'hms_client_secret': self.hms_client_secret,
            'website_url': self.website_url,
            'widget_color': self.widget_color if self.widget_color else '#8b5cf6',
            'vapid_public_key': self.vapid_public_key,
            'vapid_private_key': self.vapid_private_key,
            'api_key': self.api_key,
            'default_events': self.get_default_events(),
            'events': [event.to_json() for event in self.events],
            'default_keys': self.get_default_keys(),
            'keys': [key.to_json() for key in self.keys],
            'notification_groups': self.notification_groups.split(',') if self.notification_groups else [],
            'last_active_at': self.last_active_at.isoformat() if self.last_active_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class AppEvent(db.Model):
    __tablename__ = 'app_events'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }


class AppUserKey(db.Model):
    __tablename__ = 'app_user_variables'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    key = db.Column(db.String)
    type = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'name': self.key,
            'type': self.type,
        }


class AppUser(db.Model):
    __tablename__ = 'app_users'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    hash = db.Column(db.String)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    app = db.relationship('App')
    fcm_token = db.Column(db.String)
    apn_device_token = db.Column(db.String)
    web_push_endpoint = db.Column(db.String)
    web_push_auth = db.Column(db.String)
    web_push_p256dh = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    language = db.Column(db.String)
    notification_groups = db.Column(db.String, default='functional,marketing')
    subscribed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'hash': self.hash,
            'app_hash': self.app.hash if self.app else None,
            'language': self.language,
            'notification_groups': self.notification_groups.split(',') if self.notification_groups else [],
            'created_at': self.created_at.isoformat()
        }


class AppUserNotification(db.Model):
    __tablename__ = 'app_user_notifications'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    app_user_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))
    delivered = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=1)
    response = db.Column(db.String)
    delivered_at = db.Column(db.DateTime)
    clicked_at = db.Column(db.DateTime)
    last_sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.last_sent_at = datetime.datetime.utcnow()
        self.created_at = datetime.datetime.utcnow()


class AppUserValue(db.Model):
    __tablename__ = 'app_user_values'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    app_user_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    key = db.Column(db.String)
    value = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'key': self.key,
            'value': self.value,
            'created_at': self.created_at.isoformat()
        }


class ActiveFlow(db.Model):
    __tablename__ = 'active_flows'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    app_user_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    flow_id = db.Column(db.Integer, db.ForeignKey('flows.id'))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()


class DelayedFlowEvent(db.Model):
    __tablename__ = 'delayed_flow_events'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    active_flow_id = db.Column(db.Integer, db.ForeignKey('active_flows.id'))
    flow_event_id = db.Column(db.Integer, db.ForeignKey('flow_event.id'))
    delay = db.Column(db.Integer)
    delay_unit = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()


class CompletedFlowEvent(db.Model):
    __tablename__ = 'completed_flow_events'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    active_flow_id = db.Column(db.Integer, db.ForeignKey('active_flows.id'))
    flow_event_id = db.Column(db.Integer, db.ForeignKey('flow_event.id'))
    next_flow_event_id = db.Column(db.Integer, db.ForeignKey('flow_event.id'))
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))
    name = db.Column(db.String)
    default_title = db.Column(db.String)
    default_message = db.Column(db.String)
    action = db.Column(db.String)
    image = db.Column(db.String)
    recipients = db.Column(db.String)
    translations = db.relationship('NotificationTranslation')
    user_notifications = db.relationship('AppUserNotification')
    repeat = db.Column(db.Boolean, default=False)
    repeat_interval = db.Column(db.String)
    delivered = db.Column(db.Boolean, default=False)
    sent = db.Column(db.Boolean, default=False)  # if sent directly from notifications
    live = db.Column(db.Boolean, default=False)  # for in the flow
    flow_notification = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=1)
    scheduled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        delivery_percentage = 0
        if self.user_notifications:
            delivered = 0
            for user_notification in self.user_notifications:
                if user_notification.delivered:
                    delivered += 1
            delivery_percentage = (delivered / len(self.user_notifications)) * 100

        return {
            'id': self.id,
            'hash': self.hash,
            'name': self.name,
            'default_title': self.default_title,
            'default_message': self.default_message,
            'image': self.image,
            'action': self.action,
            'recipients': self.recipients.split(',') if self.recipients else [],
            'translations': [translation.to_json() for translation in self.translations],
            'repeat': self.repeat,
            'repeat_interval': self.repeat_interval,
            'delivered': self.delivered,
            'delivery_percentage': delivery_percentage,
            'sent': self.sent if self.sent else False,
            'live': self.live if self.live else False,
            'scheduled': self.scheduled_at is not None,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'created_at': self.created_at.isoformat()
        }


class NotificationTranslation(db.Model):
    __tablename__ = 'notification_translations'
    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))
    language = db.Column(db.String)
    title = db.Column(db.String)
    message = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'language': self.language,
            'title': self.title,
            'message': self.message,
            'image': self.image,
            'created_at': self.created_at.isoformat()
        }


class NotificationConversion(db.Model):
    __tablename__ = 'notification_conversions'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))


class Flow(db.Model):
    __tablename__ = 'flows'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    name = db.Column(db.String)
    event = db.Column(db.String)  # when flow is activated
    enabled = db.Column(db.Boolean, default=False)  # if flow is active
    one_time = db.Column(db.Boolean, default=False)  # if flow is one time
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'app_id': self.app_id,
            'hash': self.hash,
            'name': self.name,
            'event': self.event,
            'enabled': self.enabled,
            'one_time': self.one_time,
            'created_at': self.created_at.isoformat()
        }


class FlowEvent(db.Model):
    __tablename__ = 'flow_event'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String)
    flow_id = db.Column(db.Integer, db.ForeignKey('flows.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('flow_event.id'))
    loop_back_to_event_id = db.Column(db.Integer)
    type = db.Column(db.String)  # Delay, Notification, Yes/No condition, End
    delay = db.Column(db.Integer)  # in days
    delay_unit = db.Column(db.String)  # days, hours, minutes
    key_id = db.Column(db.Integer)  # key to check for condition
    value_id = db.Column(db.Integer)  # value to check for condition
    statement = db.Column(db.String)  # if statement is true, event is triggered
    is_yes = db.Column(db.Boolean, default=False)  # if statement is true, is it a yes or no
    is_no = db.Column(db.Boolean, default=False)  # if statement is true, is it a yes or no
    is_start = db.Column(db.Boolean, default=False)  # if event is start of flow
    notification = db.relationship('Notification')
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))  # notification to send
    events = db.relationship('FlowEvent')  # from parent_id
    order_id = db.Column(db.Integer)  # order of events in flow
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.hash = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'type': self.type,
            'loop_back_to_event_id': self.loop_back_to_event_id,
            'delay': self.delay,
            'delay_unit': self.delay_unit,
            'statement': self.statement,
            'is_yes': self.is_yes,
            'is_no': self.is_no,
            'notification': self.notification.to_json() if self.notification else None,
            'notification_id': self.notification_id,
            'events': [event.to_json() for event in self.events],
            'order_id': self.order_id,
            'created_at': self.created_at.isoformat()
        }
