from sqlalchemy.orm import Session
from app.models.lotoDraw import LotoDraw
from app.schemas.lotoDraw import LotoDrawCreate

from collections import Counter
import random

def create_loto_draw(db: Session, draw: LotoDrawCreate):
    existing = db.query(LotoDraw).filter_by(
        number_1=draw.number_1,
        number_2=draw.number_2,
        number_3=draw.number_3,
        number_4=draw.number_4,
        number_5=draw.number_5,
        lucky_number=draw.lucky_number
    ).first()

    if existing:
        return existing

    db_draw = LotoDraw(**draw.model_dump())
    db.add(db_draw)
    db.commit()
    db.refresh(db_draw)
    return db_draw

def get_loto_draws(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LotoDraw).offset(skip).limit(limit).all()

def get_loto_draw(db: Session, draw_id: int):
    return db.query(LotoDraw).filter(LotoDraw.id == draw_id).first()

def delete_loto_draw(db: Session, draw_id: int):
    db_draw = db.query(LotoDraw).filter(LotoDraw.id == draw_id).first()
    if db_draw:
        db.delete(db_draw)
        db.commit()
    return db_draw

## start algo

def get_global_number_frequency(db: Session):
    draws = db.query(LotoDraw).all()

    counter = Counter()
    for draw in draws:
        numbers = [
            draw.number_1,
            draw.number_2,
            draw.number_3,
            draw.number_4,
            draw.number_5
        ]
        counter.update(numbers)
        if draw.lucky_number is not None:
            counter[draw.lucky_number] += 1

    frequency = [
        {"number": number, "count": count}
        for number, count in counter.most_common()
    ]

    return {
        "total_draws": len(draws),
        "global_frequency": frequency
    }

# scrore hight (1) low (0)
def get_weighted_numbers(db: Session):
    draws = db.query(LotoDraw).all()
    counter = Counter()

    for draw in draws:
        nums = [draw.number_1, draw.number_2, draw.number_3, draw.number_4, draw.number_5]
        counter.update(nums)
        if draw.lucky_number is not None:
            counter[draw.lucky_number] += 1

    if not counter:
        return []

    max_count = max(counter.values())
    min_count = min(counter.values())

    result = []
    for number, count in counter.items():
        weight = (count - min_count) / (max_count - min_count) if max_count > min_count else 1.0
        result.append({
            "number": number,
            "count": count,
            "weight": round(weight, 4)  # normalisé entre 0 et 1
        })

def generate_weighted_grids(db: Session, config: dict):
    from collections import Counter
    from app.models.lotoDraw import LotoDraw

    draws = db.query(LotoDraw).all()
    counter = Counter()

    for draw in draws:
        counter.update([draw.number_1, draw.number_2, draw.number_3, draw.number_4, draw.number_5])
        if draw.lucky_number:
            counter[draw.lucky_number] += 1

    # Liste complète pondérée (de 1 à 49)
    all_numbers = list(range(1, 50))
    frequencies = {n: counter.get(n, 0) for n in all_numbers}

    max_f = max(frequencies.values() or [1])
    weights = {n: (frequencies[n] / max_f) + 0.01 for n in all_numbers}  # +0.01 pour éviter les zéros

    existing_grids = set()
    if config.get("shouldCheckExistence"):
        existing_grids = {
            tuple(sorted([d.number_1, d.number_2, d.number_3, d.number_4, d.number_5]))
            for d in draws
        }

    def pick_grid():
        attempts = 0
        while True:
            attempts += 1
            if attempts > 1000:
                raise Exception("Impossible de générer une grille valide selon les critères.")

            grid = config.get("includeNumbers", []).copy()

            while len(grid) < 5:
                number = random.choices(all_numbers, weights=[weights[n] for n in all_numbers])[0]
                if number in grid or number in config.get("excludeNumbers", []):
                    continue
                grid.append(number)

            grid.sort()

            # --- Vérifie existence
            if config.get("shouldCheckExistence"):
                if tuple(grid) in existing_grids:
                    continue

            # --- Contraintes pair/impair
            if config["shouldBalanceEvenOdd"]:
                pair_goal = round(config["favorEven"] / 100 * 5)
                if sum(1 for n in grid if n % 2 == 0) != pair_goal:
                    continue

            # --- Contraintes haut/bas
            if config["shouldBalanceHighLow"]:
                haut_goal = round(config["favorHigh"] / 100 * 5)
                if sum(1 for n in grid if n >= 25) != haut_goal:
                    continue

            # --- Suites interdites
            if config["shouldAvoidLogicalSequences"]:
                suites = count_consecutive(grid)
                max_suites = round(config["sequenceTolerance"] / 100 * 5)
                if suites > max_suites:
                    continue

            # --- Chiffres ronds interdits
            if config["shouldAvoidRoundNumbers"]:
                ronds = count_round_numbers(grid)
                max_ronds = round(config["roundNumberTolerance"] / 100 * 5)
                if ronds > max_ronds:
                    continue

            # --- Chance
            def generate_lucky_number():
                if not config.get("shouldGenerateLucky", True):
                    return None

                possible = [i for i in range(1, 11) if i not in config.get("excludeLucky", [])]
                if not possible:
                    return None

                base_weights = [counter.get(i, 1) for i in possible]

                # Si un lucky est à favoriser, on augmente son poids
                favori = config.get("favorLucky")
                if favori in possible:
                    favori_index = possible.index(favori)
                    base_weights[favori_index] *= 2  # ou un autre facteur

                return random.choices(possible, weights=base_weights)[0]


            lucky_number = generate_lucky_number()
            # --- Score pondéré
            score = 0
            if config.get("shouldEvaluateScore"):
                score = round(sum(weights[n] for n in grid), 4)

            return {
                "numbers": grid,
                "lucky_number": lucky_number,
                **({"score": score} if config.get("shouldEvaluateScore") else {})
            }

    return [pick_grid() for _ in range(config["gridsToGenerate"])]

def count_consecutive(numbers: list[int]) -> int:
    sorted_nums = sorted(numbers)
    return sum(1 for i in range(len(sorted_nums) - 1) if sorted_nums[i+1] - sorted_nums[i] == 1)

def count_round_numbers(numbers: list[int]) -> int:
    return sum(1 for n in numbers if n % 10 == 0)

    # tri décroissant par fréquence pondérée
    result.sort(key=lambda x: x["weight"], reverse=True)

    return result
