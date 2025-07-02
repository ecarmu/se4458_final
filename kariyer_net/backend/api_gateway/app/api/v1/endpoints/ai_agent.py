from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import httpx, os

router = APIRouter()

# Enums
class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class RecommendationType(str, Enum):
    JOB = "job"
    SKILL = "skill"
    CAREER = "career"
    COURSE = "course"

# Pydantic models
class ChatMessage(BaseModel):
    role: MessageType
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    suggestions: List[str]
    confidence: float
    response_time: float

class JobRecommendation(BaseModel):
    job_id: int
    title: str
    company: str
    match_score: float
    reasons: List[str]
    skills_match: List[str]
    skills_missing: List[str]

class CareerAdvice(BaseModel):
    advice_type: str
    title: str
    description: str
    action_items: List[str]
    resources: List[str]

class SkillRecommendation(BaseModel):
    skill_name: str
    importance_score: float
    market_demand: str
    learning_resources: List[str]
    estimated_time: str

class AIAnalysisRequest(BaseModel):
    user_id: int
    resume_text: Optional[str] = None
    job_description: Optional[str] = None
    analysis_type: str  # resume_analysis, job_matching, skill_gap

# Chat and Conversation endpoints
@router.post("/chat")
async def chat_with_ai(chat_request: dict):
    """Proxy chat to AI agent microservice"""
    #AI_AGENT_SERVICE_URL = os.getenv("AI_AGENT_SERVICE_URL", "http://ai_agent:8002")
    AI_AGENT_SERVICE_URL = os.getenv("AI_AGENT_SERVICE_URL", "http://localhost:8003")  
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{AI_AGENT_SERVICE_URL}/api/v1/ai_agent/chat", json=chat_request)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{user_id}")
async def get_chat_history(user_id: int, limit: int = 20):
    """Get user's chat history with AI agent"""
    return {
        "conversations": [
            {
                "conversation_id": "conv_123",
                "title": "Job Search Help",
                "last_message": "How can I improve my resume?",
                "timestamp": datetime.now(),
                "message_count": 5
            }
        ]
    }

@router.get("/chat/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get specific conversation messages"""
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "role": "user",
                "content": "I need help finding a Python developer job",
                "timestamp": datetime.now()
            },
            {
                "role": "assistant",
                "content": "I'd be happy to help! Let me ask a few questions to provide better recommendations...",
                "timestamp": datetime.now()
            }
        ]
    }

# Job Recommendations
@router.post("/recommendations/jobs", response_model=List[JobRecommendation])
async def get_job_recommendations(user_id: int, limit: int = 10):
    """Get AI-powered job recommendations for user"""
    return [
        {
            "job_id": 1,
            "title": "Senior Python Developer",
            "company": "Tech Corp",
            "match_score": 0.92,
            "reasons": [
                "Your Python experience matches perfectly",
                "Location preference aligns",
                "Salary range is within your expectations"
            ],
            "skills_match": ["Python", "Django", "PostgreSQL"],
            "skills_missing": ["Kubernetes", "AWS"]
        }
    ]

@router.post("/recommendations/skills", response_model=List[SkillRecommendation])
async def get_skill_recommendations(user_id: int, current_skills: List[str]):
    """Get AI-powered skill recommendations"""
    return [
        {
            "skill_name": "Docker",
            "importance_score": 0.85,
            "market_demand": "High",
            "learning_resources": [
                "Docker Official Documentation",
                "Docker for Beginners Course",
                "Hands-on Docker Tutorial"
            ],
            "estimated_time": "2-4 weeks"
        }
    ]

# Career Guidance
@router.get("/career/advice", response_model=List[CareerAdvice])
async def get_career_advice(user_id: int, field: Optional[str] = None):
    """Get AI-powered career advice"""
    return [
        {
            "advice_type": "skill_development",
            "title": "Focus on Cloud Technologies",
            "description": "Cloud computing skills are in high demand. Consider learning AWS, Azure, or GCP.",
            "action_items": [
                "Take an AWS certification course",
                "Build a cloud-based project",
                "Practice with free tier services"
            ],
            "resources": [
                "AWS Free Tier",
                "Azure Learning Paths",
                "Google Cloud Training"
            ]
        }
    ]

@router.post("/career/path", response_model=Dict[str, Any])
async def get_career_path(user_id: int, current_role: str, target_role: str):
    """Get AI-powered career path guidance"""
    return {
        "current_role": current_role,
        "target_role": target_role,
        "path": [
            {
                "step": 1,
                "action": "Learn Advanced Python",
                "duration": "3-6 months",
                "resources": ["Advanced Python Course", "Python Design Patterns"]
            },
            {
                "step": 2,
                "action": "Master System Design",
                "duration": "6-12 months",
                "resources": ["System Design Interview", "Architecture Patterns"]
            }
        ],
        "estimated_time": "1-2 years",
        "success_probability": 0.85
    }

# Resume and Profile Analysis
@router.post("/analysis/resume")
async def analyze_resume(analysis_request: AIAnalysisRequest):
    """Analyze resume with AI"""
    return {
        "analysis": {
            "overall_score": 8.5,
            "strengths": [
                "Strong technical skills",
                "Good project descriptions",
                "Clear formatting"
            ],
            "improvements": [
                "Add quantifiable achievements",
                "Include more keywords",
                "Optimize for ATS"
            ],
            "keyword_matches": ["Python", "Django", "PostgreSQL"],
            "missing_keywords": ["Docker", "Kubernetes", "AWS"]
        },
        "suggestions": [
            "Add specific metrics to achievements",
            "Include more industry-relevant keywords",
            "Consider adding a skills section"
        ]
    }

@router.post("/analysis/job-matching")
async def analyze_job_matching(user_id: int, job_description: str):
    """Analyze job matching with AI"""
    return {
        "match_score": 0.78,
        "strengths": [
            "Technical skills align well",
            "Experience level matches",
            "Location preference fits"
        ],
        "concerns": [
            "Missing some required skills",
            "Experience might be slightly below requirements"
        ],
        "recommendations": [
            "Highlight relevant projects",
            "Emphasize transferable skills",
            "Consider upskilling in missing areas"
        ]
    }

# Interview Preparation
@router.get("/interview/prep/{job_id}")
async def get_interview_prep(job_id: int):
    """Get AI-powered interview preparation"""
    return {
        "job_id": job_id,
        "common_questions": [
            "Tell me about your experience with Python",
            "How do you handle debugging complex issues?",
            "Describe a challenging project you worked on"
        ],
        "technical_topics": [
            "Python data structures",
            "Database design",
            "API development"
        ],
        "company_research": {
            "company_info": "Tech Corp is a leading software company...",
            "recent_news": ["Company raised Series B funding", "Expanding to new markets"],
            "culture_fit": "Fast-paced, innovative, collaborative"
        },
        "preparation_tips": [
            "Review the job description thoroughly",
            "Prepare specific examples of your work",
            "Research the company's recent projects"
        ]
    }

@router.post("/interview/practice")
async def practice_interview(user_id: int, question: str):
    """Practice interview with AI"""
    return {
        "question": question,
        "ai_feedback": {
            "answer_quality": "Good",
            "technical_accuracy": 0.9,
            "communication": 0.8,
            "suggestions": [
                "Provide more specific examples",
                "Include quantifiable results",
                "Explain your reasoning more clearly"
            ]
        },
        "follow_up_questions": [
            "Can you elaborate on that specific project?",
            "How did you handle the challenges you mentioned?"
        ]
    }

# Market Insights
@router.get("/market/insights")
async def get_market_insights(field: Optional[str] = None):
    """Get AI-powered market insights"""
    return {
        "field": field or "software development",
        "trends": [
            "Remote work is becoming standard",
            "AI/ML skills are in high demand",
            "Cloud computing continues to grow"
        ],
        "salary_trends": {
            "entry_level": "$60,000 - $80,000",
            "mid_level": "$80,000 - $120,000",
            "senior_level": "$120,000 - $180,000"
        },
        "in_demand_skills": [
            "Python", "JavaScript", "React", "AWS", "Docker"
        ],
        "emerging_technologies": [
            "AI/ML", "Blockchain", "IoT", "Edge Computing"
        ]
    }

# Learning Recommendations
@router.get("/learning/recommendations")
async def get_learning_recommendations(user_id: int, skill: Optional[str] = None):
    """Get AI-powered learning recommendations"""
    return {
        "skill": skill or "Python",
        "courses": [
            {
                "title": "Complete Python Bootcamp",
                "platform": "Udemy",
                "rating": 4.8,
                "duration": "22 hours",
                "price": "$29.99"
            }
        ],
        "books": [
            {
                "title": "Python Crash Course",
                "author": "Eric Matthes",
                "rating": 4.7
            }
        ],
        "projects": [
            {
                "title": "Build a Web Application",
                "difficulty": "Intermediate",
                "estimated_time": "2-3 weeks"
            }
        ],
        "learning_path": [
            "Python Basics (2 weeks)",
            "Web Development with Django (4 weeks)",
            "Advanced Python Concepts (6 weeks)"
        ]
    } 