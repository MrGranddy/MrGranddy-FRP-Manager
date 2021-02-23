import json

from .settings import status_code as st

class Parameters:
    def __init__(self):
        self.SUB_POINTS_FOR_MAIN_INCREASE = 2
        self.INIT_MAIN_SPARE_POINTS = 5

parameters = Parameters()

class Character:
    def __init__(self):

        self.character_name = None
        self._class = None
        self.gender = None

        self.level = 1
        self.hp = 3

        self.head_name = ""
        self.body_name = ""

        self.spare_skill_points = {
            "main": parameters.INIT_MAIN_SPARE_POINTS,
            "str": 0,
            "agi": 0,
            "int": 0,
            "cha": 0,
        }

        self.main_skills = {
            "str": 3,
            "agi": 3,
            "int": 3,
            "cha": 3,
        }

        self.sub_skills = {
            "str": {
                "endurance": 3,
                "power": 3,
                "weapon": 3,
            },

            "agi": {
                "sneak": 3,
                "speed": 3,
                "precision": 3,
            },

            "int": {
                "spell": 3,
                "herbalogy": 3,
                "awareness": 3,
            },

            "cha": {
                "persuasion": 3,
                "luck": 0,
            },
        }

    def level_up(self):
        
        self.level += 1
        self.spare_skill_points["main"] += 3

        return st.SUCCESS

    def main_skill_up(self, skill, amount ):

        if self.spare_skill_points["main"] >= amount:

            self.spare_skill_points["main"] -= amount
            self.main_skills[skill] += amount
            self.spare_skill_points[skill] += parameters.SUB_POINTS_FOR_MAIN_INCREASE * amount

            return st.SUCCESS
        else:
            return st.NOT_ENOUGH

    def sub_skill_up(self, skill, amount):

        main_key = [ key for key, val in self.sub_skills.items() if skill in val ][0]

        if self.spare_skill_points[main_key] >= amount:
            
            self.spare_skill_points[main_key] -= amount
            self.sub_skills[main_key][skill] += amount

            return st.SUCCESS
        
        else:
            return st.NOT_ENOUGH


    def character_setup(self, args):
        name = args['input_character_name']
        _class = args['input_character_class']
        gender = args['input_character_gender']
        body_name = args['input_body_name']
        head_name = args['input_head_name']
        added_main_skills = json.loads(args['input_added_main_skills'])
        added_sub_skills = json.loads(args['input_added_sub_skills'])

        self.character_name = name
        self._class = _class
        self.gender = gender

        self.body_name = body_name
        self.head_name = head_name

        for main_skill in added_main_skills:
            key = main_skill[0].lower()
            val = main_skill[1]
            status = self.main_skill_up(key, val)

            if status != st.SUCCESS:
                return -1

        for sub_skill_main in added_sub_skills:
            for sub_skill in sub_skill_main:
                key = sub_skill[1].lower()
                val = sub_skill[2]
                status = self.sub_skill_up(key, val)

                if status != st.SUCCESS:
                    return -1

        return 0

    def character_update(self, args):

        added_main_skills = json.loads(args['input_added_main_skills_update'])
        added_sub_skills = json.loads(args['input_added_sub_skills_update'])

        for main_skill in added_main_skills:
            key = main_skill[0].lower()
            val = main_skill[1]
            status = self.main_skill_up(key, val)

            if status != st.SUCCESS:
                return -1

        for sub_skill_main in added_sub_skills:
            for sub_skill in sub_skill_main:
                key = sub_skill[1].lower()
                val = sub_skill[2]
                status = self.sub_skill_up(key, val)

                if status != st.SUCCESS:
                    return -1

        return 0
