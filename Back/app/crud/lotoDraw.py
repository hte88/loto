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


# Score haut (1) / bas (0)
def get_weighted_numbers(db: Session):
    draws = db.query(LotoDraw).all()

    number_counter = Counter()
    lucky_counter = Counter()

    for draw in draws:
        nums = [draw.number_1, draw.number_2, draw.number_3, draw.number_4, draw.number_5]
        number_counter.update(nums)
        if draw.lucky_number is not None:
            lucky_counter[draw.lucky_number] += 1

    all_numbers = set(number_counter.keys()) | set(lucky_counter.keys())

    def normalize(counter: Counter, number: int, min_count: int, max_count: int):
        count = counter.get(number, 0)
        if max_count > min_count:
            return round((count - min_count) / (max_count - min_count), 4)
        return 1.0 if count > 0 else 0.0

    main_min = min(number_counter.values(), default=0)
    main_max = max(number_counter.values(), default=0)
    lucky_min = min(lucky_counter.values(), default=0)
    lucky_max = max(lucky_counter.values(), default=0)

    result = []
    for number in sorted(all_numbers):
        result.append({
            "number": number,
            "count": number_counter.get(number, 0),
            "weight": normalize(number_counter, number, main_min, main_max),
            "count_lucky_number": lucky_counter.get(number, 0),
            "weight_lucky_number": normalize(lucky_counter, number, lucky_min, lucky_max),
        })

    return result


def generate_weighted_grids(db: Session, config: dict):
    draws = db.query(LotoDraw).all()

    number_counter = Counter()
    lucky_counter = Counter()

    for draw in draws:
        number_counter.update([draw.number_1, draw.number_2, draw.number_3, draw.number_4, draw.number_5])
        if draw.lucky_number:
            lucky_counter[draw.lucky_number] += 1

    all_numbers = list(range(1, 50))
    frequencies = {n: number_counter.get(n, 0) for n in all_numbers}
    max_f = max(frequencies.values() or [1])
    weights = {n: (frequencies[n] / max_f) + 0.01 for n in all_numbers}  # +0.01 pour éviter les zéros

    nb_to_generate = config.get("numbersToGenerate", 5)

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

            while len(grid) < nb_to_generate:
                number = random.choices(all_numbers, weights=[weights[n] for n in all_numbers])[0]
                if number in grid or number in config.get("excludeNumbers", []):
                    continue
                grid.append(number)

            grid.sort()

            if config.get("shouldCheckExistence") and tuple(grid) in existing_grids:
                continue

            if config.get("shouldBalanceEvenOdd", False):
                pair_goal = round(config.get("favorEven", 50) / 100 * nb_to_generate)
                if sum(1 for n in grid if n % 2 == 0) != pair_goal:
                    continue

            if config.get("shouldBalanceHighLow", False):
                haut_goal = round(config.get("favorHigh", 50) / 100 * nb_to_generate)
                if sum(1 for n in grid if n >= 25) != haut_goal:
                    continue

            if config.get("shouldAvoidLogicalSequences", False):
                suites = count_consecutive(grid)
                max_suites = round(config.get("sequenceTolerance", 2) / 100 * nb_to_generate)
                if suites > max_suites:
                    continue

            if config.get("shouldAvoidRoundNumbers", False):
                ronds = count_round_numbers(grid)
                max_ronds = round(config.get("roundNumberTolerance", 2) / 100 * nb_to_generate)
                if ronds > max_ronds:
                    continue

            def generate_lucky_number():
                if not config.get("shouldGenerateLucky", True):
                    return None
                possible = [i for i in range(1, 11) if i not in config.get("excludeLucky", [])]
                if not possible:
                    return None
                base_weights = [lucky_counter.get(i, 1) for i in possible]
                favori = config.get("favorLucky")
                if favori in possible:
                    base_weights[possible.index(favori)] *= 2
                return random.choices(possible, weights=base_weights)[0]

            lucky_number = generate_lucky_number()

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
    return sum(1 for i in range(len(sorted_nums) - 1) if sorted_nums[i + 1] - sorted_nums[i] == 1)


def count_round_numbers(numbers: list[int]) -> int:
    return sum(1 for n in numbers if n % 10 == 0)
