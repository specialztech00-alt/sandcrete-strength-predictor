# -*- coding: utf-8 -*-
"""Test directional consistency of predictions per project brief."""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests

BASE = "http://127.0.0.1:8000/predict"

def predict(brand, ratio, wcr, curing, age, std="NIS"):
    r = requests.post(BASE, json={
        "cement_brand": brand,
        "mix_ratio": ratio,
        "water_cement_ratio": wcr,
        "curing_technique": curing,
        "curing_age": age,
        "design_standard": std,
    })
    d = r.json()
    return d["predicted_strength"], d["strength_category"], d["confidence_score"]

print("=" * 70)
print("TEST 1: Cement Brand ranking (Dangote > Lafarge > BUA > Purechem)")
print("   Fixed: 1:6, WCR=0.55, submerged, 28 days")
print("-" * 70)
for brand in ["Dangote", "Lafarge", "BUA", "Purechem"]:
    s, cat, conf = predict(brand, "1:6", 0.55, "submerged", 28)
    print(f"  {brand:10s}  ->  {s:.3f} MPa  ({cat}, {conf}%)")

print()
print("=" * 70)
print("TEST 2: Mix ratio (1:5 strongest -> 1:10 weakest)")
print("   Fixed: Dangote, WCR=0.55, submerged, 28 days")
print("-" * 70)
for ratio in ["1:5", "1:6", "1:7", "1:8", "1:9", "1:10"]:
    s, cat, conf = predict("Dangote", ratio, 0.55, "submerged", 28)
    print(f"  {ratio:5s}  ->  {s:.3f} MPa  ({cat}, {conf}%)")

print()
print("=" * 70)
print("TEST 3: Curing method (submerged > sprinkling > open air)")
print("   Fixed: Dangote, 1:6, WCR=0.55, 28 days")
print("-" * 70)
for curing in ["submerged", "sprinkling", "air"]:
    s, cat, conf = predict("Dangote", "1:6", 0.55, curing, 28)
    label = "Open Air" if curing == "air" else curing.title()
    print(f"  {label:12s}  ->  {s:.3f} MPa  ({cat}, {conf}%)")

print()
print("=" * 70)
print("TEST 4: Curing age (28 > 14 > 7)")
print("   Fixed: Dangote, 1:6, WCR=0.55, submerged")
print("-" * 70)
for age in [28, 14, 7]:
    s, cat, conf = predict("Dangote", "1:6", 0.55, "submerged", age)
    print(f"  {age:2d} days  ->  {s:.3f} MPa  ({cat}, {conf}%)")

print()
print("=" * 70)
print("TEST 5: Design standard changes recommendation text")
print("   Fixed: Dangote, 1:6, WCR=0.55, submerged, 28 days")
print("-" * 70)
for std in ["NIS", "BS", "ASTM"]:
    s, cat, conf = predict("Dangote", "1:6", 0.55, "submerged", 28, std)
    print(f"  {std:4s}  ->  {s:.3f} MPa  ({cat})")

print()
print("=" * 70)
print("TEST 6: Edge cases - weakest combination")
print("   Purechem, 1:10, WCR=0.65, air, 7 days")
print("-" * 70)
s, cat, conf = predict("Purechem", "1:10", 0.65, "air", 7)
print(f"  ->  {s:.3f} MPa  ({cat}, {conf}%)")

print()
print("=" * 70)
print("TEST 7: Strongest combination")
print("   Dangote, 1:5, WCR=0.50, submerged, 28 days")
print("-" * 70)
s, cat, conf = predict("Dangote", "1:5", 0.50, "submerged", 28)
print(f"  ->  {s:.3f} MPa  ({cat}, {conf}%)")

print()
print("ALL TESTS COMPLETE")
