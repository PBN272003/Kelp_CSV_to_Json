import csv
from collections import defaultdict
from io import TextIOWrapper
import traceback
from .models import UserReportData
def flatten_row(row):
    result = {}
    for key, value in row.items():
        parts = key.strip().split(".")
        d = result
        for part in parts[:-1]:  # Drill down to nested level
            d = d.setdefault(part, {})
        d[parts[-1]] = value.strip()
    return result

def flatten_dict(d, parent_key='', sep='.'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def get_value(flat_json, possible_keys):
    for key in flat_json:
        normalized = key.replace(" ", "").replace("_", "").replace(".", "").lower()
        for alias in possible_keys:
            alias_norm = alias.replace(" ", "").replace("_", "").replace(".", "").lower()
            if normalized == alias_norm:
                return flat_json[key]
    return None

def extract_user_data(flat_json):
    first = get_value(flat_json, ["name.firstname", "firstname", "first name"])
    last = get_value(flat_json, ["name.lastname", "lastname", "last name"])
    age = get_value(flat_json, ["age"])
    address = {
        "line1": flat_json.get("address.line1", ""),
        "line2": flat_json.get("address.line2", ""),
        "city": flat_json.get("address.city", ""),
        "state": flat_json.get("address.state", "")
    }
    address = {k: v for k, v in address.items() if v}

    if not all([first, last, age]) or not address:
        return None

    try:
        age = int(age.strip())
    except ValueError:
        return None

    full_name = f"{first.strip()} {last.strip()}"

   
    known_keys_normalized = {
        "namefirstname", "firstname", "first name",
        "namelastname", "lastname", "last name",
        "age","addressline1", "addressline2", "addresscity", "addressstate"
    }

    additional_info = {}
    for k, v in flat_json.items():
        norm_k = k.replace(" ", "").replace("_", "").replace(".", "").lower()
        if norm_k not in known_keys_normalized:
            additional_info[k] = v

    return {
        "name": full_name,
        "age": age,
        "address": address,
        "additional_info": additional_info
    }

def process_csv_and_save(csv_file, model):
    decoded_file = TextIOWrapper(csv_file, encoding='utf-8')
    csv_reader = csv.DictReader(decoded_file)
    age_grps = defaultdict(int)
    instances = []
    count = 0
    
    
    for row in csv_reader:
        flat_json = flatten_row(row)
        flat_json_flat = flatten_dict(flat_json)
        data = extract_user_data(flat_json_flat)
        print(data)
        
        if data:
            instances.append(model(
                name=data.get('name'),
                age=data.get('age'),
                address=data.get('address'),
                additional_info=data.get('additional_info')
            ))
            
            age = data.get('age')
            if age is not None and age < 20:
                age_grps["<20"] += 1
            elif age is not None and 20 <= age <= 40:
                age_grps["20-40"] += 1
            elif age is not None and 40 <= age <= 60:
                age_grps["40-60"] += 1
            else:
                age_grps[">60"] += 1
                
            count = count + 1
            
    if instances:
        print("Instances to be saved:", instances)
        try:
           model.objects.bulk_create(instances)
           print("Bulk create successful!")
        except Exception as e:
            print("Bulk create failed:", e)
            traceback.print_exc()
    
    print("\n📊 Age Distribution Report:")
    age_distribution = {}
    for group in ["<20", "20-40", "40-60", ">60"]:
        percent = (age_grps[group] / count) * 100 if count else 0
        print(f"{group:<8}: {percent:.2f}%")
        age_distribution[group] = f"{percent:.2f}%"
    UserReportData.objects.create(
        total_users = count,
        under_20=(age_grps["<20"] / count) * 100 if count else 0,
        between_20_40=(age_grps["20-40"] / count) * 100 if count else 0,
        between_40_60=(age_grps["40-60"] / count) * 100 if count else 0,
        above_60=(age_grps[">60"] / count) * 100 if count else 0
    )
    print("✅ Age distribution report saved to DB.")
    return age_distribution

    
            
                
                
    
        