from magicpush import app
from magicpush.models import App, AppEvent


def populate_events():
    from magicpush.database import db_session
    try:
        apps = db_session.query(App).all()

        for current_app in apps:
            events = current_app.events

            if len(events) == 0:
                default_events = ['subscribed']

                for event in default_events:
                    new_event = AppEvent()
                    new_event.app_id = current_app.id
                    new_event.name = event

                    db_session.add(new_event)
                    db_session.commit()

        db_session.close()
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
