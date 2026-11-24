from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256
from pathlib import Path

import pandas as pd

TZ = "Asia/Jakarta"
TABLES = {
    "branches": "branch_id branch_name city latitude longitude opening_time closing_time demand_multiplier prep_capacity_multiplier region",
    "menu": "menu_id menu_name category station base_prep_min list_price_idr is_active popularity_weight",
    "ingredients": "ingredient_id ingredient_name unit unit_cost_idr shelf_life_days ingredient_group",
    "recipes": "menu_id ingredient_id qty_per_unit",
    "branch_inventory_policy": "branch_id ingredient_id opening_qty reorder_point_qty restock_lot_qty lead_time_days target_cover_days",
    "orders": "order_id branch_id ordered_at ready_at completed_at channel order_status payment_status gross_amount_idr discount_amount_idr net_amount_idr sla_min prep_time_min delayed_flag simulation_date",
    "order_items": "order_item_id order_id menu_id quantity unit_price_idr line_gross_idr allocated_discount_idr line_net_idr unit_food_cost_idr line_food_cost_idr line_food_gp_idr",
    "inventory_movements": "movement_id branch_id ingredient_id order_id occurred_at movement_type signed_qty reason unit_cost_idr movement_cost_idr",
    "feedback": "feedback_id order_id rating review_text theme feedback_at",
}
TIME_FIELDS = {
    "orders": ("ordered_at", "ready_at", "completed_at"),
    "inventory_movements": ("occurred_at",),
    "feedback": ("feedback_at",),
}
MOVEMENT_PRIORITY = {kind: index for index, kind in enumerate(("OPENING", "RECEIPT", "USAGE", "WASTE"))}


def frame(table, rows):
    return pd.DataFrame(rows, columns=TABLES[table].split())


@dataclass
class DataBundle:
    tables: dict[str, pd.DataFrame]

    def __getitem__(self, name):
        return self.tables[name]


def local_timestamps(series):
    values = pd.to_datetime(series, format="mixed", utc=True)
    return values.dt.tz_convert(TZ)


def cutoff_after(day: date) -> pd.Timestamp:
    return pd.Timestamp(day + timedelta(days=1), tz=TZ)


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_clean_bundle(path: Path) -> DataBundle:
    tables = {}
    for name, columns in TABLES.items():
        table = pd.read_csv(path / f"{name}.csv", keep_default_na=False, na_values=[""])
        if list(table.columns) != columns.split():
            raise ValueError(f"Kolom {name}.csv tidak cocok dengan skema.")
        for column in TIME_FIELDS.get(name, ()):
            table[column] = local_timestamps(table[column])
        if name == "orders":
            table["delayed_flag"] = table["delayed_flag"].astype("boolean")
            table["simulation_date"] = pd.to_datetime(table["simulation_date"]).dt.date
        if name == "feedback":
            table["review_text"] = table["review_text"].fillna("")
        tables[name] = table
    return DataBundle(tables)


def write_csv(path: Path, table: pd.DataFrame):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".csv.tmp")
    table.to_csv(temporary, index=False, lineterminator="\n")
    temporary.replace(path)
