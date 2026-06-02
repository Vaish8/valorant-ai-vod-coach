from app.llm.base import LLMClient


class MockLLMClient(LLMClient):
    def generate_text(self, prompt: str) -> str:
        return (
            "Overall Match Summary\n"
            "Based on the structured match statistics and saved tactical findings, "
            "the main coaching concern is repeated decision-making risk rather than a purely mechanical issue. "
            "The evidence suggests the player should focus on reducing early-round disadvantages, "
            "using utility before high-risk fights, and improving trade coordination.\n\n"
            "Top Issues\n"
            "1. Early-round risk: The analysis contains first-death related evidence, which indicates the player or team may be giving away opening advantages.\n"
            "2. Utility usage: Saved findings indicate utility was unused in at least one important lost-round scenario.\n"
            "3. Conversion quality: The match statistics and findings suggest that advantages or planted-spike situations were not consistently converted.\n\n"
            "Practical Improvement Plan\n"
            "- Avoid isolated early duels unless a teammate is ready to trade.\n"
            "- Use key utility before taking first contact instead of dying with utility available.\n"
            "- In post-plant situations, play time, hold crossfires, and avoid unnecessary peeks.\n\n"
            "Confidence and Limitations\n"
            "This summary is generated from structured statistics and saved rule-based findings only. "
            "It does not inspect raw gameplay video yet, so the advice should be treated as evidence-grounded but limited to the events currently stored in the backend."
        )