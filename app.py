from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import os

app = Flask(__name__)
CORS(app, origins=[
    "https://jpressocoffee.com",
    "https://www.jpressocoffee.com",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
])

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.get_json()
        items = data.get("items", [])
        customer_email = data.get("customer_email")

        if not items:
            return jsonify({"error": "No items in cart"}), 400

        line_items = []
        for item in items:
            unit_amount = int(float(item["price"]) * 100)
            line_items.append({
                "price_data": {
                    "currency": "myr",
                    "unit_amount": unit_amount,
                    "product_data": {
                        "name": item["name"],
                        "description": item.get("description", ""),
                    },
                },
                "quantity": item["quantity"],
            })

        session_params = {
            "payment_method_types": ["card"],
            "line_items": line_items,
            "mode": "payment",
            "success_url": "https://www.jpressocoffee.com/jpresso-subscribe.html?success=true",
            "cancel_url": "https://www.jpressocoffee.com/jpresso-subscribe.html?cancelled=true",
            "shipping_address_collection": {
                "allowed_countries": ["MY"],
            },
            "shipping_options": [
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 0, "currency": "myr"},
                        "display_name": "Free Shipping (Peninsular MY)",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 3},
                            "maximum": {"unit": "business_day", "value": 5},
                        },
                    },
                },
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 1500, "currency": "myr"},
                        "display_name": "East Malaysia (Sabah & Sarawak)",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 5},
                            "maximum": {"unit": "business_day", "value": 10},
                        },
                    },
                },
            ],
        }

        if customer_email:
            session_params["customer_email"] = customer_email

        session = stripe.checkout.Session.create(**session_params)
        return jsonify({"url": session.url})

    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/create-subscription-session", methods=["POST"])
def create_subscription_session():
    SUBSCRIPTION_PRICES = {
        "so-weekly": "price_REPLACE_WITH_REAL_ID",
        "so-biweekly": "price_REPLACE_WITH_REAL_ID",
        "so-monthly": "price_REPLACE_WITH_REAL_ID",
        "bl-weekly": "price_REPLACE_WITH_REAL_ID",
        "bl-biweekly": "price_REPLACE_WITH_REAL_ID",
        "bl-monthly": "price_REPLACE_WITH_REAL_ID",
        "es-weekly": "price_REPLACE_WITH_REAL_ID",
        "es-biweekly": "price_REPLACE_WITH_REAL_ID",
        "es-monthly": "price_REPLACE_WITH_REAL_ID",
    }

    try:
        data = request.get_json()
        plan_id = data.get("plan_id")

        price_id = SUBSCRIPTION_PRICES.get(plan_id)
        if not price_id or "REPLACE" in price_id:
            return jsonify({"error": f"Subscription '{plan_id}' not configured. Create the price in Stripe Dashboard first."}), 400

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url="https://www.jpressocoffee.com/jpresso-subscribe.html?sub=success",
            cancel_url="https://www.jpressocoffee.com/jpresso-subscribe.html?sub=cancelled",
        )

        return jsonify({"url": session.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "stripe_configured": bool(stripe.api_key)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
