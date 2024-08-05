from . import flow
from magicpush import app
from magicpush.models import App, AppEvent, AppUserKey, Flow, FlowEvent, Notification

import datetime
from flask import jsonify, request
from flask_login import login_required, current_user


# get notification flows
@flow.route('/<app_id>', methods=['GET'])
@login_required
def get_flows(app_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        flows = db_session.query(Flow).filter(Flow.app_id == app_id, Flow.deleted != True).all()

        json = []
        for flow in flows:
            json.append(flow.to_json())

        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# get notification flow
@flow.route('/<app_id>/<flow_id>', methods=['GET'])
@login_required
def get_flow(app_id, flow_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        selected_flow = db_session.query(Flow).filter(Flow.id == flow_id, Flow.app_id == app_id).first()

        if selected_flow is None:
            db_session.close()
            return jsonify({'message': 'Flow not found'}), 404

        flow_events = db_session.query(FlowEvent)\
            .filter(FlowEvent.flow_id == selected_flow.id, FlowEvent.is_start == True)\
            .all()

        json = selected_flow.to_json()
        json['events'] = [event.to_json() for event in flow_events] if flow_events is not None else []
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# create notification flow
@flow.route('/<app_id>', methods=['POST'])
@login_required
def create_flow(app_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        if 'name' in request.json and 'event' in request.json:
            new_flow = Flow()
            new_flow.app_id = app_id
            new_flow.name = request.json.get('name')
            new_flow.event = request.json.get('event')
            new_flow.enabled = request.json.get('enabled') \
                if 'enabled' in request.json else False
            new_flow.one_time = request.json.get('one_time') \
                if 'one_time' in request.json else False
            db_session.add(new_flow)
            db_session.commit()

            existing_app_event = (db_session.query(AppEvent)
                                  .filter(AppEvent.app_id == app_id, AppEvent.name == new_flow.event)
                                  .first())
            if existing_app_event is None:
                new_app_event = AppEvent()
                new_app_event.app_id = app_id
                new_app_event.name = new_flow.event
                db_session.add(new_app_event)
                db_session.commit()

            json = new_flow.to_json()
            db_session.close()
            return jsonify(json), 201
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# update notification flow
@flow.route('/<app_id>/<flow_id>', methods=['PUT'])
@login_required
def update_flow(app_id, flow_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        selected_flow = db_session.query(Flow).filter(Flow.id == flow_id, Flow.app_id == app_id).first()

        if selected_flow is None:
            db_session.close()
            return jsonify({'message': 'Flow not found'}), 404

        selected_flow.name = request.json.get('name') \
            if 'name' in request.json else selected_flow.name
        selected_flow.event = request.json.get('event') \
            if 'event' in request.json else selected_flow.event
        selected_flow.enabled = request.json.get('enabled') \
            if 'enabled' in request.json else selected_flow.enabled
        selected_flow.one_time = request.json.get('one_time') \
            if 'one_time' in request.json else selected_flow.one_time
        db_session.commit()

        if 'event' in request.json:
            existing_app_event = (db_session.query(AppEvent)
                                  .filter(AppEvent.app_id == app_id, AppEvent.name == selected_flow.event)
                                  .first())
            if existing_app_event is None:
                new_app_event = AppEvent()
                new_app_event.app_id = app_id
                new_app_event.name = selected_flow.event
                db_session.add(new_app_event)
                db_session.commit()

        if 'events' in request.json:
            for event in request.json.get('events'):
                if 'id' in event:
                    selected_event = db_session.query(FlowEvent).filter(FlowEvent.id == event.get('id')).first()
                    if selected_event is not None:
                        selected_event.parent_id = event.get('parent_id') \
                            if 'parent_id' in event else selected_event.parent_id
                        selected_event.type = event.get('type') \
                            if 'type' in event else selected_event.type
                        selected_event.delay = event.get('delay') \
                            if 'delay' in event else selected_event.delay
                        selected_event.delay_unit = event.get('delay_unit') \
                            if 'delay_unit' in event else selected_event.delay_unit
                        selected_event.notification_id = event.get('notification_id') \
                            if 'notification_id' in event else selected_event.notification_id
                        selected_event.statement = event.get('statement') \
                            if 'statement' in event else selected_event.statement
                        selected_event.is_start = event.get('parent_id') is None \
                            if 'parent_id' in event else selected_event.is_start
                        db_session.commit()
                else:
                    new_event = FlowEvent()
                    new_event.flow_id = selected_flow.id
                    new_event.parent_id = event.get('parent_id') \
                        if 'parent_id' in event else None
                    new_event.loop_back_to_event_id = event.get('loop_back_to_event_id') \
                        if 'loop_back_to_event_id' in event else None
                    new_event.type = event.get('type') \
                        if 'type' in event else None
                    new_event.delay = event.get('delay') \
                        if 'delay' in event else None
                    new_event.delay_unit = event.get('delay_unit') \
                        if 'delay_unit' in event else None
                    new_event.notification_id = event.get('notification_id') \
                        if 'notification_id' in event else None
                    new_event.statement = event.get('statement') \
                        if 'statement' in event else None
                    new_event.is_start = event.get('parent_id') is None \
                        if 'parent_id' in event else True
                    db_session.add(new_event)
                    db_session.commit()

                    if 'key' in event:
                        app_key = (db_session.query(AppUserKey)
                                   .filter(AppUserKey.app_id == app_id, AppUserKey.key == event.get('key').get('key'))
                                   .first())

                        if app_key is None:
                            app_key = AppUserKey()
                            app_key.app_id = app_id
                            app_key.key = event.get('key').get('key')
                            app_key.type = event.get('key').get('type')
                            db_session.add(app_key)
                            db_session.commit()

                        new_event.key = app_key.id

                    if 'statement' in event:
                        new_yes_event = FlowEvent()
                        new_yes_event.flow_id = selected_flow.id
                        new_yes_event.parent_id = new_event.id
                        new_yes_event.type = 'Yes'
                        new_yes_event.is_yes = True
                        db_session.add(new_yes_event)
                        db_session.commit()

                        new_no_event = FlowEvent()
                        new_no_event.flow_id = selected_flow.id
                        new_no_event.parent_id = new_event.id
                        new_no_event.type = 'No'
                        new_no_event.is_no = True
                        db_session.add(new_no_event)
                        db_session.commit()

                        move_event_down(db_session, event, selected_flow, new_event, new_yes_event)
                    else:
                        move_event_down(db_session, event, selected_flow, new_event)

        flow_events = db_session.query(FlowEvent)\
            .filter(FlowEvent.flow_id == selected_flow.id, FlowEvent.is_start == True)\
            .all()

        json = selected_flow.to_json()
        json['events'] = [event.to_json() for event in flow_events] if flow_events is not None else []
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


def move_event_down(db_session, event, selected_flow, new_event, new_yes_event=None):
    if 'parent_id' in event and event.get('parent_id') is not None:
        # move connected events down
        connected_event = db_session.query(FlowEvent) \
            .filter(FlowEvent.id != new_event.id,
                    FlowEvent.flow_id == selected_flow.id,
                    FlowEvent.parent_id == event.get('parent_id')) \
            .first()
        if connected_event is not None:
            connected_event.parent_id = new_event.id if new_yes_event is None else new_yes_event.id
            db_session.commit()
    else:
        first_event = db_session.query(FlowEvent) \
            .filter(FlowEvent.id != new_event.id,
                    FlowEvent.flow_id == selected_flow.id,
                    FlowEvent.parent_id == None) \
            .first()
        if first_event is not None:
            first_event.parent_id = new_event.id if new_yes_event is None else new_yes_event.id
            first_event.is_start = False
            db_session.commit()


# delete notification flow
@flow.route('/<app_id>/<flow_id>', methods=['DELETE'])
@login_required
def delete_flow(app_id, flow_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        selected_flow = db_session.query(Flow).filter(Flow.id == flow_id, Flow.app_id == app_id).first()

        if selected_flow is None:
            db_session.close()
            return jsonify({'message': 'Flow not found'}), 404

        selected_flow.deleted = True
        selected_flow.deleted_at = datetime.datetime.utcnow()
        db_session.commit()
        db_session.close()
        return jsonify({'message': 'ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500
