# ═══════════════════════════════════════════════════════════
# JPRESSO STRIPE CHECKOUT SETUP GUIDE
# ═══════════════════════════════════════════════════════════
#
# STEP 1: Get your Stripe API keys
# ─────────────────────────────────
# 1. Go to https://dashboard.stripe.com/apikeys
# 2. Copy your "Secret key" (starts with sk_test_ for testing, sk_live_ for real)
# 3. Copy your "Publishable key" (starts with pk_test_ or pk_live_)
# 4. Add to your Render environment variables:
#    STRIPE_SECRET_KEY = sk_test_xxxxx  (or sk_live_xxxxx for production)
#
#
# STEP 2: Deploy this backend on Render
# ──────────────────────────────────────
# Option A: Add to your existing roastery-os repo as a new route
# Option B: Create a separate small service (recommended)
#
# If separate service:
#   - Create new GitHub repo "jpresso-checkout"
#   - Push this file as app.py
#   - Push requirements.txt (see bottom of this file)
#   - Create new Render Web Service → connect repo → auto-deploy
#   - Add STRIPE_SECRET_KEY as environment variable
#
#
# STEP 3: Update the frontend
# ───────────────────────────
# Replace the alert() in the checkout button with a fetch() to your backend
# (Code provided at the bottom of this file)
#
# ═══════════════════════════════════════════════════════════


from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import os

app = Flask(__name__)
CORS(app, origins=[
    "https://jpressocoffee.com",
    "https://www.jpressocoffee.com",
    "http://localhost:3000",  # for local testing
    "http://127.0.0.1:5500", # for VS Code Live Server testing
])

# Set your Stripe secret key from environment variable
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """
    Receives cart items from the frontend and creates a Stripe Checkout Session.
    
    Expected JSON body:
    {
        "items": [
            {
                "name": "Ethiopia Guji Siko",
                "price": 68,          # price in RM (for roasted beans, per 200g bag)
                "quantity": 2,
                "description": "Natural · Heirloom · 200g",
                "type": "roasted"      # "roasted", "green", or "equip"
            },
            {
                "name": "Honduras El Laurel (Green)",
                "price": 165,          # price in RM per kg (for green beans)
                "quantity": 10,         # kg quantity
                "description": "Washed · Parainema · 10kg @ RM165/kg",
                "type": "green"
            },
            {
                "name": "Timemore C5 Hand Grinder",
                "price": 230,
                "quantity": 1,
                "description": "S2C-042-III Burrs · Black",
                "type": "equip"
            }
        ],
        "customer_email": "optional@email.com"
    }
    """
    try:
        data = request.get_json()
        items = data.get("items", [])
        customer_email = data.get("customer_email")

        if not items:
            return jsonify({"error": "No items in cart"}), 400

        # Build Stripe line_items dynamically from cart
        line_items = []
        for item in items:
            unit_amount = int(float(item["price"]) * 100)  # Stripe uses cents (sen)
            
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

        # Create checkout session params
        session_params = {
            "payment_method_types": ["card", "fpx"],  # Card + Malaysian FPX bank transfer!
            "line_items": line_items,
            "mode": "payment",
            "success_url": "www.jpressocoffee.com/jpresso-subscribe.html?success=true",
            "cancel_url": "www.jpressocoffee.com/jpresso-subscribe.html?cancelled=true",
            "shipping_address_collection": {
                "allowed_countries": ["MY"],  # Malaysia only (add more if needed)
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
                        "fixed_amount": {"amount": 1500, "currency": "myr"},  # RM15
                        "display_name": "East Malaysia (Sabah & Sarawak)",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 5},
                            "maximum": {"unit": "business_day", "value": 10},
                        },
                    },
                },
            ],
        }

        # Add customer email if provided
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
    """
    Creates a Stripe Checkout Session for subscription plans.
    
    For subscriptions, you need to create Products + Prices in Stripe Dashboard first:
    1. Go to https://dashboard.stripe.com/products
    2. Click "+ Add product"
    3. Name: "Single Origin Explorer - Weekly" 
    4. Price: RM55, Recurring, Every week
    5. Save → copy the Price ID (price_xxxxx)
    6. Repeat for all 9 plans (3 tiers × 3 frequencies)
    
    Then map them below:
    """
    
    # ═══ REPLACE THESE WITH YOUR REAL STRIPE PRICE IDs ═══
    SUBSCRIPTION_PRICES = {
        "so-weekly":   "price_REPLACE_WITH_REAL_ID",   # Single Origin Weekly RM55
        "so-biweekly": "price_REPLACE_WITH_REAL_ID",   # Single Origin Biweekly RM50
        "so-monthly":  "price_REPLACE_WITH_REAL_ID",   # Single Origin Monthly RM45
        "bl-weekly":   "price_REPLACE_WITH_REAL_ID",   # Blend Weekly RM48
        "bl-biweekly": "price_REPLACE_WITH_REAL_ID",   # Blend Biweekly RM44
        "bl-monthly":  "price_REPLACE_WITH_REAL_ID",   # Blend Monthly RM40
        "es-weekly":   "price_REPLACE_WITH_REAL_ID",   # Espresso Weekly RM58
        "es-biweekly": "price_REPLACE_WITH_REAL_ID",   # Espresso Biweekly RM52
        "es-monthly":  "price_REPLACE_WITH_REAL_ID",   # Espresso Monthly RM48
    }

    try:
        data = request.get_json()
        plan_id = data.get("plan_id")  # e.g., "so-weekly"
        
        price_id = SUBSCRIPTION_PRICES.get(plan_id)
        if not price_id or "REPLACE" in price_id:
            return jsonify({"error": f"Subscription '{plan_id}' not configured. Create the price in Stripe Dashboard first."}), 400

        session = stripe.checkout.Session.create(
            payment_method_types=["card", "fpx"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url="www.jpressocoffee.com/jpresso-subscribe.html?sub=success",
            cancel_url="www.jpressocoffee.com/jpresso-subscribe.html?sub=cancelled",
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


# ═══════════════════════════════════════════════════════════
# requirements.txt (create this file in the same repo):
# ═══════════════════════════════════════════════════════════
#
# flask==3.0.0
# flask-cors==4.0.0
# stripe==7.0.0
# gunicorn==21.2.0
#
# ═══════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════
# FRONTEND CODE — Replace the checkout button handler
# ═══════════════════════════════════════════════════════════
#
# In your jpresso-subscribe.jsx, replace the alert() in the
# CartDrawer checkout button with this:
#
#   const handleCheckout = async () => {
#     const items = cart.map(item => ({
#       name: item.name,
#       price: item.unitPrice,
#       quantity: item.isGreen ? item.kgQty : item.qty,
#       description: item.isGreen 
#         ? `${item.process} · ${item.tierLabel} · Green Bean`
#         : item.isEquip 
#           ? item.cat
#           : `${item.process} · 200g`,
#       type: item.isGreen ? "green" : item.isEquip ? "equip" : "roasted"
#     }));
#     
#     try {
#       const res = await fetch("https://YOUR-RENDER-URL.onrender.com/create-checkout-session", {
#         method: "POST",
#         headers: { "Content-Type": "application/json" },
#         body: JSON.stringify({ items })
#       });
#       const data = await res.json();
#       if (data.url) {
#         window.location.href = data.url;
#       } else {
#         alert("Error: " + (data.error || "Unknown error"));
#       }
#     } catch (err) {
#       alert("Network error. Please try again.");
#     }
#   };
#
#
# For subscription buttons, replace the alert() with:
#
#   const handleSubscribe = async (tierId, freq) => {
#     try {
#       const res = await fetch("https://YOUR-RENDER-URL.onrender.com/create-subscription-session", {
#         method: "POST",
#         headers: { "Content-Type": "application/json" },
#         body: JSON.stringify({ plan_id: `${tierId}-${freq}` })
#       });
#       const data = await res.json();
#       if (data.url) {
#         window.location.href = data.url;
#       } else {
#         alert(data.error || "Error creating subscription");
#       }
#     } catch (err) {
#       alert("Network error. Please try again.");
#     }
#   };
#
# ═══════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════
# RENDER SETUP (render.yaml — optional, for Blueprint deploy)
# ═══════════════════════════════════════════════════════════
#
# services:
#   - type: web
#     name: jpresso-checkout
#     runtime: python
#     buildCommand: pip install -r requirements.txt
#     startCommand: gunicorn app:app
#     envVars:
#       - key: STRIPE_SECRET_KEY
#         sync: false
#
# ═══════════════════════════════════════════════════════════
