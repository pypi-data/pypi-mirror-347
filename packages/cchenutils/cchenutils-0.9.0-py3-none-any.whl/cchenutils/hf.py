import pandas as pd
from tqdm.auto import trange
from transformers import pipeline


def analyze(text, *args, batch_size=None, **kwargs):
    """
    Analyze a list, Series, or single string using a HuggingFace pipeline with batching.

    Args:
        text (str | list[str] | pd.Series): Input text(s).
        *args, **kwargs: Arguments for the transformers.pipeline function.
        batch_size (int): Number of items per batch.

    Returns:
        pd.DataFrame: Prediction scores.
    """

    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError('batch_size must be > 0')

    match text:
        case str():
            text = [text]
        case pd.Series():
            text = text.tolist()

    clf = pipeline(*args, **kwargs)
    results = ({pred['label']: pred['score'] for pred in res}
               for i in trange(0, len(text), batch_size)
               for res in clf(text[i:i + batch_size]))

    return pd.DataFrame(results)
