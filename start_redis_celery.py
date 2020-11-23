import os

if __name__=="__main__":
    try:
        os.system(r'celery -A periodical_management_system worker -l info --pool=solo')
    except Exception as error:
        raise ValueError(error)
