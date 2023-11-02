# Install Module start
import importlib
import subprocess
import sys

def check_and_install_module(module_name):
    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"The '{module_name}' module is not installed. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

# List of required modules
required_modules = ["faker", "scikit-learn", "numpy", "pandas","tabulate"]

# Check and install missing modules
for module_name in required_modules:
    check_and_install_module(module_name)

# Install Module stop

import json
import random
import faker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from tabulate import tabulate
from collections import defaultdict
from collections import Counter

# Initialize the Faker library
fake = faker.Faker()

# Create a list to store user data
users = []

# Define a list of departments
departments = ["Engineering", "Marketing", "Sales", "Finance", "HR", "IT"]

# Define a list of entitlements
entitlements = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"]

# Generate user entries
for user_id in range(1, 2000):
    user = {
        "id": user_id,
        "username": fake.user_name(),
        "email": fake.email(),
        "created_at": fake.date_time_this_decade().isoformat(),
        "entitlements": random.sample(entitlements, random.randint(1, len(entitlements))),
        "department": random.choice(departments)
    }
    users.append(user)

# Create a dictionary with the user data
data = {"users": users}

# Save the data to a JSON file in your VSCode workspace
with open("user_entitlements_data.json", "w") as json_file:
    json.dump(data, json_file, indent=2)

print("User data generated and saved to user_entitlements_data.json")

# Load the user entitlement data from the JSON file in your local workspace
with open('user_entitlements_data.json', 'r') as json_file:
    data = json.load(json_file)


# Preprocess data and create a feature matrix
user_attributes = [f"{user['department']} {' '.join(user['entitlements'])}" for user in data['users']]

# Initialize and train a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(user_attributes)

# Compute similarity scores
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)



# Replace user_id with the desired user's index
user_id = 0

# Create a dictionary to store recommendations, grouped by department
department_recommendations = defaultdict(list)

# Create a dictionary to keep track of the number of users with the same department and entitlements
user_count_by_department_entitlements = defaultdict(int)

# Create a set to keep track of unique department and entitlement combinations
unique_recommendations = set()

# Iterate through all users to find department-specific recommendations and count users with the same department and entitlements
for user in data["users"]:
    department = user["department"]
    entitlements = tuple(sorted(user["entitlements"]))  # Sort entitlements for consistent comparison
    unique_key = (department, entitlements)

    user_count_by_department_entitlements[unique_key] += 1

    # Check if this is the first occurrence of this department and entitlement combination
    if user_count_by_department_entitlements[unique_key] == 1:
        unique_recommendations.add(unique_key)

# Iterate through the recommendations and populate the count based on the user_count_by_department_entitlements
for unique_key in unique_recommendations:
    department, entitlements = unique_key
    count = user_count_by_department_entitlements[unique_key]
    department_recommendations[department].append((department, list(entitlements), count))

# Create a nicely formatted table
sorted_recommendations = []
for department in department_recommendations:
    sorted_recommendations.extend(department_recommendations[department])

table = tabulate(sorted_recommendations, headers=["Department", "Entitlements", "Count"], tablefmt="pretty")

print("Recommended Roles for User:")
print(table)


# Load the user entitlement data from the JSON file
with open('user_entitlements_data.json', 'r') as json_file:
    data = json.load(json_file)

# Group users by department
department_users = {dept: [] for dept in departments}
for user in data['users']:
    department = user.get('department', 'Unknown')  # Use 'Unknown' if department is not provided
    department_users[department].append(user)

# Define a function to recommend entitlements for each department
def recommend_entitlements_by_department(users_in_department):
    all_entitlements = []
    for user in users_in_department:
        user_entitlements = user.get('entitlements', [])
        all_entitlements.extend(user_entitlements)

    # Calculate the most common entitlements in the department
    entitlement_counts = Counter(all_entitlements)
    total_users = len(users_in_department)
    recommended_entitlements = []

    for ent, count in entitlement_counts.most_common(5):
        percentage = (count / total_users) * 100
        recommended_entitlements.append((ent, percentage))

    return recommended_entitlements

# Generate department-specific recommendations
department_recommendations = {}
for department in departments:
    users_in_department = department_users.get(department, [])
    recommended_entitlements = recommend_entitlements_by_department(users_in_department)
    department_recommendations[department] = recommended_entitlements

# Print the department-specific recommendations with confirmation percentages
for department, recommendations in department_recommendations.items():
    print(f"Recommendations for Department '{department}':")
    for i, (entitlement, percentage) in enumerate(recommendations, start=1):
        print(f"{i}. {entitlement}: {percentage:.2f}% confirmation")
    print()
