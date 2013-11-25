SteamForecast
=============

Steam sale predictor for ECE-4984

##Requirements:
- Numpy
Ubuntu:
<pre>
    sudo apt-get install python-numpy
</pre>
Fedora:
<pre>
    sudo yum install numpy
</pre>

###TODO:
- k-Nearest Neighbor (using Date difference) - Shaishav
- Web Parser - Travis
- Database set up - Travis & Shaishav

###Recent Changes:
Added current year to first line of dataset so saleDates matrix size is known, and matrix can be properly created.
