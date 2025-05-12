from agents import Agent
from agents import Model
from agents import ModelSettings

from ..model import get_openai_model
from ..prompts.summary import INSTRUCTIONS
from ..prompts.summary import Summary


def get_summary_agent(
    lang: str,
    length: int = 200,
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
) -> Agent:
    """Get the summary agent."""
    if model is None:
        model = get_openai_model()

    return Agent(
        name="summary_agent",
        instructions=INSTRUCTIONS.format(lang=lang, length=length),
        model=model,
        output_type=Summary,
    )
