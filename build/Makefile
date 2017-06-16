CUR_DATE=`date +'%m_%d_%Y'`
# lanier4@illinois.edu      -- build jupyter notebooks images for KnowEnG

build_base_image:
	cd knoweng_basenb/; docker build --no-cache -t knowengdev/jupyter_notebooks:base_image .
# 18 minutes

push_base_image:
	docker push knowengdev/jupyter_notebooks:base_image

build_pipelines_notebook:
	cd knoweng_pipelines/; docker build --no-cache -t knowengdev/jupyter_notebooks:$(CUR_DATE) .
# 4 minute

build_pipelines_update:
	cd knoweng_pipelines_update/; docker build --no-cache -t knowengdev/jupyter_notebooks:$(CUR_DATE) .

login_to_dockerhub:
	docker login --username=$(username) --email=$(email)

pipelines_notebook_to_dockerhub:
	docker push knowengdev/jupyter_notebooks:$(CUR_DATE)


