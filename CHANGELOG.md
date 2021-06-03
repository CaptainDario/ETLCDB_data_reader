# ETL Data Reader : Changelog

## v 2.1.3

features:
  - parameter to set the integer from which the folder names will start when saving to file 

------------------------------------------------------------
## v 2.1.2

fixed:
  - `save_to` crashes when some special characters should be saved to file
  - certain images were not saved correctly (were saved completely black) 

------------------------------------------------------------
## v 2.1.1

fixed:
  - `save_to` has obsolete parameter which causes a crash

------------------------------------------------------------
## v 2.1

features:
  - parameter to save all images and labels to disk

fixed:
  - loading always returns numpy arrays
  - katakana encoded with "KE", etc. are now converted to ケ, etc.
  - some of the empty images are not loaded anymore

------------------------------------------------------------
## v 2.0:
features:
- multi processed loading of the data is now possible

changes:
- breaking
  - the parameter 'include' expects now a list 

------------------------------------------------------------
## v 1.0:
added features:
- load all images and labels from the ETL data set