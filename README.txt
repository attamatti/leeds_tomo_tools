-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
tomography image tools for ABSL
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Matt Iadanza - 2019/05/23

tomo-rename.py
--------------
rename tomography images aquired in serial em, replace square brackets with '_' fix -0.0 tilt notation.  Standardize naming convention to:

	user_selected_name_tiltnumber_tilt_tilt_imagenumber.mrc
	IE
	my_awesome_tomo_1_01_-60_00_123456
	my_awesome_tomo_1_02_-56_00_123567
	my_awesome_tomo_1_02_10_00_123567

run in the directory with the raw tomoimages

USAGE: 	tomo-rename.py <images search string>
IE:	tomo-rename.py matts_tomos*.mrc

tomo-stacker.py
---------------
make stacks from individual tomogram images
USAGE: 	tomo-stacker.py <images search string> <tilt axis angle> <pixel size (A)>
IE:	tomo-stacker.py matts_tomos*.mrc -4.5 2.13

must be used on image named with the above convention.
needs access to IMOD's alterheader and newstack commands to work
writes the stacked tomogram and .rawtlt files in a separate directory named for the tomogram.

If you use these programs to preprocess data used in publications plese cite them in your methods.
Iadanza MG. Leeds tomography tools v1.0. https://github.com/leeds_tomo_tools. DOI: 10.5281/zenodo.3247523
