#!/usr/bin/env python3
"""Synthetic SmartFarm data generator.

Produces newline-delimited JSON records in ./generator_output.jsonl (or configured path).
Supports domain diversity and anomaly simulation.
"""
import argparse
import json
import random
from datetime import datetime, timedelta
from faker import Faker


fake = Faker()


def gen_livestock(anomaly_rate):
    animal_id = f"A-{fake.random_int(1000,9999)}"
    temp = round(random.uniform(36.0, 40.5), 1)
    health = "healthy"
    if temp > 39.0 or random.random() < anomaly_rate:
        health = "critical"
    return {
        "domain": "livestock",
        "animal_id": animal_id,
        "species": random.choice(["cow", "sheep", "goat"]),
        "health_status": health,
        "temperature": temp,
        "recorded_at": datetime.utcnow().isoformat()
    }


def gen_crop(anomaly_rate):
    plot_id = f"P-{fake.random_int(1,200)}"
    moisture = round(random.uniform(5, 60), 1)
    status = "good"
    if moisture < 15 or random.random() < anomaly_rate:
        status = "dry"
    return {
        "domain": "crop",
        "plot_id": plot_id,
        "crop_type": random.choice(["wheat", "corn", "soy"]),
        "health_status": status,
        "moisture_level": moisture,
        "recorded_at": datetime.utcnow().isoformat()
    }


def gen_irrigation(anomaly_rate):
    schedule_id = f"S-{fake.random_int(1000,9999)}"
    delay = random.choice([0, 0, 5, 10, 60])
    status = "on_time" if delay <= 5 else "delayed"
    if random.random() < anomaly_rate and delay > 30:
        status = "failed"
    start_time = datetime.utcnow() - timedelta(minutes=delay)
    return {
        "domain": "irrigation",
        "schedule_id": schedule_id,
        "plot_id": f"P-{fake.random_int(1,200)}",
        "start_time": start_time.isoformat(),
        "duration_minutes": random.choice([15, 30, 45]),
        "status": status,
        "recorded_at": datetime.utcnow().isoformat()
    }


def gen_worker_task(anomaly_rate):
    worker_id = f"W-{fake.random_int(1,500)}"
    assigned_at = datetime.utcnow() - timedelta(hours=random.randint(0,48))
    completed = random.choice([True, True, False])
    status = "completed" if completed else "pending"
    if random.random() < anomaly_rate and not completed:
        status = "overdue"
    return {
        "domain": "worker",
        "worker_id": worker_id,
        "task": fake.sentence(nb_words=4),
        "assigned_at": assigned_at.isoformat(),
        "completed_at": (assigned_at + timedelta(hours=random.randint(1,72))).isoformat() if completed else None,
        "status": status,
        "recorded_at": datetime.utcnow().isoformat()
    }


def main(path, count, anomaly_rate):
    generators = [gen_livestock, gen_crop, gen_irrigation, gen_worker_task]
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(count):
            g = random.choice(generators)
            rec = g(anomaly_rate)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic SmartFarm records")
    parser.add_argument("--out", default="./generator_output.jsonl", help="Output JSONL path")
    parser.add_argument("--count", type=int, default=12000, help="Number of records to generate (default 12000)")
    parser.add_argument("--anomaly-rate", type=float, default=0.02, help="Probability (0-1) of injecting an anomaly per record")
    args = parser.parse_args()
    main(args.out, args.count, args.anomaly_rate)
