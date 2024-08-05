from magicpush import app, celery_app
from magicpush.helpers.apn import Apn
from magicpush.helpers.fcm import Fcm
from magicpush.helpers.encryption import Encryption
from magicpush.helpers.stripe_billing import StripeBilling
from magicpush.models import (User, App, AppUser, AppUserKey, AppUserValue, AppUserNotification, Flow, FlowEvent,
                              Notification, ActiveFlow, CompletedFlowEvent, DelayedFlowEvent)

import json
import datetime
from sqlalchemy import or_, and_, cast, Date
from magicpush.helpers.pywebpushv2 import webpush
from dateutil.relativedelta import relativedelta

apn = Apn()
fcm = Fcm()
stripe = StripeBilling()


@celery_app.task()
def schedule_notifications():
    from magicpush.database import db_session
    try:
        notifications = db_session.query(Notification)\
            .filter(Notification.flow_notification == False, Notification.repeat == True)\
            .all()
        for notification in notifications:
            repeat_interval = notification.repeat_interval

            last_notification = db_session.query(Notification)\
                .filter(Notification.app_id == notification.app_id)\
                .filter(Notification.parent_id == notification.id)\
                .order_by(Notification.scheduled_at.desc())\
                .first()

            if repeat_interval == 'daily':
                # schedule the next 365 days of notifications
                for i in range(365):
                    schedule_at = notification.scheduled_at + datetime.timedelta(days=i)

                    if last_notification is not None and schedule_at <= last_notification.scheduled_at:
                        continue

                    # check if notification already exists
                    existing_notification = db_session.query(Notification)\
                        .filter(Notification.app_id == notification.app_id)\
                        .filter(Notification.parent_id == notification.id)\
                        .filter(Notification.scheduled_at == schedule_at)\
                        .first()
                    if existing_notification is not None:
                        continue

                    new_notification = Notification()
                    new_notification.app_id = notification.app_id
                    new_notification.parent_id = notification.id
                    new_notification.name = notification.name
                    new_notification.image = notification.image
                    new_notification.scheduled_at = notification.scheduled_at + datetime.timedelta(days=i)
                    new_notification.repeat = notification.repeat
                    new_notification.repeat_interval = notification.repeat_interval
                    db_session.add(new_notification)
                    db_session.commit()
            elif repeat_interval == 'weekly':
                # schedule next 52 weeks of notifications
                for i in range(52):
                    schedule_at = notification.scheduled_at + datetime.timedelta(weeks=i)

                    if last_notification is not None and schedule_at <= last_notification.scheduled_at:
                        continue

                    # check if notification already exists
                    existing_notification = db_session.query(Notification)\
                        .filter(Notification.app_id == notification.app_id)\
                        .filter(Notification.parent_id == notification.id)\
                        .filter(Notification.scheduled_at == schedule_at)\
                        .first()
                    if existing_notification is not None:
                        continue

                    new_notification = Notification()
                    new_notification.app_id = notification.app_id
                    new_notification.parent_id = notification.id
                    new_notification.name = notification.name
                    new_notification.image = notification.image
                    new_notification.scheduled_at = notification.scheduled_at + datetime.timedelta(weeks=i)
                    new_notification.repeat = notification.repeat
                    new_notification.repeat_interval = notification.repeat_interval
                    db_session.add(new_notification)
                    db_session.commit()
            elif repeat_interval == 'monthly':
                # schedule next 12 months of notifications
                for i in range(12):
                    schedule_at = notification.scheduled_at + relativedelta(months=+i)

                    if last_notification is not None and schedule_at <= last_notification.scheduled_at:
                        continue

                    # check if notification already exists
                    existing_notification = db_session.query(Notification)\
                        .filter(Notification.app_id == notification.app_id)\
                        .filter(Notification.parent_id == notification.id)\
                        .filter(Notification.scheduled_at == schedule_at)\
                        .first()
                    if existing_notification is not None:
                        continue

                    new_notification = Notification()
                    new_notification.app_id = notification.app_id
                    new_notification.parent_id = notification.id
                    new_notification.name = notification.name
                    new_notification.image = notification.image
                    new_notification.scheduled_at = notification.scheduled_at + relativedelta(months=+i)
                    new_notification.repeat = notification.repeat
                    new_notification.repeat_interval = notification.repeat_interval
                    db_session.add(new_notification)
                    db_session.commit()
            elif repeat_interval == 'yearly':
                # schedule next 5 years of notifications
                for i in range(5):
                    schedule_at = notification.scheduled_at + relativedelta(years=+i)

                    if last_notification is not None and schedule_at <= last_notification.scheduled_at:
                        continue

                    # check if notification already exists
                    existing_notification = db_session.query(Notification)\
                        .filter(Notification.app_id == notification.app_id)\
                        .filter(Notification.parent_id == notification.id)\
                        .filter(Notification.scheduled_at == schedule_at)\
                        .first()
                    if existing_notification is not None:
                        continue

                    new_notification = Notification()
                    new_notification.app_id = notification.app_id
                    new_notification.parent_id = notification.id
                    new_notification.name = notification.name
                    new_notification.image = notification.image
                    new_notification.scheduled_at = notification.scheduled_at + relativedelta(years=+i)
                    new_notification.repeat = notification.repeat
                    new_notification.repeat_interval = notification.repeat_interval
                    db_session.add(new_notification)
                    db_session.commit()
        db_session.close()
    except Exception as e:
        app.logger.exception('Schedule Notifications: {}'.format(e))
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()

@celery_app.task()
def notifier():
    from magicpush.database import db_session
    try:
        notifications = db_session.query(Notification)\
            .filter(Notification.flow_notification == False, Notification.delivered == False,
                    Notification.sent == True)\
            .filter(or_(and_(Notification.scheduled_at == None, cast(Notification.created_at, Date) == datetime.datetime.utcnow().date()),
                        and_(Notification.scheduled_at != None, Notification.scheduled_at <= datetime.datetime.utcnow())))\
            .all()

        for notification in notifications:
            if (notification.scheduled_at is not None
                    and notification.scheduled_at.date() != datetime.datetime.utcnow().date()):
                continue

            selected_app = db_session.query(App).filter(App.id == notification.app_id).first()

            filters = []
            if notification.recipients is not None and notification.recipients != 'all':
                filters.append(AppUser.hash.in_(notification.recipients.split(',')))

            app_users = db_session.query(AppUser) \
                .filter(AppUser.app_id == notification.app_id, AppUser.created_at <= notification.created_at) \
                .filter(or_(AppUser.web_push_endpoint != None, AppUser.fcm_token != None,
                            AppUser.apn_device_token != None))\
                .filter(*filters) \
                .all()

            for app_user in app_users:
                send_push_notification(db_session, selected_app, app_user, notification)

            notified_users = db_session.query(AppUserNotification) \
                .join(AppUser, AppUserNotification.app_user_id == AppUser.id) \
                .filter(AppUserNotification.notification_id == notification.id, AppUserNotification.delivered == True) \
                .group_by(AppUserNotification.id, AppUserNotification.app_user_id) \
                .count()
            if notified_users >= len(app_users):
                # all users have been notified
                notification.delivered = True
                db_session.commit()

        db_session.close()
    except Exception as e:
        app.logger.exception('Notifier: {}'.format(e))
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()

@celery_app.task()
def send_push(notification_id):
    from magicpush.database import db_session
    try:
        notification = db_session.query(Notification)\
            .filter(Notification.id == notification_id, Notification.delivered == False, Notification.sent == True) \
            .filter(or_(Notification.scheduled_at == None, Notification.scheduled_at <= datetime.datetime.utcnow())) \
            .first()
        if notification is None:
            return

        if (notification.scheduled_at is not None
                and Notification.scheduled_at.date() != datetime.datetime.utcnow().date()):
            return

        selected_app = db_session.query(App).filter(App.id == notification.app_id).first()
        if selected_app is None:
            return

        filters = []
        if notification.recipients is not None and notification.recipients != 'all':
            filters.append(AppUser.hash.in_(notification.recipients.split(',')))

        app_users = db_session.query(AppUser)\
            .filter(AppUser.app_id == notification.app_id)\
            .filter(or_(AppUser.web_push_endpoint != None, AppUser.fcm_token != None, AppUser.apn_device_token != None))\
            .filter(*filters)\
            .all()

        for app_user in app_users:
            send_push_notification(db_session, selected_app, app_user, notification)

        notified_users = db_session.query(AppUserNotification)\
            .join(AppUser, AppUserNotification.app_user_id == AppUser.id)\
            .filter(AppUserNotification.notification_id == notification.id, AppUserNotification.delivered == True)\
            .group_by(AppUserNotification.id, AppUserNotification.app_user_id)\
            .count()
        if notified_users >= len(app_users):
            # all users have been notified
            notification.delivered = True
            db_session.commit()

        db_session.close()
    except Exception as e:
        app.logger.exception('Send Push: {}'.format(e))
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()

@celery_app.task()
def run_flow():
    from magicpush.database import db_session
    try:
        active_flows = db_session.query(ActiveFlow).all()
        for active_flow in active_flows:
            selected_flow = db_session.query(Flow).filter(Flow.id == active_flow.flow_id, Flow.enabled == True).first()
            if selected_flow is None:
                continue

            completed_events = db_session.query(CompletedFlowEvent)\
                .filter(CompletedFlowEvent.active_flow_id == active_flow.id)\
                .all()
            completed_event_ids = [completed_event.flow_event_id for completed_event in completed_events]

            events = db_session.query(FlowEvent)\
                .filter(FlowEvent.flow_id == selected_flow.id, FlowEvent.parent_id == None)\
                .all()
            for event in events:
                parse_event(db_session, active_flow, selected_flow, completed_event_ids, event)

        db_session.close()
    except Exception as e:
        app.logger.exception('Run Flow: {}'.format(e))
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()

def parse_event(db_session, active_flow, selected_flow, completed_event_ids, event):
    next_event = None
    if event.id not in completed_event_ids:
        if event.delay is not None and event.delay > 0:
            delayed_event = db_session.query(DelayedFlowEvent) \
                .filter(DelayedFlowEvent.active_flow_id == active_flow.id) \
                .filter(DelayedFlowEvent.flow_event_id == event.id) \
                .first()

            print('delayed_event: {}'.format(delayed_event))

            if delayed_event is None:
                # create delayed event
                delayed_event = DelayedFlowEvent()
                delayed_event.active_flow_id = active_flow.id
                delayed_event.flow_event_id = event.id
                delayed_event.delay = event.delay
                delayed_event.delay_unit = event.delay_unit
                db_session.add(delayed_event)
                db_session.commit()
                return
            else:
                # check if delay has passed
                future_datetime = None
                if delayed_event.delay_unit == 'seconds':
                    future_datetime = delayed_event.created_at + datetime.timedelta(seconds=delayed_event.delay)
                elif delayed_event.delay_unit == 'minutes':
                    future_datetime = delayed_event.created_at + datetime.timedelta(minutes=delayed_event.delay)
                elif delayed_event.delay_unit == 'hours':
                    future_datetime = delayed_event.created_at + datetime.timedelta(hours=delayed_event.delay)
                elif delayed_event.delay_unit == 'days':
                    future_datetime = delayed_event.created_at + datetime.timedelta(days=delayed_event.delay)
                elif delayed_event.delay_unit == 'weeks':
                    future_datetime = delayed_event.created_at + datetime.timedelta(weeks=delayed_event.delay)
                elif delayed_event.delay_unit == 'months':
                    future_datetime = delayed_event.created_at + relativedelta(months=+delayed_event.delay)

                if future_datetime <= datetime.datetime.utcnow():
                    print('delay has passed')
                    # delay has passed send notification
                    db_session.delete(delayed_event)
                    db_session.commit()
                else:
                    print('delay has not passed')
                    # delay has not passed
                    return None

        if event.statement is not None:
            key = event.statement.split(' ')[0]
            operator = event.statement.split(' ')[1]
            value = event.statement.split(' ')[2]

            app_user = db_session.query(AppUser).filter(AppUser.id == active_flow.app_user_id).first()

            app_user_key = (db_session.query(AppUserKey)
                   .filter(AppUserKey.app_id == app_user.app_id, AppUserKey.key == key)
                   .first())

            app_user_value = (db_session.query(AppUserValue)
                   .filter(AppUserValue.app_user_id == app_user.id, AppUserValue.key == key)
                   .first())

            statement = None
            if key == 'current_date':
                statement = 'datetime.datetime.utcnow().date() ' + operator + ' datetime.datetime.strptime("' + value + '", "%Y-%m-%d").date()'
            elif key == 'user.created_at':
                statement = 'app_user.created_at.date() ' + operator + ' datetime.datetime.strptime("' + value + '", "%Y-%m-%d").date()'
            elif app_user_value is not None:
                if app_user_key.type == 'datetime':
                    statement = 'datetime.datetime.strptime("' + str(app_user_value.value).lower() + '", "%Y-%m-%d").date() ' + operator + ' datetime.datetime.strptime("' + str(value).lower() + '", "%Y-%m-%d").date()'
                elif app_user_key.type == 'number':
                    statement = 'int(' + str(app_user_value.value) + ') ' + operator + ' int(' + str(value) + ')'
                elif app_user_key.type == 'boolean':
                    statement = 'bool(' + str(app_user_value.value) + ') ' + operator + ' bool(' + str(value) + ')'
                else:
                    statement = app_user_value.value + ' ' + operator + ' "' + value + '"'

            print(statement)

            if statement is None or eval(statement) is False:
                print('statement is false')
                next_event = db_session.query(FlowEvent).filter(FlowEvent.parent_id == event.id, FlowEvent.is_no == True).first()
            else:
                print('statement is true')
                next_event = db_session.query(FlowEvent).filter(FlowEvent.parent_id == event.id, FlowEvent.is_yes == True).first()

        if event.notification_id is not None:
            notification = db_session.query(Notification).filter(Notification.id == event.notification_id).first()
            if notification is None:
                print('notification not found')
                return None

            app_user = db_session.query(AppUser).filter(AppUser.id == active_flow.app_user_id).first()
            if app_user is None:
                print('app user not found')
                return None

            selected_app = db_session.query(App).filter(App.id == app_user.app_id).first()

            send_push_notification(db_session, selected_app, app_user, notification, in_flow=True)

        if event.type == 'End':
            db_session.delete(active_flow)
            db_session.commit()
            return None

        if event.loop_back_to_event_id is not None:
            for completed_event_id in completed_event_ids:
                completed_event = db_session.query(CompletedFlowEvent)\
                    .filter(CompletedFlowEvent.active_flow_id == active_flow.id)\
                    .filter(CompletedFlowEvent.flow_event_id == completed_event_id)\
                    .first()
                db_session.delete(completed_event)
                db_session.commit()

            next_event = db_session.query(FlowEvent).filter(FlowEvent.id == event.loop_back_to_event_id).first()

        if next_event is None:
            if len(event.events) > 0:
                next_event = event.events[0]

        if next_event is not None and event.loop_back_to_event_id is None:
            completed_event = CompletedFlowEvent()
            completed_event.active_flow_id = active_flow.id
            completed_event.flow_event_id = event.id
            completed_event.next_flow_event_id = next_event.id
            db_session.add(completed_event)
            db_session.commit()
    else:
        print(active_flow.id)
        print(event.id)
        completed_event = db_session.query(CompletedFlowEvent)\
            .filter(CompletedFlowEvent.active_flow_id == active_flow.id, CompletedFlowEvent.flow_event_id == event.id)\
            .first()

        print(completed_event.next_flow_event_id)

        next_event = db_session.query(FlowEvent).filter(FlowEvent.id == completed_event.next_flow_event_id).first()

    if next_event is None:
        return None

    completed_events = db_session.query(CompletedFlowEvent) \
        .filter(CompletedFlowEvent.active_flow_id == active_flow.id) \
        .all()
    completed_event_ids = [completed_event.flow_event_id for completed_event in completed_events]

    parse_event(db_session, active_flow, selected_flow, completed_event_ids, next_event)

    return None

def send_push_notification(db_session, selected_app, app_user, notification, in_flow=False):
    if in_flow is False:
        app_user_notification = db_session.query(AppUserNotification) \
            .filter(AppUserNotification.app_user_id == app_user.id) \
            .filter(AppUserNotification.notification_id == notification.id) \
            .first()
        print('app_user_notification: {}'.format(app_user_notification))
        if app_user_notification:
            if app_user_notification.delivered is True:
                return True

            if app_user_notification.attempts is not None and app_user_notification.attempts >= 3:
                return False

            if (app_user_notification.last_sent_at is not None and
                    app_user_notification.last_sent_at + datetime.timedelta(hours=1) <=
                    datetime.datetime.utcnow()):
                # wait at least 30 minutes before resending notification
                return False
        else:
            app_user_notification = AppUserNotification()
            app_user_notification.app_user_id = app_user.id
            app_user_notification.notification_id = notification.id
            db_session.add(app_user_notification)
            db_session.commit()

        attempts = app_user_notification.attempts if app_user_notification.attempts is not None else 0

        app_user_notification.attempts = attempts + 1 if attempts is not None else 1
        app_user_notification.last_sent_at = datetime.datetime.utcnow()
        db_session.commit()
    else:
        app_user_notification = AppUserNotification()
        app_user_notification.app_user_id = app_user.id
        app_user_notification.notification_id = notification.id
        db_session.add(app_user_notification)
        db_session.commit()

    response = False
    try:
        if app_user.fcm_token is not None:
            fcm.send(selected_app, app_user, app_user_notification.hash, notification)
        elif app_user.apn_device_token is not None:
            apn.send(selected_app, app_user, app_user_notification.hash, notification)
        elif app_user.web_push_endpoint is not None:
            subscription_info = {
                'endpoint': app_user.web_push_endpoint,
                'keys': {
                    'p256dh': app_user.web_push_p256dh,
                    'auth': app_user.web_push_auth
                }
            }
            data = {
                'id': app_user_notification.hash,
                'icon': selected_app.icon if selected_app.icon else 'https://getmagicpush.com/images/magicpushlogo.png',
                'image': notification.image,
                'title': notification.default_title,
                'message': notification.default_message,
                'action': notification.action
            }
            headers = None
            if 'windows' in app_user.web_push_endpoint:
                headers = {
                    'x-wns-cache-policy': 'no-cache'
                }

            webpush(subscription_info=subscription_info, data=json.dumps(data),
                    vapid_private_key=selected_app.vapid_private_key,
                    headers=headers,
                    vapid_claims={'sub': 'mailto:pushoperations@getmagicpush.com'})
            response = True
    except Exception as e:
        app.logger.exception('Notifier: {}'.format(e))
        app_user_notification.response = str(e)
        db_session.commit()

    if response is True:
        app_user_notification.delivered = True
        app_user_notification.delivered_at = datetime.datetime.utcnow()
        db_session.commit()

    return response

@celery_app.task()
def run_billing():
    from magicpush.database import db_session
    try:
        users = (db_session.query(User)
                 .filter(User.stripe_customer_id != None)
                 .all())

        for user in users:
            print(user.email)
            print(user.last_billed_at)
            if (user.last_billed_at is None or
                    user.last_billed_at <= datetime.datetime.utcnow() - datetime.timedelta(days=30)):
                print('billing')
                total_subscribers = (db_session.query(AppUser)
                                     .join(App, AppUser.app_id == App.id)
                                     .filter(App.user_id == user.id, AppUser.web_push_endpoint != None)
                                     .count())

                active_flows = db_session.query(Flow).filter(Flow.enabled == True).count()

                print('total_subscribers: {}'.format(total_subscribers))

                if total_subscribers < 1000 and active_flows <= 1:
                    continue

                if user.has_purchased_deal is True and total_subscribers < 200000:
                    continue

                try:
                    subscriptions = stripe.get_subscriptions(user.stripe_customer_id)

                    if len(subscriptions['data']) == 0:
                        continue

                    current_price_id = subscriptions['data'][0]['items']['data'][0]['price']['id']

                    value = 1
                    if total_subscribers >= 5000 and total_subscribers < 15000:
                        value = 2
                    elif total_subscribers >= 15000 and total_subscribers < 50000:
                        value = 4
                    elif total_subscribers >= 50000 and total_subscribers < 100000:
                        value = 6
                    elif total_subscribers >= 100000:
                        if current_price_id == 'price_1PO58FInCJD8iYfuCiyV2z0K' or\
                                current_price_id == 'price_1PNzKYInCJD8iYfuGjhrI4m9':
                            value = 105 + ((total_subscribers - 100000) / 1000)
                        else:
                            value = 8 + ((total_subscribers - 100000) / 1000)

                    print('value: {}'.format(value))

                    stripe.update_meter(user.stripe_customer_id, value)

                    user.last_billed_at = datetime.datetime.utcnow()
                    db_session.commit()
                except Exception as e:
                    app.logger.exception('Run Billing: {}'.format(e))
                    continue
        db_session.close()
    except Exception as e:
        app.logger.exception('Run Billing: {}'.format(e))
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
