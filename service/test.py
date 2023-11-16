# import func.creation.creation as creation
# import func.rhythm.scheduler
# from func.rhythm.scheduler import Scheduler
# from func.rhythm.checker import Checker
# from func.rhythm.generator import Generator
# from config.rhythm_config import rhymebooks

# print(creation.Creation().create_poem("/static/imgs/abc.jpg","薄霭", 1, "踏莎行",
#                                       "中华新韵", "丑"))
# s: func.rhythm.scheduler.Scheduler = Scheduler(Checker(), Generator(Checker()))
# print(s.generate_rhyme_poem(["春", "秋月", "残花", "枯叶"], rhymebooks["平水韵"], "踏莎行", 1, "遇"))


from utils.rhyme_utils import get_poem_can_rhyme

print(get_poem_can_rhyme(0, "七律平起首句入韵", "平水韵"))
