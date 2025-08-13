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


def get_all_draws(db: Session, sources: list[str], start_date=None, end_date=None) -> tuple[list, dict]:
    draws = []
    stats_count = {}

    if "loto" in sources:
        query = db.query(Loto)
        if start_date:
            query = query.filter(Loto.date_draw >= start_date)
        if end_date:
            query = query.filter(Loto.date_draw <= end_date)
        loto_draws = query.all()
        draws.extend(loto_draws)
        stats_count["loto"] = len(loto_draws)

    if "super" in sources:
        query = db.query(SuperLoto)
        if start_date:
            query = query.filter(SuperLoto.date_draw >= start_date)
        if end_date:
            query = query.filter(SuperLoto.date_draw <= end_date)
        super_draws = query.all()
        draws.extend(super_draws)
        stats_count["super"] = len(super_draws)

    if "grand" in sources:
        query = db.query(GrandLoto)
        if start_date:
            query = query.filter(GrandLoto.date_draw >= start_date)
        if end_date:
            query = query.filter(GrandLoto.date_draw <= end_date)
        grand_draws = query.all()
        draws.extend(grand_draws)
        stats_count["grand"] = len(grand_draws)

    return draws, stats_count


def get_weighted_numbers_combined(db: Session, sources: list[str], start_date=None, end_date=None):
    draws, stats_count  = get_all_draws(db, sources, start_date, end_date)

    total_draws = len(draws)
    number_counter = Counter()
    lucky_counter = Counter()

    for draw in draws:
        numbers = [draw.number_1, draw.number_2, draw.number_3, draw.number_4, draw.number_5]
        if draw.number_6 is not None:
            numbers.append(draw.number_6)
        if draw.additional_number is not None:
            numbers.append(draw.additional_number)

        number_counter.update([n for n in numbers if isinstance(n, int)])

        if isinstance(draw.lucky_number, int) and 1 <= draw.lucky_number <= 10:
            lucky_counter[draw.lucky_number] += 1

    # Normalisation
    def normalize(counter: Counter, total_draws: int):
        if not counter or total_draws == 0:
            return []

        max_count = max(counter.values())
        min_count = min(counter.values())

        return [
            {
                "number": number,
                "count": count,
                "weight": round((count - min_count) / (max_count - min_count), 4)
                if max_count > min_count else 1.0,
                "percentage": round((count / total_draws) * 100, 2)
  }
            for number, count in sorted(counter.items())
        ]

    return {
        "numbers": normalize(number_counter, total_draws),        # ✅ de 1 à 49
        "lucky_numbers": normalize(lucky_counter, total_draws),    # ✅ de 1 à 10
        "source_counts": stats_count,
        "total_draws_used": total_draws
    }



def generate_weighted_grids(db: Session, config: dict):
    print("🔍 Configuration reçue :", config)  # ou logger.info(...)

    draws, source_counts = get_all_draws(
        db,
        sources=config.get("includedSources", ["loto", "super", "grand"]),
        start_date=config.get("start_date"),
        end_date=config.get("end_date")
    )

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
    total_draws = len(draws)

    max_count = max(number_counter.values(), default=0)
    weights = {n: (number_counter.get(n, 0) / max_count) + 0.01 for n in all_numbers}
    percentages = {n: (number_counter.get(n, 0) / total_draws) * 100 if total_draws > 0 else 0 for n in all_numbers}

    existing_grids = set()
    if config.get("shouldCheckExistence"):
        existing_grids = {
            tuple(sorted([
                d.number_1, d.number_2, d.number_3,
                d.number_4, d.number_5, d.number_6 is not None,
                d.additional_number is not None
            ]))
            for d in draws
        }

    nb_to_generate = config.get("numbersToGenerate", 5)

    def pick_grid():
        """mode ∈ {'score', 'weight', 'percentage'}"""
        attempts = 0

        while True:
            attempts += 1
            if attempts > 3000:
                raise Exception("Impossible de générer une grille valide")

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

                lucky_frequencies = {i: lucky_counter.get(i, 0) for i in range(1, 11)}
                max_lucky = max(lucky_frequencies.values(), default=0)

                if max_lucky == 0:
                    lucky_weights = [1] * len(possible)
                else:
                    lucky_weights = [(lucky_counter.get(i, 0) / max_lucky) + 0.01 for i in possible]

                favori = config.get("favorLucky")
                if favori in possible:
                    lucky_weights[possible.index(favori)] *= 2

                return random.choices(possible, weights=lucky_weights)[0]

            lucky_number = generate_lucky_number()

            score = 0
            if config.get("shouldEvaluateScore"):
                score = round(sum(weights[n] for n in grid if isinstance(n, int)), 4)

            score = round(sum(weights[n] for n in grid), 4) if config.get("shouldEvaluateScore") else None
            avg_weight = round(sum(weights[n] for n in grid) / nb_to_generate, 4) if config.get("shouldEvaluateWeight") else None
            avg_percentage = round(sum(percentages[n] for n in grid) / nb_to_generate, 4) if config.get("shouldEvaluatePercentage") else None

            return {
                "numbers": grid,
                "lucky_number": lucky_number,
                "source_counts": source_counts,
                "total_draws_used": total_draws,
                **({"score": score} if score is not None else {}),
                **({"weight": avg_weight} if avg_weight is not None else {}),
                **({"percentage": avg_percentage} if avg_percentage is not None else {})
            }

    modes = []
    if config.get("shouldEvaluateScore"):
        modes.append("score")
    if config.get("shouldEvaluateWeight"):
        modes.append("weight")
    if config.get("shouldEvaluatePercentage"):
        modes.append("percentage")

    results = []
    if len(modes) == 1:
        # Un seul mode → génération classique
        mode = modes[0]
        results = [dict(pick_grid(), mode=mode) for _ in range(config["gridsToGenerate"])]
    else:
        # Plusieurs modes → garder les N meilleures pour chaque
        for mode in modes:
            generated = [pick_grid() for _ in range(config["gridsToGenerate"] * 2)]
            sorted_grids = sorted(generated, key=lambda g: g.get(mode, 0), reverse=True)
            results.extend([dict(g, mode=mode) for g in sorted_grids[:config["gridsToGenerate"]]])

    return results


def count_consecutive(numbers: list[int]) -> int:
    filtered = sorted([n for n in numbers if isinstance(n, int)])
    return sum(1 for i in range(len(filtered) - 1) if filtered[i + 1] - filtered[i] == 1)


def count_round_numbers(numbers: list[int]) -> int:
    return sum(1 for n in numbers if isinstance(n, int) and n % 10 == 0)
