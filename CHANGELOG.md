# ETL Data Reader : Changelog

## v 2.1

features:
  - parameter to save all images and labels to disk

fixed:
  - loading always returns numpy arrays
  - katakana encoded with "KE", etc. are now converted to ケ, etc.
  - some of the empty images are not loaded anymore
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