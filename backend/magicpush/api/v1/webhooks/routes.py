import os
import hmac
import stripe
import hashlib

from flask import request, jsonify

from . import webhooks
from magicpush import app
from magicpush.models import User

stripe.api_key = os.getenv('STRIPE_API_KEY')
endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')

@webhooks.route('/stripe', methods=['POST'])
def stripe_webhook():
    from magicpush.database import db_session
    try:
        event = None
        payload = request.data
        sig_header = request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = stripe.checkout.Session.list_line_items(event['data']['object']['id'])

            if 'data' in session and session['data'] is not None:
                line_items = session['data']

                user = db_session.query(User).filter(User.stripe_customer_id == event['data']['object']['customer']).first()

                for item in line_items:
                    if item['price']['id'] == os.getenv('STRIPE_DEAL_PRICE_ID'):
                        user.has_purchased_deal = True
                        db_session.commit()
        else:
            print('Unhandled event type {}'.format(event['type']))

        db_session.close()
        return 'Ok', 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500

@webhooks.route('/lemons', methods=['POST'])
def lemons():
    from magicpush.database import db_session
    try:
        signature = request.headers.get('X-Signature')

        digest = hmac.new(os.getenv('LEMONS_SIGNING_KEY').encode('utf-8'), request.data, hashlib.sha256).hexdigest()

        if signature != digest:
            db_session.close()
            return jsonify({'message': 'Invalid signature'}), 400

        if request.is_json:
            json = request.get_json()

            event = json['meta']['event_name']
            email = json['data']['attributes']['user_email']
            customer_id = json['data']['attributes']['customer_id']

            user = db_session.query(User).filter(User.email == email).first()

            if user is None:
                user = User()
                user.email = email
                user.lemonsqueezy_customer_id = customer_id
                db_session.add(user)
                db_session.commit()
            else:
                user.lemonsqueezy_customer_id = customer_id
                db_session.commit()

            if event == 'subscription_created':
                user.lemonsqueezy_subscription_id = json['data']['id']
                user.subscription_status = 'active'
                db_session.commit()
            elif event == 'subscription_updated':
                pass
            elif event == 'subscription_cancelled':
                user.subscription_status = 'cancelled'
                db_session.commit()
            elif event == 'subscription_resumed':
                user.subscription_status = 'active'
                db_session.commit()
            elif event == 'subscription_expired':
                user.subscription_status = 'expired'
                db_session.commit()
            elif event == 'subscription_paused':
                user.subscription_status = 'paused'
                db_session.commit()
            elif event == 'subscription_unpaused':
                user.subscription_status = 'active'
                db_session.commit()
            elif event == 'order_created':
                if json['data']['attributes']['first_order_item']['product_id'] == 283185\
                        or json['data']['attributes']['first_order_item']['product_id'] == 280627:
                    if json['data']['attributes']['status'] == 'paid':
                        user.has_purchased_deal = True
                        db_session.commit()
            elif event == 'order_refunded':
                if json['data']['attributes']['first_order_item']['product_id'] == 283185\
                        or json['data']['attributes']['first_order_item']['product_id'] == 280627:
                    user.has_purchased_deal = False
                    db_session.commit()
        db_session.close()
        return jsonify({'message': 'ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500
