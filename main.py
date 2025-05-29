import sys
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))
sys.path.append(path + '\\\\merge_clean_and_api')
sys.path.append(path + '\\\\csv')
sys.path.append(path + '\\\\clean_and_merge')
sys.path.append(path + '\\\\call_api')
sys.path.append(path + '\\\\tools')
sys.path.append(path)

from tools import get_tmdb

#print("clean_akas start...")
#from clean_and_merge import clean_akas
#print("clean_akas end, clean_name_basics start...") 
#from clean_and_merge import clean_name_basics
#print("clean_name_basic end, clean_title_basics start...") 
#from clean_and_merge import clean_title_basics
#print("clean_title_basic end, clean_title_principals start...") 
#from clean_and_merge import clean_title_principals
#print("clean_title_principals end, clean_title_ratings start...") 
#from clean_and_merge import clean_title_ratings
#print("clean_title_ratings end") 
#
#print("merge_movies start...")
#from clean_and_merge import merge_movies
#print("merge_movies end") 
#
#print("filter_principals start...")
#from clean_and_merge import filter_principals
#print("filter_principals end, filter_name start...") 
#from clean_and_merge import filter_name
#print("filter_name end") 
#
#print("find_by_id start...")
#from call_api import find_by_id
#print("find_by_id end, key_words start...") 
#from call_api import key_words
#print("key_words end, movie_video start...") 
#from call_api import movie_video
#print("movie_video end, people_details start...") 
#from call_api import people_details
#print("people_details end") 
#
#print("merge_movies start...")
#from merge_clean_and_api import merge_movies
#print("merge_movies end, merge_intervenants start...") 
#from merge_clean_and_api import merge_intervenants
print("merge_intervenants end, intermediate_table start...") 
from merge_clean_and_api import intermediate_table
print("intermediate_table end") 

print("add_recos start...")
from ML import add_recos
print("add_recos end") 