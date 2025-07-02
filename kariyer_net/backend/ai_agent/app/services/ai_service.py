from typing import List, Optional
from ..core.ai_client import AIClient
from ..schemas.chat import ChatRequest, ChatResponse
from ..schemas.commands import ParsedCommand
from ..services.command_parser import CommandParser
import httpx
from ..core.config import settings
import openai
import json

class AIService:
    def __init__(self):
        self.ai_client = AIClient()
        self.command_parser = CommandParser()

    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """Process chat message using GPT for intent extraction, then call real APIs and format response."""
        # 1. Build strict system prompt
        system_prompt = (
            "You are JobBot, the official kariyer.net assistant. You must ONLY return a valid JSON object with these keys: "
            "intent (SEARCH_JOBS, APPLY_TO_JOB, GET_JOB_DETAILS), query, location, job_id, user_id. "
            "NEVER fabricate job data, NEVER answer in free text, NEVER add explanations, NEVER invent companies or jobs. "
            "If the user request is unclear, return: {\"intent\": \"UNKNOWN\"}. "
            "Your output must be valid JSON and nothing else."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ]
        # 2. Call OpenAI
        try:
            resp = await openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY).chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages
            )
            gpt_content = resp.choices[0].message.content.strip()
            print("[DEBUG] GPT raw response:", gpt_content)  # LOG GPT RESPONSE
        except Exception as e:
            return ChatResponse(response=f"⚠️ AI servisinde hata: {str(e)}", suggestions=[], actions=[])
        # 3. Parse JSON
        try:
            parsed = json.loads(gpt_content)
            print("[DEBUG] Parsed GPT JSON:", parsed)  # LOG PARSED JSON
        except Exception:
            print("[ERROR] Failed to parse GPT response as JSON.")
            return ChatResponse(response="⚠️ Yanıtı anlayamadım, lütfen daha açık yazar mısınız?", suggestions=[], actions=[])
        intent = parsed.get('intent')
        # 4. Route to correct API
        if intent == 'SEARCH_JOBS':
            params = {}
            if parsed.get('query'): params['query'] = parsed['query']
            if parsed.get('location'): params['location'] = parsed['location']
            if request.user_id: params['user_id'] = request.user_id
            print("[DEBUG] Calling job search API with params:", params)  # LOG API PARAMS
            async with httpx.AsyncClient() as client:
                api_resp = await client.get(f"{settings.JOB_SEARCH_SERVICE_URL}/api/v1/search", params=params)
                jobs_response = api_resp.json()
                print("[DEBUG] Job search API response:", jobs_response)  # LOG API RESPONSE
            jobs_list = jobs_response.get('jobs', [])
            print('[DEBUG] jobs_list type:', type(jobs_list))
            print('[DEBUG] jobs_list length:', len(jobs_list) if hasattr(jobs_list, '__len__') else 'N/A')
            print('[DEBUG] jobs_list contents:', jobs_list)
            response_text = "Hiç iş bulunamadı."
            if jobs_list:
                print('[DEBUG] jobs_list is truthy and has length:', len(jobs_list))
                jobs_str = "\n\n".join([
                    f"{i+1}. {job.get('title', 'İş Başlığı Yok')}\n"
                    f"   Şirket: {job.get('company_name', 'Bilinmeyen Şirket')}\n"
                    f"   Lokasyon: {job.get('location', 'Bilinmeyen Lokasyon')}\n"
                    f"   Çalışma Şekli: {job.get('work_mode', 'Bilinmiyor')}\n"
                    f"   Maaş: {job.get('salary_min', '-')}-{job.get('salary_max', '-')} TL\n"
                    f"   Açıklama: {job.get('description', '')[:100]}..."
                    for i, job in enumerate(jobs_list)
                ])
                response_text = f"İşte bulduğum işler:\n\n{jobs_str}\n\nBaşka bir şehirde iş bakmak ister misiniz?"
            print('[DEBUG] Final response_text:', response_text)
            return ChatResponse(response=response_text, suggestions=["Daha fazla iş göster", "Farklı şehirde ara"], actions=[])
        elif intent == 'APPLY_TO_JOB':
            job_id = parsed.get('job_id')
            user_id = request.user_id or parsed.get('user_id')
            if not job_id or not user_id:
                return ChatResponse(response="Başvuru için iş ID ve kullanıcı ID gerekli.", suggestions=[], actions=[])
            print(f"[DEBUG] Calling apply API for job_id={job_id}, user_id={user_id}")
            async with httpx.AsyncClient() as client:
                api_resp = await client.post(f"{settings.JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}/apply", json={"user_id": user_id})
                result = api_resp.json()
                print("[DEBUG] Apply API response:", result)
            msg = result.get('message') or str(result)
            return ChatResponse(response=f"Başvuru sonucu: {msg}", suggestions=[], actions=[])
        elif intent == 'GET_JOB_DETAILS':
            job_id = parsed.get('job_id')
            if not job_id:
                return ChatResponse(response="İş detayları için iş ID gerekli.", suggestions=[], actions=[])
            print(f"[DEBUG] Calling job details API for job_id={job_id}")
            async with httpx.AsyncClient() as client:
                api_resp = await client.get(f"{settings.JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}")
                job = api_resp.json()
                print("[DEBUG] Job details API response:", job)
            if job:
                response_text = f"İş Detayları:\nBaşlık: {job.get('job_name') or job.get('title')}\nAçıklama: {job.get('job_description', '')}\nŞirket: {job.get('company_name', '')}\nKonum: {job.get('city', job.get('location', ''))}"
            else:
                response_text = "İş detayları bulunamadı."
            return ChatResponse(response=response_text, suggestions=[], actions=[])
        else:
            print("[WARN] Unknown or missing intent from GPT.")
            return ChatResponse(response="Ne yapmak istediğinizi anlayamadım. Lütfen iş arama, başvuru veya detay isteğinizi açıkça belirtin.", suggestions=[], actions=[])

    async def search_jobs(self, request: ChatRequest) -> dict:
        """Search jobs using AI interpretation"""
        parsed_command = self.command_parser.parse_message(request.message)
        job_title = None
        location = None
        if parsed_command.commands:
            for cmd in parsed_command.commands:
                if cmd.type == "search":
                    job_title = cmd.parameters.get("job_title")
                    location = cmd.parameters.get("location")
        params = {"query": job_title or "", "location": location or ""}
        if request.user_id:
            params["user_id"] = request.user_id
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{settings.JOB_SEARCH_SERVICE_URL}/api/v1/search", params=params)
            return resp.json()

    async def apply_to_job(self, request: ChatRequest) -> dict:
        """Apply to job using AI interpretation"""
        parsed_command = self.command_parser.parse_message(request.message)
        job_id = None
        if parsed_command.commands:
            for cmd in parsed_command.commands:
                if cmd.type == "apply":
                    job_id = cmd.parameters.get("job_id")
        if not job_id:
            return {"error": "No job ID found in message."}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{settings.JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}/apply", json={"user_id": request.user_id})
            return resp.json()

    async def get_job_details(self, request: ChatRequest) -> dict:
        """Get job details by job_id if present in the message"""
        parsed_command = self.command_parser.parse_message(request.message)
        job_id = None
        if parsed_command.commands:
            for cmd in parsed_command.commands:
                if cmd.type == "get_job_details":
                    job_id = cmd.parameters.get("job_id")
        if not job_id:
            return {}
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{settings.JOB_POSTING_SERVICE_URL}/api/v1/jobs/{job_id}")
            return resp.json()

    def _generate_suggestions(self, parsed_command: ParsedCommand) -> List[str]:
        """Generate suggestions based on parsed command"""
        # Use intent or first command type for suggestions
        command_type = None
        if parsed_command:
            if parsed_command.commands and len(parsed_command.commands) > 0:
                command_type = parsed_command.commands[0].type
            else:
                command_type = parsed_command.intent
        if command_type == "search":
            return ["Try searching for jobs in another city", "Filter by company"]
        elif command_type == "apply":
            return ["Check job requirements", "Update your CV"]
        return ["Search for jobs", "Apply to a job"]

    def _generate_actions(self, parsed_command: ParsedCommand) -> List[dict]:
        """Generate actions based on parsed command"""
        actions = []
        command_type = None
        if parsed_command:
            if parsed_command.commands and len(parsed_command.commands) > 0:
                command_type = parsed_command.commands[0].type
            else:
                command_type = parsed_command.intent
        if command_type == "search":
            actions.append({"type": "search", "label": "Search Jobs"})
        elif command_type == "apply":
            actions.append({"type": "apply", "label": "Apply to Job"})
        return actions 