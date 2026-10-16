from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from core.config import settings
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM, StoryOptionLLM
from core.procedural_generator import ProceduralStoryEngine
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class StoryGenerator:

    @classmethod
    def _get_api_key(cls):
        return (
            os.getenv("CHOREO_OPENAI_CONNECTION_OPENAI_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or settings.OPENAI_API_KEY
            or ""
        ).strip()

    @classmethod
    def _get_llm(cls):
        api_key = cls._get_api_key()
        serviceurl = os.getenv("CHOREO_OPENAI_CONNECTION_SERVICEURL")

        if api_key and serviceurl:
            return ChatOpenAI(model="gpt-4o-mini", api_key=api_key, base_url=serviceurl, temperature=0.8)
        elif api_key:
            return ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.8)

        return None

    _llm_quota_exhausted = False

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm() if not cls._llm_quota_exhausted else None
        story_structure = None

        if llm:
            try:
                story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

                prompt = ChatPromptTemplate.from_messages([
                    ("system", STORY_PROMPT),
                    ("human", f"Create a unique, immersive choose-your-own-adventure story with this exact theme: {theme}")
                ]).partial(format_instructions=story_parser.get_format_instructions())

                raw_response = llm.invoke(prompt.invoke({}))

                response_text = raw_response
                if hasattr(raw_response, "content"):
                    response_text = raw_response.content

                story_structure = story_parser.parse(response_text)
            except Exception as e:
                err_str = str(e)
                if "insufficient_quota" in err_str or "credit_balance_exhausted" in err_str:
                    cls._llm_quota_exhausted = True
                logger.warning(f"LLM generation failed ({e}), using dynamic procedural engine for theme '{theme}'.")
                story_structure = None

        if not story_structure:
            story_structure = ProceduralStoryEngine.generate(theme)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)
        root_node_data = cls._ensure_minimum_depth(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _ensure_minimum_depth(cls, node_data, depth: int = 1, minimum_depth: int = 3) -> StoryNodeLLM:
        node = node_data if isinstance(node_data, StoryNodeLLM) else StoryNodeLLM.model_validate(node_data)

        if node.isEnding:
            return node

        if not node.options:
            return node.model_copy(update={
                "isEnding": True,
                "isWinningEnding": False,
                "options": []
            })

        padded_options = [
            StoryOptionLLM(
                text=option.text,
                nextNode=cls._ensure_minimum_depth(option.nextNode, depth + 1, minimum_depth).model_dump()
            )
            for option in node.options
        ]
        return node.model_copy(update={"options": padded_options})

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data, is_root: bool = False) -> StoryNode:
        if isinstance(node_data, dict):
            content = node_data.get("content", "")
            is_ending = bool(node_data.get("isEnding", False))
            is_winning_ending = bool(node_data.get("isWinningEnding", False))
            options_raw = node_data.get("options", [])
        else:
            content = getattr(node_data, "content", "")
            is_ending = bool(getattr(node_data, "isEnding", False))
            is_winning_ending = bool(getattr(node_data, "isWinningEnding", False))
            options_raw = getattr(node_data, "options", [])

        node = StoryNode(
            story_id=story_id,
            content=content,
            is_root=is_root,
            is_ending=is_ending,
            is_winning_ending=is_winning_ending,
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and options_raw:
            options_list = []
            for option_data in options_raw:
                if isinstance(option_data, dict):
                    opt_text = option_data.get("text", "")
                    next_node_data = option_data.get("nextNode", {})
                else:
                    opt_text = getattr(option_data, "text", "")
                    next_node_data = getattr(option_data, "nextNode", {})

                if isinstance(next_node_data, dict):
                    next_node_data = StoryNodeLLM.model_validate(next_node_data)

                child_node = cls._process_story_node(db, story_id, next_node_data, is_root=False)

                options_list.append({
                    "text": opt_text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node