from sqlalchemy.orm import Session
from app.models.lotoDraw import Loto, SuperLoto, GrandLoto
from app.schemas.lotoDraw import LotoDrawCreate
from collections import Counter
import random

MODEL_MAPPING = {
    "loto": Loto,
    "super": SuperLoto,
    "grand": GrandLoto,
}

def create_loto_draw(db: Session, draw: LotoDrawCreate):
    model = MODEL_MAPPING.get(draw.game_type.lower())
    if not model:
        raise ValueError("Type de jeu invalide")

    exists = db.query(model).filter_by(
        date_draw=draw.date_draw,
        number_1=draw.number_1,
        number_2=draw.number_2,
        number_3=draw.number_3,
        number_4=draw.number_4,
        number_5=draw.number_5,
        number_6=draw.number_6,
        lucky_number=draw.lucky_number,
        game_type=draw.game_type,
    ).first()

    if exists:
        return exists

    db_draw = model(**draw.model_dump())
    db.add(db_draw)
    db.commit()
    db.refresh(db_draw)
    return db_draw


def get_loto_draws(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Loto).offset(skip).limit(limit).all()


def get_loto_draw(db: Session, draw_id: int):
    return db.query(Loto).filter(Loto.id == draw_id).first()


def delete_loto_draw(db: Session, draw_id: int):
    db_draw = db.query(Loto).filter(Loto.id == draw_id).first()
    if db_draw:
        db.delete(db_draw)
        db.commit()
    return db_draw


def get_all_draws(db: Session, sources: list[str]) -> list:
    draws = []
    if "loto" in sources:
        draws.extend(db.query(Loto).all())
    if "super" in sources:
        draws.extend(db.query(SuperLoto).all())
    if "grand" in sources:
        draws.extend(db.query(GrandLoto).all())
    return draws


def get_weighted_numbers_combined(db: Session, sources: list[str]):
    from app.models.lotoDraw import Loto, SuperLoto, GrandLoto
    from collections import Counter

    models = {
        "loto": Loto,
        "super": SuperLoto,
        "grand": GrandLoto,
    }

    all_draws = []
    for source in sources:
        model = models.get(source)
        if model:
            all_draws.extend(db.query(model).all())

    number_counter = Counter()
    lucky_counter = Counter()

    for draw in all_draws:

        numbers = [draw.number_1, draw.number_2, draw.number_3, draw.number_4, draw.number_5]
        if draw.number_6 is not None:
            numbers.append(draw.number_6)
        if draw.additional_number is not None:
            numbers.append(draw.additional_number)

        number_counter.update(numbers)

        if draw.lucky_number is not None:
            lucky_counter[draw.lucky_number] += 1

        for n in numbers:
            if isinstance(n, int):  # ✅ Exclure les None
                number_counter[n] += 1

        if isinstance(draw.lucky_number, int):
            lucky_counter[draw.lucky_number] += 1

    # Gestion des poids (pondération normalisée)
    def normalize(counter):
        if not counter:
            return []
        max_count = max(counter.values())
        min_count = min(counter.values())
        return [
            {
                "number": number,
                "count": count,
                "weight": round((count - min_count) / (max_count - min_count), 4)
                if max_count > min_count else 1.0,
            }
            for number, count in sorted(counter.items())
        ]

    return {
        "numbers": normalize(number_counter),
        "lucky_numbers": normalize(lucky_counter),
    }



def generate_weighted_grids(db: Session, config: dict):
    draws = get_all_draws(db, config.get("includedSources", ["loto", "super", "grand"]))

    number_counter = Counter()
    lucky_counter = Counter()

    for draw in draws:
        numbers = [draw.number_1, draw.number_2, draw.number_3, draw.number_4, draw.number_5]
        if draw.number_6 is not None:
            numbers.append(draw.number_6)
        if draw.additional_number is not None:
            numbers.append(draw.additional_number)

        number_counter.update([n for n in numbers if isinstance(n, int)])

        if isinstance(draw.lucky_number, int):
            lucky_counter[draw.lucky_number] += 1

    all_numbers = list(range(1, 50))
    frequencies = {n: number_counter.get(n, 0) for n in all_numbers}
    max_f = max(frequencies.values() or [1])
    weights = {n: (frequencies[n] / max_f) + 0.01 for n in all_numbers}  # +0.01 pour éviter poids nuls

    nb_to_generate = config.get("numbersToGenerate", 5)
    existing_grids = set()
    if config.get("shouldCheckExistence"):
        existing_grids = {
            tuple(sorted([
                d.number_1, d.number_2, d.number_3, d.number_4, d.number_5
            ]))
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
                even_count = sum(1 for n in grid if isinstance(n, int) and n % 2 == 0)
                if even_count != pair_goal:
                    continue

            if config.get("shouldBalanceHighLow", False):
                high_goal = round(config.get("favorHigh", 50) / 100 * nb_to_generate)
                high_count = sum(1 for n in grid if isinstance(n, int) and n >= 25)
                if high_count != high_goal:
                    continue

            if config.get("shouldAvoidLogicalSequences", False):
                if count_consecutive(grid) > round(config.get("sequenceTolerance", 10) / 100 * nb_to_generate):
                    continue

            if config.get("shouldAvoidRoundNumbers", False):
                if count_round_numbers(grid) > round(config.get("roundNumberTolerance", 50) / 100 * nb_to_generate):
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
                score = round(sum(weights[n] for n in grid if isinstance(n, int)), 4)

            return {
                "numbers": grid,
                "lucky_number": lucky_number,
                **({"score": score} if config.get("shouldEvaluateScore") else {})
            }

    return [pick_grid() for _ in range(config["gridsToGenerate"])]


def count_consecutive(numbers: list[int]) -> int:
    filtered = sorted([n for n in numbers if isinstance(n, int)])
    return sum(1 for i in range(len(filtered) - 1) if filtered[i + 1] - filtered[i] == 1)


def count_round_numbers(numbers: list[int]) -> int:
    return sum(1 for n in numbers if isinstance(n, int) and n % 10 == 0)
