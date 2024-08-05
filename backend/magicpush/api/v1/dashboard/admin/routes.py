from . import admin
from magicpush import app
from magicpush.models import App, AppUser, AppUserNotification

import datetime
import sqlalchemy as sa
from sqlalchemy import and_, or_
from flask import request, jsonify
from dateutil.relativedelta import relativedelta
from flask_login import login_required, current_user


@admin.route('/info', methods=['GET'])
@login_required
def get_info():
    from magicpush.database import db_session
    try:
        if not current_user.is_admin:
            db_session.close()
            return jsonify({'message': 'Unauthorized'}), 401

        total_subscribers = db_session.query(AppUser) \
            .filter(or_(AppUser.web_push_endpoint != None, AppUser.fcm_token != None,
                        AppUser.apn_device_token != None)) \
            .count()

        last_total_subscribers = db_session.query(AppUser) \
            .filter(or_(AppUser.web_push_endpoint != None, AppUser.fcm_token != None,
                        AppUser.apn_device_token != None)) \
            .filter(AppUser.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=30))\
            .count()

        growth_rate = (total_subscribers - last_total_subscribers) / last_total_subscribers * 100 \
            if last_total_subscribers > 0 else None

        total_notifications = db_session.query(AppUserNotification)\
            .join(AppUser, AppUser.id == AppUserNotification.app_user_id)\
            .count()

        last_total_notifications = db_session.query(AppUserNotification)\
            .join(AppUser, AppUser.id == AppUserNotification.app_user_id)\
            .filter(AppUserNotification.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=30))\
            .count()

        total_delivered_notifications = db_session.query(AppUserNotification)\
            .join(AppUser, AppUser.id == AppUserNotification.app_user_id)\
            .filter(AppUserNotification.delivered == True)\
            .count()

        last_total_delivered_notifications = db_session.query(AppUserNotification)\
            .join(AppUser, AppUser.id == AppUserNotification.app_user_id)\
            .filter(AppUserNotification.delivered == True)\
            .filter(AppUserNotification.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=30))\
            .count()

        total_clicked_notifications = db_session.query(AppUserNotification)\
            .join(AppUser, AppUser.id == AppUserNotification.app_user_id)\
            .filter(AppUserNotification.clicked == True)\
            .count()

        last_total_clicked_notifications = db_session.query(AppUserNotification)\
            .join(AppUser, AppUser.id == AppUserNotification.app_user_id)\
            .filter(AppUserNotification.clicked == True)\
            .filter(AppUserNotification.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=30))\
            .count()

        delivery_rate = total_delivered_notifications / total_notifications * 100 if total_notifications > 0 else 0
        click_rate = total_clicked_notifications / total_notifications * 100 if total_notifications > 0 else 0

        last_delivery_rate = last_total_delivered_notifications / last_total_notifications * 100 \
            if last_total_notifications > 0 else 0
        last_click_rate = last_total_clicked_notifications / last_total_notifications * 100 \
            if last_total_notifications > 0 else 0

        delivery_rate_growth = (delivery_rate - last_delivery_rate) / last_delivery_rate * 100 \
            if last_delivery_rate > 0 else None
        click_rate_growth = (click_rate - last_click_rate) / last_click_rate * 100 \
            if last_click_rate > 0 else None

        json = {
            'total_subscribers': total_subscribers,
            'total_subscribers_growth_rate': growth_rate,
            'delivery_rate': delivery_rate,
            'delivery_rate_growth_rate': delivery_rate_growth,
            'click_rate': click_rate,
            'click_rate_growth_rate': click_rate_growth
        }
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'Internal server error'}), 500


@admin.route('/subscribers', methods=['GET'])
@login_required
def get_subscribers():
    from magicpush.database import db_session
    try:
        if not current_user.is_admin:
            db_session.close()
            return jsonify({'message': 'Unauthorized'}), 401

        select = []
        queries = []

        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=30)
        end_date = datetime.datetime.utcnow()
        select.append(sa.func.date_trunc('day', AppUser.created_at).label('time'))
        queries.append(and_(AppUser.created_at >= start_date, AppUser.created_at <= end_date))

        subscribers_query = db_session.query(*select, AppUser.id) \
            .filter(or_(AppUser.web_push_endpoint != None, AppUser.fcm_token != None,
                        AppUser.apn_device_token != None)) \
            .filter(*queries)\
            .subquery()

        subscribers_results = db_session \
            .query(subscribers_query.c.time, sa.func.count(subscribers_query.c.id).label('subscribers')) \
            .group_by(subscribers_query.c.time) \
            .order_by(subscribers_query.c.time.asc())

        last_30_days = [start_date + datetime.timedelta(days=i) for i in range(30)]

        results = []
        for date in last_30_days:
            result = {
                'time': date.date(),
                'subscribers': 0
            }
            for subscriber_result in subscribers_results:
                if subscriber_result.time.date() == date.date():
                    result['subscribers'] = subscriber_result.subscribers
                    break
            results.append(result)

        json = {
            'results': [
                {
                    str(result['time']): int(result['subscribers']) if result['subscribers'] is not None else 0
                } for result in results
            ]
        }
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'Internal server error'}), 500


@admin.route('/messages', methods=['GET'])
@login_required
def get_messages():
    from magicpush.database import db_session
    try:
        if not current_user.is_admin:
            db_session.close()
            return jsonify({'message': 'Unauthorized'}), 401

        select = []
        queries = []

        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=30)
        end_date = datetime.datetime.utcnow()
        select.append(sa.func.date_trunc('day', AppUserNotification.created_at).label('time'))
        queries.append(and_(AppUserNotification.created_at >= start_date, AppUserNotification.created_at <= end_date))

        messages_query = db_session.query(*select, AppUserNotification.id)\
            .filter(AppUserNotification.delivered == True)\
            .filter(*queries)\
            .subquery()

        subscribers_results = db_session \
            .query(messages_query.c.time, sa.func.count(messages_query.c.id).label('subscribers')) \
            .group_by(messages_query.c.time) \
            .order_by(messages_query.c.time.asc())

        last_30_days = [start_date + datetime.timedelta(days=i) for i in range(30)]

        results = []
        for date in last_30_days:
            result = {
                'time': date.date(),
                'subscribers': 0
            }
            for subscriber_result in subscribers_results:
                if subscriber_result.time.date() == date.date():
                    result['subscribers'] = subscriber_result.subscribers
                    break
            results.append(result)

        json = {
            'results': [
                {
                    str(result['time']): int(result['messages']) if result['messages'] is not None else 0
                } for result in results
            ]
        }
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'Internal server error'}), 500


# get subscribers per app without time
@admin.route('/subscribers/app', methods=['GET'])
@login_required
def get_subscribers_per_app():
    from magicpush.database import db_session
    try:
        if not current_user.is_admin:
            db_session.close()
            return jsonify({'message': 'Unauthorized'}), 401

        subscribers_query = db_session.query(App.name, sa.func.count(AppUser.id).label('subscribers'))\
            .join(AppUser, App.id == AppUser.app_id)\
            .filter(AppUser.web_push_endpoint != None)\
            .group_by(App.name)

        results = subscribers_query.all()

        json = {
            'results': [
                {
                    str(result['name']): int(result['subscribers']) if result['subscribers'] is not None else 0
                } for result in results
            ]
        }
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'Internal server error'}), 500

