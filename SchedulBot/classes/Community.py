from classes.Parser import Parser
from classes.Users import Users
from classes.Tools import BackTool


class Data:
    @classmethod
    def week_group_schedule(cls, user_id, shift=0):
        ipz_schedule = Parser.parse(shift)
        return ipz_schedule[Users.get_group_by_user_id(user_id)]

    @classmethod
    def today_group_schedule(cls, user_id, shift=0):
        ipz_schedule = Parser.parse(shift)[Users.get_group_by_user_id(user_id)]
        a = BackTool.rename_day(BackTool.get_time_dict(shift=shift)['day'])
        return ipz_schedule[a]
