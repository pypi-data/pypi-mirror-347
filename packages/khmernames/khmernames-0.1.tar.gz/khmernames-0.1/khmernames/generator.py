import random
import pandas as pd

male_first_names = ['វិចិត្រ', 'សុភ័ក្រ', 'សំអុន', 'ព្រហ្ម', 'សុភា']
female_first_names = ['ស្រីនី', 'សុឆារ៉ា', 'ម៉ាលីន', 'ស្រីស្អាត', 'សុភាព']
last_names = ['ជា', 'ប៉ា', 'សុខ', 'អេង', 'ថោង', 'ពៅ', 'លី', 'សេង']

def get_first_name(gender='random'):
    if gender == 'male':
        return random.choice(male_first_names)
    elif gender == 'female':
        return random.choice(female_first_names)
    return random.choice(male_first_names + female_first_names)

def get_last_name():
    return random.choice(last_names)

def get_full_name(gender='random'):
    return f"{get_last_name()} {get_first_name(gender)}"

def generate_bulk_names(count=1000):
    results = []
    for _ in range(count):
        gender = random.choice(['male', 'female'])
        first = get_first_name(gender)
        last = get_last_name()
        results.append({
            'Full Name': f"{last} {first}",
            'First Name': first,
            'Last Name': last,
            'Gender': gender
        })
    return results

def export_to_excel(data, filename='khmer_names.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def export_to_txt(data, filename='khmer_names.txt'):
    with open(filename, "w", encoding="utf-8") as f:
        for row in data:
            f.write(row['Full Name'] + "\n")
