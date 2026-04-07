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


def get_shipping_options(items):
    green_kg = 0
    has_non_green = False

    for item in items:
        if item.get("type") == "green":
            green_kg += item.get("quantity", 1)
        else:
            has_non_green = True

    if green_kg == 0:
        return [
            {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 990, "currency": "myr"},
                    "display_name": "Peninsular MY",
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
                    "display_name": "East Malaysia (Sabah & Sarawak) - RM15",
                    "delivery_estimate": {
                        "minimum": {"unit": "business_day", "value": 5},
                        "maximum": {"unit": "business_day", "value": 10},
                    },
                },
            },
        ]

    if green_kg >= 60:
        pen_amount = 0
        pen_label = f"Free Shipping (Peninsular MY) - {green_kg}kg"
    elif green_kg >= 30:
        pen_amount = 6000
        pen_label = f"Peninsular MY - RM60 ({green_kg}kg)"
    elif green_kg >= 10:
        pen_amount = 4000
        pen_label = f"Peninsular MY - RM40 ({green_kg}kg)"
    elif green_kg >= 5:
        pen_amount = 2500
        pen_label = f"Peninsular MY - RM25 ({green_kg}kg)"
    else:
        pen_amount = 1500
        pen_label = f"Peninsular MY - RM15 ({green_kg}kg)"

    options = [
        {
            "shipping_rate_data": {
                "type": "fixed_amount",
                "fixed_amount": {"amount": pen_amount, "currency": "myr"},
                "display_name": pen_label,
                "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 3},
                    "maximum": {"unit": "business_day", "value": 7},
                },
            },
        },
    ]

    if green_kg < 30:
        if green_kg >= 10:
            em_amount = 15000
            em_label = f"East Malaysia - RM150 ({green_kg}kg)"
        elif green_kg >= 5:
            em_amount = 8000
            em_label = f"East Malaysia - RM80 ({green_kg}kg)"
        else:
            em_amount = 5000
            em_label = f"East Malaysia - RM50 ({green_kg}kg)"

        options.append({
            "shipping_rate_data": {
                "type": "fixed_amount",
                "fixed_amount": {"amount": em_amount, "currency": "myr"},
                "display_name": em_label,
                "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 5},
                    "maximum": {"unit": "business_day", "value": 10},
                },
            },
        })
    else:
        options.append({
            "shipping_rate_data": {
                "type": "fixed_amount",
                "fixed_amount": {"amount": 0, "currency": "myr"},
                "display_name": "East Malaysia (30kg+) - Contact us for quote",
                "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 7},
                    "maximum": {"unit": "business_day", "value": 14},
                },
            },
        })

    if has_non_green:
        options[0]["shipping_rate_data"]["display_name"] += " + roasted/equipment"

    return options


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

        shipping_options = get_shipping_options(items)

        session_params = {
            "payment_method_types": ["card"],
            "line_items": line_items,
            "mode": "payment",
            "success_url": "https://www.jpressocoffee.com/jpresso-subscribe.html?success=true",
            "cancel_url": "https://www.jpressocoffee.com/jpresso-subscribe.html?cancelled=true",
            "shipping_address_collection": {
                "allowed_countries": ["MY"],
            },
            "shipping_options": shipping_options,
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
        "so-weekly": "price_1TIjV3H2MTIbGDtxkUZGzvJ8",
        "so-biweekly": "price_1TIjVrH2MTIbGDtx6OnJKT5L",
        "so-monthly": "price_1TIjWYH2MTIbGDtxEuaUQJ0F",
        "bl-weekly": "price_1TIjXIH2MTIbGDtxtII3MgHo",
        "bl-biweekly": "price_1TIjXuH2MTIbGDtx46YZeUYy",
        "bl-monthly": "price_1TIjYQH2MTIbGDtxtmILDSns",
        "es-weekly": "price_1TIjZnH2MTIbGDtx3KF2OMBI",
        "es-biweekly": "price_1TIj4OH2MTIbGDtxdYNttWzT",
        "es-monthly": "price_1TIjaXH2MTIbGDtxcU468xU8",
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
