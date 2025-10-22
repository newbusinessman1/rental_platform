# fix_fixture.py
import json
from pathlib import Path
from django.apps import apps

p_in = Path("fixtures/seed_multi.json")
p_out = Path("fixtures/seed_multi.fixed.json")
data = json.loads(p_in.read_text())

Listing = apps.get_model("ads", "Listing")
Booking = apps.get_model("ads", "Booking", require_ready=False)
Review = apps.get_model("ads", "Review", require_ready=False)

f_listing = {f.name for f in Listing._meta.fields}
f_booking = {f.name for f in Booking._meta.fields} if Booking else set()
f_review  = {f.name for f in Review._meta.fields}  if Review else set()

def fix_listing(fields):
    # rename
    if "location" in fields:
        fields["city"] = fields.pop("location")
    if "price" in fields:
        fields["price_per_night"] = fields.pop("price")
    if "owner" in fields:
        v = fields.pop("owner")
        if isinstance(v, int):
            fields["owner_email"] = f"owner{v}@example.com"
        else:
            fields["owner_email"] = str(v)
    # drop лишние
    for k in ["rooms", "housing_type", "is_active", "views", "updated_at"]:
        fields.pop(k, None)
    # оставить только существующие поля
    return {k: v for k, v in fields.items() if k in f_listing}

def squash_to(model_fields, fields):
    return {k: v for k, v in fields.items() if k in model_fields}

fixed = []
for obj in data:
    model = obj.get("model")
    fields = dict(obj.get("fields", {}))
    if model == "ads.listing":
        fields = fix_listing(fields)
    elif model == "ads.booking" and f_booking:
        if "tenant" in fields and "tenant_email" in f_booking and "tenant" not in f_booking:
            v = fields.pop("tenant")
            fields["tenant_email"] = f"tenant{v}@example.com" if isinstance(v, int) else str(v)
        fields = squash_to(f_booking, fields)
    elif model == "ads.review" and f_review:
        if "user" in fields and "user_email" in f_review and "user" not in f_review:
            v = fields.pop("user")
            fields["user_email"] = f"user{v}@example.com" if isinstance(v, int) else str(v)
        fields = squash_to(f_review, fields)
    fixed.append({"model": model, "pk": obj.get("pk"), "fields": fields})

p_out.write_text(json.dumps(fixed, ensure_ascii=False, indent=2))
print("✅ Written:", p_out)
