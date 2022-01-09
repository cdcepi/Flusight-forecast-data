#mcandrew;

PYTHON:=python3 -W ignore

COMMITprefix:=Forecasts generated for LUcompUncertLab-VAR2_plusCOVID model on
COMMITsuffix:=$(shell date +"%Y-%m-%d")

COMMIT:=$(COMMITprefix) $(COMMITsuffix)

runall: collectAndFormatData generateForecasts postprocess checkLocations sync
.PHONY: runall

collectAndFormatData:
	$(PYTHON) LUcompUncertLab-dataprep.py && echo "data prepared"

generateForecasts:
	$(PYTHON) LUcompUncertLab-VAR2_plusCOVID.py && echo "forecasts generated"

postprocess:
	$(PYTHON) LUcompUncertLab-postProcess.py && echo "Post process complete"

checkLocations:
	$(PYTHON) checkFile.py && echo "Location information"

add:
	git add .

commit:
	git commit -m "$(COMMIT)"

push:
	git push

send: add commit push
.PHONY: send

sync:
	rsync -arvz --progress ../LUcompUncertLab-VAR2_plusCOVID/ ../../../2022FluSightModels/LUcompUncertLab-VAR2_plusCOVID && \
	make -C ../../../2022FluSightModels/
