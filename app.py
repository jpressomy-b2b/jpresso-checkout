from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import stripe
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=[
    "https://bloomdaily.io",
    "https://www.bloomdaily.io",
    "https://jpressocoffee.com",
    "https://www.jpressocoffee.com",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
])

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
ADMIN_KEY = os.environ.get("ADMIN_KEY", "jpresso2026")
GMAIL_USER = os.environ.get("GMAIL_USER", "jpresso.my@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "jpresso.my@gmail.com")

SITE_URL = "https://bloomdaily.io"
RETURN_PAGE = f"{SITE_URL}/subscribe.html"


def send_order_email(session_data):
    if not GMAIL_APP_PASSWORD:
        print("[EMAIL] Skipped - GMAIL_APP_PASSWORD not set")
        return
    try:
        sd = session_data.get("shipping_details") or {}
        addr = sd.get("address", {}) if isinstance(sd, dict) else {}
        cd = session_data.get("customer_details") or {}
        name = sd.get("name", "") or cd.get("name", "Unknown")
        email = cd.get("email", "")
        phone = cd.get("phone", "")
        amount = session_data.get("amount_total", 0) / 100
        order_id = session_data.get("id", "")[-8:].upper()
        created = datetime.fromtimestamp(session_data.get("created", 0)).strftime("%d %b %Y, %I:%M %p")
        address_str = ", ".join(filter(None, [addr.get("line1", ""), addr.get("line2", ""), addr.get("postal_code", ""), addr.get("city", ""), addr.get("state", "")]))
        mode = session_data.get("mode", "payment")
        label_url = f"https://jpresso-checkout.onrender.com/admin/label/{session_data.get('id', '')}?key={ADMIN_KEY}"

        items_text = ""
        try:
            full_session = stripe.checkout.Session.retrieve(session_data.get("id"), expand=["line_items"])
            if full_session.line_items:
                for li in full_session.line_items.data:
                    items_text += f"  - {li.description} x{li.quantity} (RM{li.amount_total / 100:.2f})\n"
        except Exception:
            items_text = "  (Could not fetch items)\n"

        subject = f"New Order #{order_id} - RM{amount:.2f} - {name}"

        body_html = f"""
<div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;color:#333">
<div style="background:#4E1F73;color:#fff;padding:16px 20px;border-radius:8px 8px 0 0">
<h2 style="margin:0;font-size:18px;letter-spacing:2px">NEW ORDER RECEIVED</h2>
</div>
<div style="border:1px solid #e8dff0;border-top:none;padding:20px;border-radius:0 0 8px 8px">
<table style="width:100%;font-size:14px;margin-bottom:16px">
<tr><td style="color:#888;padding:4px 0">Order ID</td><td style="font-weight:700;color:#4E1F73">#{order_id}</td></tr>
<tr><td style="color:#888;padding:4px 0">Date</td><td>{created}</td></tr>
<tr><td style="color:#888;padding:4px 0">Type</td><td>{"Subscription" if mode == "subscription" else "One-time purchase"}</td></tr>
<tr><td style="color:#888;padding:4px 0">Total</td><td style="font-weight:700;font-size:18px;color:#4E1F73">RM{amount:.2f}</td></tr>
</table>
<div style="background:#f8f5f1;border-radius:6px;padding:14px;margin-bottom:14px">
<div style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#999;margin-bottom:6px;font-weight:600">Customer</div>
<div style="font-size:15px;font-weight:700;color:#4E1F73">{name}</div>
<div style="font-size:13px">{email}</div>
{f'<div style="font-size:13px">Tel: {phone}</div>' if phone else ''}
</div>
<div style="background:#f8f5f1;border-radius:6px;padding:14px;margin-bottom:14px">
<div style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#999;margin-bottom:6px;font-weight:600">Ship To</div>
<div style="font-size:13px;line-height:1.6">{address_str or 'No address provided'}</div>
</div>
<div style="background:#f8f5f1;border-radius:6px;padding:14px;margin-bottom:14px">
<div style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#999;margin-bottom:6px;font-weight:600">Items Ordered</div>
<pre style="font-family:Arial,sans-serif;font-size:13px;margin:0;white-space:pre-wrap">{items_text or '(No items)'}</pre>
</div>
<a href="{label_url}" style="display:inline-block;padding:12px 24px;background:#DAB07B;color:#2D1145;text-decoration:none;border-radius:6px;font-weight:700;font-size:13px;letter-spacing:1px">PRINT SHIPPING LABEL</a>
<p style="font-size:11px;color:#999;margin-top:16px">This email was sent automatically by Bloom Daily. <a href="https://jpresso-checkout.onrender.com/admin?key={ADMIN_KEY}" style="color:#4E1F73">View all orders</a></p>
</div>
</div>"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Bloom Daily Orders <{GMAIL_USER}>"
        msg["To"] = NOTIFY_EMAIL
        msg.attach(MIMEText(f"New Order #{order_id}\nCustomer: {name}\nEmail: {email}\nTotal: RM{amount:.2f}\nAddress: {address_str}\n\nItems:\n{items_text}\nPrint label: {label_url}", "plain"))
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())

        print(f"[EMAIL] Sent order notification #{order_id} to {NOTIFY_EMAIL}")

    except Exception as e:
        print(f"[EMAIL] Failed: {str(e)}")


def get_or_create_customer(email):
    customers = stripe.Customer.list(email=email, limit=1)
    if customers.data:
        return customers.data[0]
    return stripe.Customer.create(email=email)


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
            {"shipping_rate_data": {"type": "fixed_amount", "fixed_amount": {"amount": 0, "currency": "myr"}, "display_name": "Free Shipping (Peninsular MY)", "delivery_estimate": {"minimum": {"unit": "business_day", "value": 3}, "maximum": {"unit": "business_day", "value": 5}}}},
            {"shipping_rate_data": {"type": "fixed_amount", "fixed_amount": {"amount": 1500, "currency": "myr"}, "display_name": "East Malaysia (Sabah & Sarawak) - RM15", "delivery_estimate": {"minimum": {"unit": "business_day", "value": 5}, "maximum": {"unit": "business_day", "value": 10}}}},
        ]
    if green_kg >= 60:
        pen_amount, pen_label = 0, f"Free Shipping (Peninsular MY) - {green_kg}kg"
    elif green_kg >= 30:
        pen_amount, pen_label = 6000, f"Peninsular MY - RM60 ({green_kg}kg)"
    elif green_kg >= 10:
        pen_amount, pen_label = 4000, f"Peninsular MY - RM40 ({green_kg}kg)"
    elif green_kg >= 5:
        pen_amount, pen_label = 2500, f"Peninsular MY - RM25 ({green_kg}kg)"
    else:
        pen_amount, pen_label = 1500, f"Peninsular MY - RM15 ({green_kg}kg)"
    options = [{"shipping_rate_data": {"type": "fixed_amount", "fixed_amount": {"amount": pen_amount, "currency": "myr"}, "display_name": pen_label, "delivery_estimate": {"minimum": {"unit": "business_day", "value": 3}, "maximum": {"unit": "business_day", "value": 7}}}}]
    if green_kg < 30:
        if green_kg >= 10:
            em_amount, em_label = 15000, f"East Malaysia - RM150 ({green_kg}kg)"
        elif green_kg >= 5:
            em_amount, em_label = 8000, f"East Malaysia - RM80 ({green_kg}kg)"
        else:
            em_amount, em_label = 5000, f"East Malaysia - RM50 ({green_kg}kg)"
        options.append({"shipping_rate_data": {"type": "fixed_amount", "fixed_amount": {"amount": em_amount, "currency": "myr"}, "display_name": em_label, "delivery_estimate": {"minimum": {"unit": "business_day", "value": 5}, "maximum": {"unit": "business_day", "value": 10}}}})
    else:
        options.append({"shipping_rate_data": {"type": "fixed_amount", "fixed_amount": {"amount": 0, "currency": "myr"}, "display_name": "East Malaysia (30kg+) - Contact us for quote", "delivery_estimate": {"minimum": {"unit": "business_day", "value": 7}, "maximum": {"unit": "business_day", "value": 14}}}})
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
            line_items.append({"price_data": {"currency": "myr", "unit_amount": unit_amount, "product_data": {"name": item["name"], "description": item.get("description", "")}}, "quantity": item["quantity"]})
        shipping_options = get_shipping_options(items)
        session_params = {"payment_method_types": ["card"], "line_items": line_items, "mode": "payment", "success_url": f"{RETURN_PAGE}?success=true", "cancel_url": f"{RETURN_PAGE}?cancelled=true", "shipping_address_collection": {"allowed_countries": ["MY"]}, "shipping_options": shipping_options}
        if customer_email:
            customer = get_or_create_customer(customer_email)
            session_params["customer"] = customer.id
        else:
            session_params["customer_creation"] = "always"
        session = stripe.checkout.Session.create(**session_params)
        return jsonify({"url": session.url})
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Pricing for dynamic subscription creation
# Base prices match frontend SUB_PRICES
SUB_BASE_PRICES = {
    "Jpresso Roastery": {"filter": {"base": 66, "disc": 0.05}, "espresso": {"base": 50, "disc": 0.10}},
    "LewisGene": {"filter": {"base": 45, "disc": 0.10}, "espresso": {"base": 45, "disc": 0.10}},
    "Richman": {"filter": {"base": 80, "disc": 0.10}, "espresso": {"base": 80, "disc": 0.10}},
}


@app.route("/create-subscription-session", methods=["POST"])
def create_subscription_session():
    try:
        data = request.get_json()

        # New format: {roastery, roast, duration, months, quantity}
        roastery = data.get("roastery")
        roast = data.get("roast")
        duration = data.get("duration", "6m")
        months = data.get("months", 6)
        quantity = int(data.get("quantity", 1))

        # Legacy format support: {plan_id}
        plan_id = data.get("plan_id")
        if plan_id and not roastery:
            # Map old plan IDs to new format
            legacy_map = {
                "so-monthly": ("Jpresso Roastery", "filter"),
                "es-monthly": ("Jpresso Roastery", "espresso"),
                "bl-monthly": ("Jpresso Roastery", "filter"),
            }
            if plan_id in legacy_map:
                roastery, roast = legacy_map[plan_id]
                duration = "6m"
                months = 6
                quantity = 1

        if not roastery or not roast:
            return jsonify({"error": "Missing roastery or roast selection"}), 400

        pricing = SUB_BASE_PRICES.get(roastery, {}).get(roast)
        if not pricing:
            return jsonify({"error": f"Pricing not configured for {roastery} {roast}"}), 400

        # Calculate monthly price (with discount applied, rounded)
        monthly_price = round(pricing["base"] * (1 - pricing["disc"]))
        unit_amount = monthly_price * 100 * quantity  # in sen

        # Build dynamic subscription product name
        roast_label = "Filter Roast" if roast == "filter" else "Espresso Roast"
        duration_label = {"3m": "3 Months", "6m": "6 Months", "12m": "12 Months"}.get(duration, f"{months} Months")
        bags_label = f"{quantity} bag{'s' if quantity > 1 else ''} x 250g"
        product_name = f"{roastery} - {roast_label} Subscription"
        product_desc = f"{bags_label} per month, {duration_label} commitment"

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "myr",
                    "unit_amount": unit_amount,
                    "recurring": {"interval": "month"},
                    "product_data": {
                        "name": product_name,
                        "description": product_desc,
                    },
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{RETURN_PAGE}?sub=success",
            cancel_url=f"{RETURN_PAGE}?sub=cancelled",
            subscription_data={
                "metadata": {
                    "roastery": roastery,
                    "roast": roast,
                    "duration": duration,
                    "months": str(months),
                    "quantity": str(quantity),
                }
            },
        )
        return jsonify({"url": session.url})
    except stripe.error.StripeError as e:
        return jsonify({"error": f"Stripe error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/create-portal-session", methods=["POST"])
def create_portal_session():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        if not email:
            return jsonify({"error": "Please enter your email address"}), 400
        customers = stripe.Customer.list(email=email, limit=1)
        if not customers.data:
            return jsonify({"error": "No account found with this email."}), 404
        customer = customers.data[0]
        session = stripe.billing_portal.Session.create(customer=customer.id, return_url=RETURN_PAGE)
        return jsonify({"url": session.url})
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        if WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
        else:
            event = json.loads(payload)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return jsonify({"error": str(e)}), 400
    if event.get("type") == "checkout.session.completed":
        session_data = event["data"]["object"]
        print(f"[ORDER] New: {session_data.get('id')} | {session_data.get('customer_details', {}).get('email', 'N/A')} | RM{session_data.get('amount_total', 0) / 100:.2f}")
        send_order_email(session_data)
    return jsonify({"status": "ok"}), 200


@app.route("/admin/orders", methods=["GET"])
def admin_orders():
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        limit = min(int(request.args.get("limit", 20)), 100)
        sessions = stripe.checkout.Session.list(limit=limit, expand=["data.line_items"])
        orders = []
        for s in sessions.data:
            if s.payment_status != "paid":
                continue
            shipping = s.shipping_details or {}
            address = shipping.get("address", {}) if isinstance(shipping, dict) else {}
            cd = s.customer_details or {}
            items = []
            if s.line_items:
                for li in s.line_items.data:
                    items.append({"name": li.description or "", "quantity": li.quantity, "amount": li.amount_total / 100})
            orders.append({"id": s.id, "created": datetime.fromtimestamp(s.created).strftime("%Y-%m-%d %H:%M"), "email": cd.get("email", ""), "name": shipping.get("name", "") or cd.get("name", ""), "phone": cd.get("phone", ""), "address": {"line1": address.get("line1", ""), "line2": address.get("line2", ""), "city": address.get("city", ""), "state": address.get("state", ""), "postal_code": address.get("postal_code", ""), "country": address.get("country", "MY")}, "total": s.amount_total / 100 if s.amount_total else 0, "items": items, "mode": s.mode})
        return jsonify({"orders": orders})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/label/<session_id>", methods=["GET"])
def admin_label(session_id):
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        return "Unauthorized", 401
    try:
        session = stripe.checkout.Session.retrieve(session_id, expand=["line_items"])
        shipping = session.shipping_details or {}
        address = shipping.get("address", {}) if isinstance(shipping, dict) else {}
        cd = session.customer_details or {}
        items = []
        if session.line_items:
            for li in session.line_items.data:
                items.append({"name": li.description, "qty": li.quantity})
        name = shipping.get("name", "") or cd.get("name", "")
        email = cd.get("email", "")
        phone = cd.get("phone", "")
        line1 = address.get("line1", "")
        line2 = address.get("line2", "")
        city = address.get("city", "")
        state = address.get("state", "")
        postal = address.get("postal_code", "")
        order_date = datetime.fromtimestamp(session.created).strftime("%d %b %Y, %I:%M %p")
        order_id = session.id[-8:].upper()
        items_rows = "".join(f'<tr><td style="padding:6px 10px;border-bottom:1px solid #ddd;font-size:14px">{it["name"]}</td><td style="padding:6px 10px;border-bottom:1px solid #ddd;font-size:14px;text-align:center;font-weight:600">x{it["qty"]}</td></tr>' for it in items)
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Label #{order_id}</title>
<style>
@media print {{ body {{ margin:0 }} .no-print {{ display:none!important }} @page {{ size:A5 landscape; margin:10mm }} }}
body {{ font-family:'Segoe UI',Arial,sans-serif; margin:20px; color:#222 }}
.label {{ border:2.5px solid #333; border-radius:10px; padding:24px; max-width:600px; margin:0 auto }}
.hdr {{ display:flex; justify-content:space-between; align-items:center; border-bottom:2.5px solid #4E1F73; padding-bottom:14px; margin-bottom:16px }}
.logo {{ font-size:26px; font-weight:800; color:#4E1F73; letter-spacing:4px }}
.oid {{ text-align:right; font-size:12px; color:#666 }}
.oid strong {{ color:#333; font-size:15px; display:block }}
.stitle {{ font-size:10px; text-transform:uppercase; letter-spacing:2.5px; color:#999; margin-bottom:5px; font-weight:700 }}
.addr {{ font-size:16px; line-height:1.7; font-weight:500; margin-bottom:18px }}
.addr .nm {{ font-size:20px; font-weight:700; color:#4E1F73; margin-bottom:2px }}
table {{ width:100%; border-collapse:collapse }}
th {{ text-align:left; padding:8px 10px; background:#f3edf8; font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:#4E1F73; border-bottom:2px solid #4E1F73 }}
th:last-child {{ text-align:center }}
.from {{ font-size:12px; color:#888; line-height:1.6; margin-top:16px; padding-top:12px; border-top:1.5px dashed #ccc }}
.from strong {{ color:#555 }}
.btn {{ display:inline-block; margin:20px auto; padding:14px 36px; background:#4E1F73; color:#fff; border:none; border-radius:8px; font-size:15px; cursor:pointer; font-weight:700; letter-spacing:1px }}
.btn:hover {{ background:#6B3A94 }}
.ctr {{ text-align:center }}
</style></head><body>
<div class="ctr no-print"><button class="btn" onclick="window.print()">Print Shipping Label</button><br><br></div>
<div class="label">
<div class="hdr"><div class="logo">BLOOM DAILY</div><div class="oid"><strong>#{order_id}</strong>{order_date}</div></div>
<div class="stitle">Ship To</div>
<div class="addr"><div class="nm">{name}</div>{line1}<br>{(line2 + '<br>') if line2 else ''}{postal} {city}, {state}<br>Malaysia{('<br>Tel: ' + phone) if phone else ''}{('<br>' + email) if email else ''}</div>
<div class="stitle">Items ordered</div>
<table><tr><th>Product</th><th>Qty</th></tr>{items_rows}</table>
<div class="from"><strong>From:</strong> Big Jpresso Sdn Bhd | 29, Jalan Tembaga SD 5/2C, Bandar Sri Damansara, 52200 KL<br>Tel: +60 12-878 2876 | hello@bloomdaily.io</div>
</div></body></html>"""
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/admin", methods=["GET"])
def admin_page():
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        return "Unauthorized. Add ?key=YOUR_ADMIN_KEY to the URL.", 401
    return render_template_string(ADMIN_HTML, admin_key=key)


ADMIN_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Bloom Daily Admin - Orders</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',Arial,sans-serif;background:#f8f5f1;color:#2D1145}
.nav{background:#4E1F73;color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center}
.nav h1{font-size:16px;letter-spacing:3px;font-weight:600}
.nav span{font-size:11px;opacity:.7}
.ct{max-width:900px;margin:24px auto;padding:0 16px}
.ctl{display:flex;gap:8px;margin-bottom:18px;align-items:center}
.ctl select,.ctl button{padding:8px 14px;border-radius:6px;border:1px solid #ddd;font-size:12px;cursor:pointer}
.ctl button{background:#4E1F73;color:#fff;border:none;font-weight:600}
.ctl button:hover{background:#6B3A94}
.oc{background:#fff;border-radius:10px;border:1px solid #e8dff0;margin-bottom:12px;overflow:hidden;box-shadow:0 1px 4px rgba(78,31,115,.05)}
.oh{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;cursor:pointer;transition:background .2s}
.oh:hover{background:#f8f5f1}
.om{display:flex;gap:16px;align-items:center}
.oi{font-weight:700;color:#4E1F73;font-size:13px}
.od{font-size:11px;color:#888}
.on{font-size:13px;font-weight:500}
.ot{font-size:14px;font-weight:700;color:#4E1F73}
.ob{padding:0 18px 16px;display:none;border-top:1px solid #f0ebf5}
.ob.open{display:block;padding-top:14px}
.dg{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
.db{background:#f8f5f1;border-radius:6px;padding:10px 12px}
.db .l{font-size:9px;text-transform:uppercase;letter-spacing:1.5px;color:#999;margin-bottom:2px;font-weight:600}
.db .v{font-size:12px;line-height:1.5}
.it{width:100%;border-collapse:collapse;margin-bottom:12px}
.it th{text-align:left;padding:6px 8px;background:#f3edf8;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#4E1F73}
.it td{padding:6px 8px;border-bottom:1px solid #f0ebf5;font-size:12px}
.pb{display:inline-block;padding:8px 18px;background:#DAB07B;color:#2D1145;border:none;border-radius:5px;font-size:11px;font-weight:700;cursor:pointer;text-decoration:none;letter-spacing:1px}
.pb:hover{background:#C49A5E}
.em{text-align:center;padding:48px;color:#999;font-size:14px}
.bg{display:inline-block;padding:2px 8px;border-radius:100px;font-size:9px;font-weight:600}
.bg-p{background:#e6f5ec;color:#16a34a}
.bg-s{background:#f3edf8;color:#6B3A94}
</style></head><body>
<div class="nav"><h1>BLOOM DAILY ADMIN</h1><span>Orders & Shipping Labels</span></div>
<div class="ct">
<div class="ctl">
<select id="lim"><option value="10">Last 10</option><option value="20" selected>Last 20</option><option value="50">Last 50</option></select>
<button onclick="load()">Refresh</button>
</div>
<div id="out"><div class="em">Loading orders...</div></div>
</div>
<script>
const K="{{ admin_key }}",B=window.location.origin;
async function load(){
const el=document.getElementById("out");
el.innerHTML='<div class="em">Loading...</div>';
const l=document.getElementById("lim").value;
try{
const r=await fetch(B+"/admin/orders?key="+K+"&limit="+l);
const d=await r.json();
if(d.error){el.innerHTML='<div class="em">Error: '+d.error+'</div>';return}
if(!d.orders.length){el.innerHTML='<div class="em">No paid orders found.</div>';return}
let h="";
d.orders.forEach((o,i)=>{
const a=o.address,as=[a.line1,a.line2,[a.postal_code,a.city].filter(Boolean).join(" "),a.state].filter(Boolean).join(", ");
const bg=o.mode==="subscription"?'<span class="bg bg-s">Sub</span>':'<span class="bg bg-p">Paid</span>';
let ir="";o.items.forEach(t=>{ir+='<tr><td>'+t.name+'</td><td style="text-align:center">x'+t.quantity+'</td><td style="text-align:right">RM'+t.amount.toFixed(2)+'</td></tr>'});
h+='<div class="oc"><div class="oh" onclick="tog('+i+')"><div class="om"><span class="oi">#'+o.id.slice(-8).toUpperCase()+'</span><span class="od">'+o.created+'</span>'+bg+'</div><div style="display:flex;align-items:center;gap:12px"><span class="on">'+(o.name||o.email)+'</span><span class="ot">RM'+o.total.toFixed(2)+'</span></div></div><div class="ob" id="o-'+i+'"><div class="dg"><div class="db"><div class="l">Customer</div><div class="v"><strong>'+o.name+'</strong><br>'+o.email+(o.phone?'<br>'+o.phone:'')+'</div></div><div class="db"><div class="l">Ship To</div><div class="v">'+(as||'No address')+'</div></div></div><table class="it"><tr><th>Product</th><th style="text-align:center">Qty</th><th style="text-align:right">Amount</th></tr>'+ir+'</table><a class="pb" href="'+B+'/admin/label/'+o.id+'?key='+K+'" target="_blank">Print Label</a></div></div>'});
el.innerHTML=h}catch(e){el.innerHTML='<div class="em">Error: '+e.message+'</div>'}}
function tog(i){document.getElementById("o-"+i).classList.toggle("open")}
load();
</script></body></html>"""


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "stripe_configured": bool(stripe.api_key)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
