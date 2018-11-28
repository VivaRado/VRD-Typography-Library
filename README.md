VRD (VivaRado) Typography Library
===================

The library that VRD's Typography Department is using for authoring fonts.
Includes Autokerning(Class based and Flat), Componentization, Conversion of UFO to SVG and back.

Old Scripts Include
Exporting and Importing for FontLab and Illustrator.


The endpoints of the Lib so far as argument functions:  

**EFO to SVGs**
```
-s (source EFO)  
-f (the weights of the font to convert)  
```
**SVGs to EFO**
```
-s (source EFO)  
-f (the weights of the font to convert)  
```
**EFO to UFOs**
```
-s (source EFO)  
-o (output directory)
-f (the weights of the font to convert)  
-k (what kerning to export / "flat" or "comp")
```
**Kerning Autokern**
```
-s (source EFO)  
-f (the weights of the font to kern)  
-c (compress using SIMEX - EFO/groups/kerning.plist)  
```
**Kerning Compress Flat**
```
-s (source EFO)  
-f (the weights of the font to compress)
```
**Kerning Extract Similarity** 
```
-s (source EFO)  
-f (the weights of the font to extract similarity from - just needs one weight)  
-p (purpose - Either for Components or Kerning: "comp" or "kern")
```

[By VivaRado](https://www.vivarado.com)
