import openai
from .config import settings

class AIClient:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_response(self, prompt: str) -> str:
        """Generate AI response"""
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful job search assistant for kariyer.net. Always answer as if you are a kariyer.net bot, and your answers are based on kariyer.net's job database and APIs."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}" 