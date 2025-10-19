#!/usr/bin/env python3
import os
import sys
import glob
import json
import pandas as pd

def _load_lookup_data(lookup_dir):
    all_lookup_df = []
    for fname in sorted(glob.glob(os.path.join(lookup_dir, "*.json"))):
        try:
            with open(fname, "r") as fh:
                data = json.load(fh)
        except Exception:
            continue
        if "data" not in data:
            continue
        df = pd.json_normalize(data["data"])

        holo = df.get("tcgplayer.prices.holofoil.market")
        normal = df.get("tcgplayer.prices.normal.market")
        if holo is None:
            holo = pd.Series([pd.NA] * len(df))
        if normal is None:
            normal = pd.Series([pd.NA] * len(df))

        df["card_market_value"] = holo.fillna(normal).fillna(0.0)

        df = df.rename(columns={
            "id": "card_id",
            "name": "card_name",
            "number": "card_number",
            "set.id": "set_id",
            "set.name": "set_name"
        })

        required_cols = ["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"]
        for c in required_cols:
            if c not in df.columns:
                df[c] = None

        df["card_number"] = df["card_number"].astype(str)
        df["set_id"] = df["set_id"].astype(str)
        df["card_id"] = df["set_id"] + "-" + df["card_number"]

        all_lookup_df.append(df[required_cols].copy())

    if not all_lookup_df:
        return pd.DataFrame(columns=["card_id","card_name","card_number","set_id","set_name","card_market_value"])
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values("card_market_value", ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first")
    return lookup_df

def _load_inventory_data(inventory_dir):
    inventory_data = []
    for fname in sorted(glob.glob(os.path.join(inventory_dir, "*.csv"))):
        try:
            df = pd.read_csv(fname, dtype=str)
        except Exception:
            continue
        inventory_data.append(df)
    if not inventory_data:
        return pd.DataFrame()
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    inventory_df["card_number"] = inventory_df["card_number"].astype(str)
    inventory_df["set_id"] = inventory_df["set_id"].astype(str)
    inventory_df["card_id"] = inventory_df["set_id"] + "-" + inventory_df["card_number"]
    return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    if inventory_df.empty:
        print("Error: Inventory directory empty or no CSVs found.", file=sys.stderr)
        cols = ["index","binder_name","page_number","slot_number","card_id","card_name","set_id","set_name","card_number","card_market_value"]
        pd.DataFrame(columns=cols).to_csv(output_file, index=False)
        return

    # merge with explicit suffixes so we can reconcile card_name columns
    merged = pd.merge(
        inventory_df,
        lookup_df[["card_id","card_name","set_name","card_market_value"]],
        on="card_id",
        how="left",
        suffixes=("_inv", "_lkup")
    )

    # prefer lookup name, fall back to inventory name
    if "card_name_lkup" in merged.columns or "card_name_inv" in merged.columns:
        merged["card_name"] = merged.get("card_name_lkup").fillna(merged.get("card_name_inv"))
    elif "card_name" not in merged.columns:
        merged["card_name"] = None

    # normalize market value and set_name
    merged["card_market_value"] = pd.to_numeric(merged.get("card_market_value", 0.0), errors="coerce").fillna(0.0)
    merged["set_name"] = merged.get("set_name").fillna("NOT_FOUND")

    # create index/location string
    merged["index"] = merged["binder_name"].astype(str) + "-" + merged["page_number"].astype(str) + "-" + merged["slot_number"].astype(str)

    final_cols = ["index","binder_name","page_number","slot_number","card_id","card_name","set_id","set_name","card_number","card_market_value"]

    # ensure all final columns exist
    for c in final_cols:
        if c not in merged.columns:
            merged[c] = 0.0 if c == "card_market_value" else None

    merged.to_csv(output_file, columns=final_cols, index=False)
    print(f"Wrote portfolio to {output_file}")

def main():
    update_portfolio("./card_inventory/", "./card_set_lookup/", "card_portfolio.csv")

def test():
    update_portfolio("./card_inventory_test/", "./card_set_lookup_test/", "test_card_portfolio.csv")

if __name__ == "__main__":
    print("Starting update_portfolio in TEST mode", file=sys.stderr)
    test()