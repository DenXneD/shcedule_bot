import pandas as pd
from classes.Tools import BackTool


class Parser:
    @classmethod
    def parse(cls, shift):
        df = pd.read_excel(r'files/ipz_schedule.xlsx').values.tolist()
        groups_schedule = {}

        for i in range(len(df[0]) - 2):
            groups_schedule[df[0][i + 2]] = {"Понеділок": {'09:00-10:20': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '10:30-11:50': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '12:10-13:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '13:40-15:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '15:10-16:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '16:40-18:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '18:10-19:30': {"Пара": 'nan', "Аудиторія": 'nan'}},
                                             "Вівторок":  {'09:00-10:20': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '10:30-11:50': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '12:10-13:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '13:40-15:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '15:10-16:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '16:40-18:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '18:10-19:30': {"Пара": 'nan', "Аудиторія": 'nan'}},
                                             "Середа":    {'09:00-10:20': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '10:30-11:50': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '12:10-13:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '13:40-15:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '15:10-16:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '16:40-18:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '18:10-19:30': {"Пара": 'nan', "Аудиторія": 'nan'}},
                                             "Четвер":    {'09:00-10:20': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '10:30-11:50': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '12:10-13:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '13:40-15:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '15:10-16:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '16:40-18:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '18:10-19:30': {"Пара": 'nan', "Аудиторія": 'nan'}},
                                             "П\'ятниця": {'09:00-10:20': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '10:30-11:50': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '12:10-13:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '13:40-15:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '15:10-16:30': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '16:40-18:00': {"Пара": 'nan', "Аудиторія": 'nan'},
                                                           '18:10-19:30': {"Пара": 'nan', "Аудиторія": 'nan'}}}

        if str(BackTool.week_of_study(shift) % 2) == '1':
            n = 1
        else:
            n = 3

        for i in range(n, len(df) - 1, 4):
            objects = df[i]
            links = df[i + 1]

            k = 2
            for key in groups_schedule:
                groups_schedule[key][objects[0]][objects[1]]["Пара"] = objects[k]
                groups_schedule[key][objects[0]][objects[1]]["Аудиторія"] = links[k]
                k += 1

        return groups_schedule  # Має вигляд { 'Назва групи': { 'День': {'Період': {'Пара': str, 'Аудиторія': str}}}

    @classmethod
    def prep_parse(cls):
        return pd.read_excel(r'files/prep_info.xlsx').values.tolist()
