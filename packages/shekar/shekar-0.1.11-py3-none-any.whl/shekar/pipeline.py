from .base import BaseTransformer
from typing import Iterable
from functools import wraps
from inspect import signature


class Pipeline(BaseTransformer):
    """
    A class for creating a pipeline of transformations using a sequence of BaseTransformer steps.
    The Pipeline class allows chaining multiple transformation steps, where each step is an instance
    of a class that inherits from BaseTransformer. The pipeline can be used to fit, transform, and
    fit-transform data sequentially through the defined steps.

    Args:
        steps (list[tuple[str, BaseTransformer]]): A list of tuples where each tuple contains a
            string (name of the step) and an instance of a BaseTransformer.

    Methods:
        fit(X, y=None):
            Fits each step in the pipeline sequentially using the input data X and optional target y.
        transform(X):
            Transforms the input data X sequentially through each step in the pipeline.
        fit_transform(X, y=None):
            Fits and transforms the input data X sequentially through each step in the pipeline.
            Supports both single string input and a list of strings.
        __call__(X):
            Allows the pipeline to be called as a function, fitting and transforming the input data X.

    Attributes:
        steps (list[tuple[str, BaseTransformer]]): A list of tuples where each tuple contains a
            string (name of the step) and an instance of a BaseTransformer.

    Example:

        >>> pipeline = Pipeline([
                    ("AlphaNumericUnifier", AlphabetNormalizer()),
                    ("ArabicUnicodeNormalizer", ArabicUnicodeNormalizer()),
                    ("NumericNormalizer", NumericNormalizer()),
                    ("PunctuationUnifier", PunctuationNormalizer()),
                    ("EmailMasker", EmailMasker(mask="")),
                    ("URLMasker", URLMasker(mask="")),
                    ("EmojiRemover", EmojiRemover()),
                    ("HTMLTagRemover", HTMLTagRemover()),
                    ("DiacriticsRemover", DiacriticsRemover()),
                    ("RedundantCharacterRemover", RedundantCharacterRemover()),
                    ("NonPersianRemover", NonPersianRemover()),
                    ("SpacingStandardizer", SpacingStandardizer()),
        ])
        >>> result = pipeline("🌹 باز هم مرغ سحر🐔 بر سر منبر گل ")
        >>> print(result)
        باز هم مرغ سحر بر سر منبر گل
    """

    def __init__(self, steps: list[tuple[str, BaseTransformer]]):
        self.steps = steps

    def fit(self, X, y=None):
        for name, step in self.steps:
            X = step.fit(X, y)
        return self

    def transform(self, X):
        for name, step in self.steps:
            X = step.transform(X)
        return X

    def fit_transform(self, X, y=None):
        if isinstance(X, str):
            for name, step in self.steps:
                X = step.fit_transform(X, y)
            return X
        elif isinstance(X, list):

            def generator():  # to avoid making the outer function a generator
                for text in X:
                    for name, step in self.steps:
                        text = step.fit_transform(text, y)
                    yield text

            return generator()

        else:
            raise ValueError("Input must be a string or a list of strings.")

    def __call__(self, X):
        return self.fit_transform(X)

    def on_args(self, param_names):
        """
        Returns a decorator that applies this pipeline to one or more function arguments.

        Args:
            param_names (str or Iterable[str]): The name(s) of the function parameter(s) to be transformed.
                If a string is provided, it will be treated as a single parameter name.
                If an iterable is provided, each item will be treated as a separate parameter name.
        Returns:
            function: A decorator that applies the pipeline to the specified function arguments.

        Raises:
            TypeError: If param_names is not a string or an iterable of strings.
            ValueError: If a specified parameter name is not found in the function arguments.

        Example:
            @normalizer.on_args("text")
            def process_text(text):
                # text will be normalized before being passed to this function
                print(text)

            @normalizer.on_args(["text", "description"])
            def process_text_and_description(text, description):
                # both text and description will be normalized before being passed to this function
                print(text, description)
        """
        if isinstance(param_names, str):
            param_names = [param_names]
        elif not isinstance(param_names, Iterable) or not all(
            isinstance(p, str) for p in param_names
        ):
            raise TypeError("param_names must be a string or an iterable of strings")

        pipeline_instance = self

        def decorator(func):
            sig = signature(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()

                for name in param_names:
                    if name in bound.arguments:
                        bound.arguments[name] = pipeline_instance(bound.arguments[name])
                    else:
                        raise ValueError(
                            f"Parameter '{name}' not found in function arguments."
                        )

                return func(*bound.args, **bound.kwargs)

            return wrapper

        return decorator
