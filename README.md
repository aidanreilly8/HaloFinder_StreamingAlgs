This repository holds code to use the Count Sketch frequent item finding algorithm as a halo finder, 
while including velocity information. The relevant code is found within the folder 6D.

Under that folder, freq_finders includes the count sketch code in the file csvec.py,
as well as the code to actually run it on data. This folder also includes code to get
exact frequency counts. 

As one would imagine, post_proc contains the code to analyze the results of the halo
finders in freq_finders.

Finally we have utils which has some code to write particle data to the appropriate 
binary format (this may or may not be useful), as well as a binary reader class
that is implemented int he halo finders.
