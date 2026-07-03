"""
Generates a realistic synthetic restaurant reviews dataset (Yelp-style)
for the CodeAlpha Data Analytics internship project.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

N = 650

restaurant_names = [
    "The Spice Route", "Golden Dragon", "Bella Napoli", "Taco Fiesta", "Sushi Zen",
    "The Burger Joint", "Curry House", "Le Petit Bistro", "Ocean Grill", "Pasta Palace",
    "Green Leaf Cafe", "Smoky BBQ Pit", "Coastal Kitchen", "Urban Tandoor", "Noodle Bar",
    "The Pizza Cellar", "Saffron Table", "Blue Lotus", "Rustic Oven", "Chai & Chaat"
]
cuisines = {
    "The Spice Route": "Indian", "Golden Dragon": "Chinese", "Bella Napoli": "Italian",
    "Taco Fiesta": "Mexican", "Sushi Zen": "Japanese", "The Burger Joint": "American",
    "Curry House": "Indian", "Le Petit Bistro": "French", "Ocean Grill": "Seafood",
    "Pasta Palace": "Italian", "Green Leaf Cafe": "Vegan", "Smoky BBQ Pit": "American",
    "Coastal Kitchen": "Seafood", "Urban Tandoor": "Indian", "Noodle Bar": "Chinese",
    "The Pizza Cellar": "Italian", "Saffron Table": "Indian", "Blue Lotus": "Thai",
    "Rustic Oven": "Italian", "Chai & Chaat": "Indian"
}
cities = ["Ahmedabad", "Mumbai", "Delhi", "Bengaluru", "Pune", "Chennai", "Hyderabad", "Jaipur"]

positive_phrases = [
    "The food was absolutely delicious and beautifully presented.",
    "Amazing service, our server was attentive and friendly.",
    "Best meal I've had in months, will definitely come back!",
    "The ambiance was cozy and the staff made us feel welcome.",
    "Fresh ingredients and bold flavors, highly recommend this place.",
    "Portion sizes were generous and the prices were very fair.",
    "The chef clearly knows what they're doing, every dish was perfect.",
    "Quick service even though the place was packed.",
    "Loved the dessert menu, the tiramisu was outstanding.",
    "A hidden gem, the flavors were authentic and comforting.",
    "Great spot for a family dinner, kids loved it too.",
    "The staff went above and beyond to accommodate our allergies.",
]
negative_phrases = [
    "The food was cold by the time it reached our table.",
    "Service was extremely slow and the staff seemed disinterested.",
    "Way overpriced for the quality and quantity we received.",
    "The place was dirty and the tables hadn't been cleaned properly.",
    "Our order was wrong and it took forever to get it corrected.",
    "The food was bland and lacked any real seasoning.",
    "We waited over an hour despite having a reservation.",
    "The restaurant was too noisy and cramped to enjoy the meal.",
    "I found a hair in my food and the manager barely apologized.",
    "Definitely not worth the hype, quite disappointing overall.",
    "The portions were tiny for the price we paid.",
    "Parking was a nightmare and the staff was rude at the entrance.",
]
neutral_phrases = [
    "The food was okay, nothing special but not bad either.",
    "Average experience overall, might try another dish next time.",
    "Decent place for a quick bite if you're in the area.",
    "Service was fine, food took a bit longer than expected.",
    "It's a standard restaurant, does the job but nothing memorable.",
    "The ambiance was nice but the food was just average.",
    "Reasonable prices, the menu could use more variety though.",
    "Not the best, not the worst, a fairly typical dining experience.",
]

def make_review_text(rating):
    if rating >= 4:
        pool = positive_phrases
        n = random.choice([1, 2])
    elif rating == 3:
        pool = neutral_phrases
        n = random.choice([1, 2])
    else:
        pool = negative_phrases
        n = random.choice([1, 2])
    return " ".join(random.sample(pool, n))

def rating_from_bias(bias):
    # bias controls how positive a restaurant skews (0-1)
    r = np.random.normal(loc=2 + bias * 3, scale=1.0)
    r = int(round(min(5, max(1, r))))
    return r

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

restaurant_bias = {name: random.uniform(0.25, 0.9) for name in restaurant_names}

rows = []
for i in range(1, N + 1):
    name = random.choice(restaurant_names)
    bias = restaurant_bias[name]
    rating = rating_from_bias(bias)
    review_date = start_date + timedelta(days=random.randint(0, date_range_days))
    text = make_review_text(rating)
    review_len = len(text)
    rows.append({
        "review_id": i,
        "restaurant_name": name,
        "cuisine_type": cuisines[name],
        "city": random.choice(cities),
        "rating": rating,
        "review_text": text,
        "review_length": review_len,
        "review_date": review_date.strftime("%Y-%m-%d"),
    })

df = pd.DataFrame(rows)

# Inject a few realistic data quality issues for the EDA task to surface
missing_idx = np.random.choice(df.index, size=15, replace=False)
df.loc[missing_idx, "city"] = np.nan

dup_rows = df.sample(8, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

df["rating"] = df["rating"].astype(object)
messy_idx = df.sample(5, random_state=2).index
df.loc[messy_idx, "rating"] = df.loc[messy_idx, "rating"].apply(lambda r: str(r))  # inject stringified ratings
df.loc[df.sample(5, random_state=3).index, "review_text"] = ""

df.to_csv("/home/claude/CodeAlpha_DataAnalytics/data/restaurant_reviews.csv", index=False)
print("Dataset generated:", df.shape)
print(df.head())
