from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ....schemas.chat import ChatRequest, ChatResponse
from ....services.ai_service import AIService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    ai_service: AIService = Depends()
):
    """Chat with AI agent"""
    return await ai_service.process_chat(request)

@router.post("/search")
async def ai_search_jobs(
    request: ChatRequest,
    ai_service: AIService = Depends()
):
    """Search jobs using AI"""
    return await ai_service.search_jobs(request)

@router.post("/apply")
async def ai_apply_job(
    request: ChatRequest,
    ai_service: AIService = Depends()
):
    """Apply to job using AI"""
    return await ai_service.apply_to_job(request) 