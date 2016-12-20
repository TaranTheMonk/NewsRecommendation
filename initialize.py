import RecommendationSys.src.CosSimilarity as cos_sim
import RecommendationSys.src.BuildInitialMatrix as build_pq_matrix
import RecommendationSys.src.UpdateMatrix as update_matrix
from pathlib import Path
import os

#cos_sim.main()
#build_pq_matrix.main()
if not Path(os.path.expanduser('~/.recsys/Data/Input/input.csv')).is_file():
	os.system('mkdir -p ~/.recsys/Data/Input')
	os.system('cat '' > ~/.recsys/Data/Input/input.csv')
update_matrix.main()
