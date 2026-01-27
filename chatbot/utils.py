KEYWORDS = {
    "products": [
        "pizza", "pizzas", "burger", "burgers", "sushi", 
        "roll", "rolls", "wrap", "wraps", "sandwich", "sandwiches",
        "pasta", "noodles", "rice", "biryani", "fried rice"
    ],
    "pizza_types": [
        "margherita", "pepperoni", "cheese", "veggie", "supreme",
        "bbq", "hawaiian", "thin crust", "stuffed crust", "pan pizza"
    ],
    "burger_types": [
        "veg burger", "chicken burger", "beef burger", "cheese burger",
        "double patty", "crispy chicken", "grilled", "spicy"
    ],
    "sushi_types": [
        "sushi", "nigiri", "maki", "california roll", "salmon",
        "tuna", "tempura", "dragon roll", "philadelphia roll"
    ],
    "rolls_wraps": [
        "chicken roll", "paneer roll", "egg roll", "veg roll",
        "shawarma", "kebab roll", "falafel", "spring roll"
    ],
    "seafood": [
        "seafood", "fish", "prawn", "prawns", "shrimp", "crab",
        "lobster", "salmon", "tuna", "fish fry", "grilled fish"
    ],
    "vegetarian": [
        "veg", "vegetarian", "paneer", "tofu", "veggie",
        "plant based", "mushroom", "falafel", "vegan"
    ],
    "sides": [
        "fries", "french fries", "wedges", "nuggets", "wings",
        "salad", "soup", "garlic bread", "coleslaw", "onion rings"
    ],
    "beverages": [
        "drink", "drinks", "coke", "pepsi", "juice", "shake",
        "milkshake", "smoothie", "coffee", "tea", "water"
    ],
    "availability": [
        "available", "stock", "in stock", "out of stock",
        "fresh", "hot", "ready", "menu"
    ],
    "pricing": [
        "price", "cost", "rate", "expensive", "cheap", "offer",
        "discount", "deal", "combo", "meal"
    ],
    "ordering": [
        "order", "buy", "delivery", "takeaway", "pickup",
        "home delivery", "cash on delivery", "cod", "online payment"
    ],
    "dietary": [
        "spicy", "mild", "extra cheese", "no onion", "no garlic",
        "gluten free", "dairy free", "halal", "jain"
    ],
    "offers": [
        "offer", "offers", "deal", "deals", "discount", "promo",
        "coupon", "special", "combo", "buy one get one", "bogo"
    ],
    "occasions": [
        "party", "birthday", "office", "bulk order", "catering",
        "family pack", "group order"
    ]
}

GREETINGS = [
    "hi", "hello", "hey", "hai",
    "good morning", "good afternoon", "good evening",
    "greetings", "howdy", "namaste"
]

def is_food_query(message: str) -> bool:
    msg = message.lower()

    for category, words in KEYWORDS.items():
        for word in words:
            if word in msg:
                return True

    return False

def is_greeting(message: str) -> bool:
    msg = message.lower().strip()
    return any(
        msg == g or msg.startswith(g + " ")
        for g in GREETINGS
    )

def greeting_response() -> str:
    return (
        "Hello and welcome! 🍕🍔 "
        "Are you craving pizza, burgers, sushi, rolls, or checking our special offers today?"
    )
