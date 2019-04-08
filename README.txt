-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
tomography image tools for ABSL
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

tomo-rename.py
--------------
rename tomography images aquired in serial em, replace square brackets with '_' fix -0.0 tilt notation.  Standardize naming convention to:

	user_selected_name_tiltnumber_tilt_tilt_imagenumber.mrc
	IE
	my_awesome_tomo_1_01_-60_00_123456
	my_awesome_tomo_1_02_-56_00_123567

run in the directory with the raw tomoimages 


tomo-stacker.py
---------------
make stacks from individual tomogram images
USAGE: tomo-stacker.py <images search string> <tilt axis angle> <pixel size (A)>

must be used on image named with the aboive convention.
needs access to IMOD's alterheader and newstack commands to work.

