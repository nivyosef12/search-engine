from fastapi import APIRouter
from config.database import client
from models.search_results_model import SearchResult
from schemas.search_results_schema import search_result_serializer, search_results_serializer

api_router = APIRouter()
