VRD TYPL (VivaRado Typography Library)
===================

The library that VRD's Typography Department is using for authoring fonts.
Includes Autokerning(Class based and Flat), Componentization and Anchoring, Conversion of UFO to SVG and back.

Old Scripts Include
Exporting and Importing for FontLab and Illustrator.

The endpoints of the VRD TYPL so far, as argument functions:  

[**EFO to UFOs:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/efo)
```
efo_to_ufos.py

-s (source EFO)  
-o (output directory)
-f (the weights of the font to convert)  
-k (what kerning to export / "flat" or "comp")
```
[**UFOs to EFO:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/efo)
```
ufos_to_efo.py

-s (source fontinfo.JSON)
-o (Optional, Default Output Directory for EFO is fontinfo.JSON Directory or Provide)
```
[**EFO to VAR:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/efo)
```
efo_to_var.py

-s (source EFO)
-o (output file: name.ttf, name.otf ...)
```
[**EFO to SVGs:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/efo)
```
efo_to_svgs.py

-s (source EFO)  
-f (the weights of the font to convert: "reg,bld,...")  
```
[**SVGs to EFO:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/efo)
```
svgs_to_efo.py

-s (source EFO)  
-f (the weights of the font to convert: "reg,bld,...")  
```
[**Kerning Extract Similarity**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/similarity_extractor)
```
kerning_extract_similarity.py

-s (source EFO)  
-f (the weights of the font to extract similarity from - just needs one weight)  
-p (purpose - Either for Components or Kerning: "comp" or "kern")
```
[**Kerning Autokern:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/kerning)
```
kerning_autokern.py

-s (source fontinfo.JSON)  
-o (Optional, Default Output Directory for EFO is fontinfo.JSON Directory or Provide) 
```
[**Kerning Compress Flat:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/compress_kerning)
```
kerning_compress_flat.py

-s (source EFO)  
-f (the weights of the font to compress: "reg,bld,...") 
```
[**Componentize EFO:**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/components)
```
componentize_efo.py

-s (source EFO)  
-f (the weights of the font to componentize: "reg,bld,...")
```
[**Kerning Adjust UI (beta):**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/kerning_adjust)
```
cd "/kerning_adjust"

npm install

node app --source (source EFO)
```
[**Transfer Kerning to Slanted (alpha):**](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/generic/transfer_kerning_to_slanted.pdf)
```
transfer_kerning_to_slanted.py

-s (source EFO)  
-f (the weights of the font to get kerning info: "reg,bld,...")
-t (the weights of the font to put kerning info: "reg,bld,...")
-d (Slant Degrees: "12")
```
------

[By VivaRado](https://www.vivarado.com)

<sup>
VivaRado is thankful for all your observations :+1: please submit any issues at support@vivarado.com - with Subject: ISSUE:Topic, or send it here on github!
</sup>
