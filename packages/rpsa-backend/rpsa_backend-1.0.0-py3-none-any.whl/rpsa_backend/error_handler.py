import importlib.util
import os
import time
import logging

from typing import Optional, Type
from .safety import (
    SAFE_BUILTINS,
    SAFE_MODULES,
    PYTHON_ERROR_HELPER,
    MAX_STRATEGY_RUNTIME,
)
from .arena import Game
from .models import Strategy as StrategyModel, MLModel
from . import db
from .random_strategy import RandomStrategy


class StrategyValidationError(Exception):
    def __init__(self, message: str, suggestions: Optional[list[str]] = None):
        super().__init__(message)
        self.suggestions = suggestions or []

    def __str__(self):
        return self.args[0]


def get_error_suggestions(error_message: str) -> list[str]:
    suggestions: list[str] = []
    for key, hints in PYTHON_ERROR_HELPER.items():
        if key in error_message:
            suggestions.extend(hints)
    return suggestions


def validate_strategy_script(
    script: str,
    temp_path: str,
    strategies_folder: str,
    model_path: Optional[str] = None,
) -> Type[StrategyModel]:
    """
    Validate that the uploaded script:
      - defines `strategy` variable
      - imports under SAFE_BUILTINS
      - instantiates (with model_path if provided)
      - passes a quick Game smoke‐test within time limit
    """
    try:
        # -- Load user module under our sandbox builtins --
        spec = importlib.util.spec_from_file_location(temp_path, temp_path)
        module = importlib.util.module_from_spec(spec)
        module.__builtins__ = SAFE_BUILTINS
        spec.loader.exec_module(module)

        # -- Ensure `strategy` exists --
        if not hasattr(module, "strategy"):
            raise StrategyValidationError(
                "The script does not contain a 'strategy' variable.",
                suggestions=[
                    "Ensure you assign your Strategy subclass to a variable named `strategy`."
                ],
            )

        # -- Grab the class --
        StratCls = module.strategy

        # -- Instantiate, passing model_path if accepted --
        try:
            strat_inst = StratCls(model_path) if model_path else StratCls()
        except TypeError:
            strat_inst = StratCls()

        # -- Check `.name` attribute --
        if not hasattr(strat_inst, "name"):
            raise StrategyValidationError(
                "Strategy instance has no `.name` property.",
                suggestions=["Add a `name` attribute to your Strategy class."],
            )

        # -- Unique name in DB --
        existing = (
            db.session.query(StrategyModel).filter_by(name=strat_inst.name).first()
        )
        if existing:
            raise StrategyValidationError(
                f"A strategy named '{strat_inst.name}' already exists.",
                suggestions=["Use a unique strategy name."],
            )

        # -- Build model_paths map for smoke test --
        model_paths: dict[str, str] = {}
        if model_path:
            model_paths[strat_inst.name] = model_path

        # -- Smoke‐test game with RandomStrategy --
        test_game = Game(StratCls, RandomStrategy, model_paths)
        t0 = time.time()
        w1, w2, ties = test_game.play_rounds(n=2000)
        elapsed = time.time() - t0
        logging.info(f"Strategy runtime: {elapsed:.3f}s")

        if w1 + w2 + ties == 0:
            raise StrategyValidationError("No valid moves detected in test game.")

        if elapsed > MAX_STRATEGY_RUNTIME:
            raise StrategyValidationError(
                f"Strategy took too long ({elapsed:.3f}s). Max is {MAX_STRATEGY_RUNTIME}s."
            )

        return StratCls

    except StrategyValidationError:
        raise
    except ImportError as e:
        msg = str(e)
        raise StrategyValidationError(
            f"ImportError: {msg}. Only modules in {', '.join(SAFE_MODULES)} are allowed.",
            suggestions=["Check your imports for typos or disallowed modules."],
        )
    except Exception as e:
        msg = str(e)
        suggestions = get_error_suggestions(msg)
        raise StrategyValidationError(msg, suggestions=suggestions)
