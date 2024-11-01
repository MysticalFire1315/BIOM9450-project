from typing import Dict, Tuple

from app.main.util.dto import PersonDto
from app.main.util.decorator import require_logged_in_as
from flask import request
from flask_restx import Resource

api = PersonDto.api