import os
from django.apps import AppConfig

default_app_config="manuscript_record.ManuscriptRecordConfig"

def getCurrentAppName(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class ManuscriptRecordConfig(AppConfig):
    name=getCurrentAppName(__file__)
    verbose_name="稿件记录模块"