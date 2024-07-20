from app import db
from app.models import Game
import openai

class GameLogic:
    def __init__(self):
        self.initial_prompt = "You are a master detective novelist in the style of Sir Arthur Conan Doyle. Create an interactive Sherlock Holmes-inspired mystery game for the user. Begin the story in Victorian London, setting the scene and introducing a puzzling case. After the introduction, present the user with 4 numbered choices for how to proceed with the investigation. These choices should be meaningful and lead to different story branches. After I give you the user's choice, continue the story based on that choice, always ending with 4 new numbered options. The story should include clues, red herrings, interesting characters, and plot twists. Maintain the atmosphere and deductive reasoning style typical of Sherlock Holmes stories. Keep each response under 200 words for readability. Begin the story now."

    def start_new_game(self):
        response = self.get_ai_response(self.initial_prompt)
        game = Game(current_scene=response)
        db.session.add(game)
        db.session.commit()
        return game.id, response

    def make_choice(self, game_id, choice):
        game = Game.query.get(game_id)
        if game:
            prompt = f"{game.current_scene}\n\nchoice: {choice}\n\n Present the next scene and 4 new choices."
            response = self.get_ai_response(prompt)
            game.current_scene = response
            game.story_progress += 1
            db.session.commit()
            return response
        return None

    def get_ai_response(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()