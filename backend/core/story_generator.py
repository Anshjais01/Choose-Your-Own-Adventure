from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from core.config import settings
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM, StoryOptionLLM
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
            return ChatOpenAI(model="gpt-4o-mini", api_key=api_key, base_url=serviceurl)
        elif api_key:
            return ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

        return None

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm()
        story_structure = None

        if llm:
            try:
                story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

                prompt = ChatPromptTemplate.from_messages([
                    ("system", STORY_PROMPT),
                    ("human", f"Create the story with this theme: {theme}")
                ]).partial(format_instructions=story_parser.get_format_instructions())

                raw_response = llm.invoke(prompt.invoke({}))

                response_text = raw_response
                if hasattr(raw_response, "content"):
                    response_text = raw_response.content

                story_structure = story_parser.parse(response_text)
            except Exception as e:
                logger.warning(f"LLM generation failed, using procedural fallback: {e}")
                story_structure = None

        if not story_structure:
            story_structure = cls._generate_fallback_story(theme)

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
    def _generate_fallback_story(cls, theme: str) -> StoryLLMResponse:
        theme_clean = theme.strip().title() or "Adventure"
        return StoryLLMResponse(
            title=f"The Legend of {theme_clean}",
            rootNode=StoryNodeLLM(
                content=f"You find yourself standing at the threshold of a mysterious realm: {theme}. The atmosphere is charged with electric silence. Ahead, two distinct paths present themselves.",
                isEnding=False,
                isWinningEnding=False,
                options=[
                    StoryOptionLLM(
                        text="Investigate the strange glowing artifact in the center chamber",
                        nextNode={
                            "content": "The artifact hums with ancient power as you approach. Intricate runes swirl across its surface, and a concealed stone pedestal rises from the floor.",
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Carefully align the ancient glyphs on the pedestal",
                                    "nextNode": {
                                        "content": "A brilliant wave of golden light washes over the chamber! The artifact opens to reveal the ancient wisdom and treasures of the realm. You have successfully conquered the quest!",
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Grab the glowing artifact and pull it from its mount",
                                    "nextNode": {
                                        "content": "A sudden tremor shakes the ground as security mechanisms activate! Stone walls slam shut, sealing you in eternal darkness. Your journey ends here.",
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    ),
                    StoryOptionLLM(
                        text="Follow the narrow shadowed passage leading deeper into the unknown",
                        nextNode={
                            "content": "You creep down the narrow corridor. A shadowy guardian steps forward, its eyes burning like blue embers. It demands to know your purpose.",
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Bow with respect and state your quest truthfully",
                                    "nextNode": {
                                        "content": "The guardian nods with deep reverence. It steps aside and presents you with the enchanted talisman of champions. You walk forth victorious and revered!",
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Draw your weapon and attempt to charge through",
                                    "nextNode": {
                                        "content": "The guardian raises its staff, casting an illusionary maze that traps your senses forever. You are lost in the shadows. Game over.",
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    )
                ]
            )
        )

    @classmethod
    def _ensure_minimum_depth(cls, node_data, depth: int = 1, minimum_depth: int = 4) -> StoryNodeLLM:
        node = node_data if isinstance(node_data, StoryNodeLLM) else StoryNodeLLM.model_validate(node_data)

        if node.isEnding:
            padded_node = node
            for _ in range(max(0, minimum_depth - depth)):
                padded_node = StoryNodeLLM(
                    content="The path forward reveals one final challenge before the journey is decided.",
                    isEnding=False,
                    isWinningEnding=False,
                    options=[StoryOptionLLM(
                        text="Face the final challenge",
                        nextNode=padded_node.model_dump()
                    )]
                )
            return padded_node

        if not node.options:
            next_node = StoryNodeLLM(
                content="The consequences of your choice finally become clear.",
                isEnding=True,
                isWinningEnding=False,
                options=[]
            )
            for _ in range(max(0, minimum_depth - depth - 1)):
                next_node = StoryNodeLLM(
                    content="A final obstacle stands between you and the outcome of your quest.",
                    isEnding=False,
                    isWinningEnding=False,
                    options=[StoryOptionLLM(
                        text="Continue toward the outcome",
                        nextNode=next_node.model_dump()
                    )]
                )
            return node.model_copy(update={
                "options": [StoryOptionLLM(
                    text="Continue the adventure",
                    nextNode=next_node.model_dump()
                )]
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