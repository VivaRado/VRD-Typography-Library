VRD (VivaRado) Typography Library
===================

The library that VRD's Typography Department is using for authoring fonts.
Includes Autokerning(Class based and Flat), Componentization, Conversion of UFO to SVG and back.

Old Scripts Include
Exporting and Importing for FontLab and Illustrator.


The endpoints of the Lib so far, as argument functions:  

**EFO to SVGs**
```
-s (source EFO)  
-f (the weights of the font to convert: "reg,bld,...")  
```
**SVGs to EFO**
```
-s (source EFO)  
-f (the weights of the font to convert: "reg,bld,...")  
```
**EFO to UFOs**
```
-s (source EFO)  
-o (output directory)
-f (the weights of the font to convert)  
-k (what kerning to export / "flat" or "comp")
```
**UFOs to EFO** 
```
-s (source fontinfo.JSON)
-o (Optional, Default Output Directory for EFO is fontinfo.JSON Directory or Provide)
```
**Kerning Autokern**
```
-s (source fontinfo.JSON)  
-o (Optional, Default Output Directory for EFO is fontinfo.JSON Directory or Provide) 
```
**Kerning Compress Flat**
```
-s (source EFO)  
-f (the weights of the font to compress: "reg,bld,...") 
```
**Kerning Extract Similarity** 
```
-s (source EFO)  
-f (the weights of the font to extract similarity from - just needs one weight)  
-p (purpose - Either for Components or Kerning: "comp" or "kern")
```
**Componentize EFO** 
```
-s (source EFO)  
-f (the weights of the font to componentize: "reg,bld,...")
```

**VivaRado is thankful for all your observations :+1: please submit any issues at support@vivarado.com - with Subject: ISSUE:Topic, or send it here on github**

[By VivaRado](https://www.vivarado.com)
