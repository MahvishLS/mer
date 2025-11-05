from datetime import datetime, timedelta

PRODUCTS = {
    "wired earphones": {"warranty_days": 365, "info": "Wired earphones with noise cancellation."},
    "wireless earphones": {"warranty_days": 365, "info": "Wireless earphones with Bluetooth 5.0."},
    "smart watch": {"warranty_days": 730, "info": "Smart watch with heart rate monitor and GPS."},
    "speakers": {"warranty_days": 365, "info": "Portable Bluetooth speakers with 10h battery."},
    "charger": {"warranty_days": 180, "info": "Fast charging USB-C charger."}
}

def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["claim", "broken", "issue", "problem", "not working"]):
        return "file_claim"
    elif any(word in text for word in ["warranty", "guarantee", "valid", "expired"]):
        return "check_warranty"
    elif any(word in text for word in ["info", "information", "details", "specs"]):
        return "product_info"
    else:
        return "unknown"

SLOT_PROMPTS = {
    "file_claim": ["Which product is affected?", "Please describe the issue:", "When did you purchase it? (YYYY-MM-DD)"],
    "check_warranty": ["Which product do you want to check?", "When did you purchase it? (YYYY-MM-DD)"],
    "product_info": ["Which product do you want info about?"]
}

TEMPLATES = {
    "file_claim": "Thanks! We've registered your claim for {product_name} with issue: {issue_description}.",
    "check_warranty": "Your warranty status for {product_name} purchased on {purchase_date} is: {warranty_status}.",
    "product_info": "Here is the info for product {product_name}: {product_info}",
    "fallback": "Sorry, I didn't understand. Can you please rephrase?",
    "invalid_product": "Sorry, we don't have information about that product. Please choose from: {}."
}

def validate_product(product_name):
    product_name = product_name.lower()

    for p in PRODUCTS.keys():
        if product_name == p:
            return p

    for p in PRODUCTS.keys():
        if product_name in p or p in product_name:
            return p
    return None

def check_warranty_status(product_name, purchase_date_str):
    try:
        purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d")
    except ValueError:
        return "INVALID_DATE"

    warranty_days = PRODUCTS[product_name]["warranty_days"]
    expiry_date = purchase_date + timedelta(days=warranty_days)
    today = datetime.today()

    if today <= expiry_date:
        return "ACTIVE (expires on {})".format(expiry_date.strftime("%Y-%m-%d"))
    else:
        return "EXPIRED (expired on {})".format(expiry_date.strftime("%Y-%m-%d"))

def respond(intent, context):
    if intent == "file_claim":

        status = check_warranty_status(context["product_name"], context["purchase_date"])
        if status == "INVALID_DATE":
            warranty_msg = " (But the purchase date format was invalid for warranty check.)"
        else:
            warranty_msg = f" Warranty status: {status}."
        return TEMPLATES[intent].format(**context) + warranty_msg

    elif intent == "check_warranty":
        status = check_warranty_status(context["product_name"], context["purchase_date"])
        if status == "INVALID_DATE":
            return "Invalid purchase date format. Please use YYYY-MM-DD."
        context["warranty_status"] = status
        context["product_info"] = PRODUCTS[context["product_name"]]["info"]
        return TEMPLATES[intent].format(**context)

    elif intent == "product_info":
        context["product_info"] = PRODUCTS[context["product_name"]]["info"]
        return TEMPLATES[intent].format(**context)

    return TEMPLATES["fallback"]


context = {}
current_intent = None
slot_index = 0

print("Warranty Support Bot: Hi! How can I assist you? (Type 'exit' to quit)")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit", "okay", "thanks"):
        print("Bot: Goodbye!")
        break

    if current_intent:

        slot_key = list(context.keys())[slot_index]

        # Special validation for product name slot
        if slot_key == "product_name":
            valid_product = validate_product(user_input)
            if not valid_product:
                print("Bot:", TEMPLATES["invalid_product"].format(", ".join(PRODUCTS.keys())))
                continue
            else:
                context[slot_key] = valid_product
        else:
            context[slot_key] = user_input

        slot_index += 1
        if slot_index < len(SLOT_PROMPTS[current_intent]):
            print("Bot:", SLOT_PROMPTS[current_intent][slot_index])
        else:
            print("Bot:", respond(current_intent, context))
            current_intent = None
            context = {}
    else:
        intent = detect_intent(user_input)
        if intent == "unknown":
            print("Bot:", TEMPLATES["fallback"])
        else:
            current_intent = intent

            if intent == "file_claim":
                context = {"product_name": "", "issue_description": "", "purchase_date": ""}
            elif intent == "check_warranty":
                context = {"product_name": "", "purchase_date": ""}
            elif intent == "product_info":
                context = {"product_name": ""}
            slot_index = 0
            print("Bot:", SLOT_PROMPTS[intent][slot_index])
