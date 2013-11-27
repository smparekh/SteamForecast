SteamForecast
=============

Steam sale predictor for ECE-4984

##Requirements:
- Numpy <br>
Ubuntu:
<pre>
    sudo apt-get install python-numpy
</pre>
Fedora:
<pre>
    sudo yum install numpy
</pre>

###Usage:
- kNN.py <br>
Inputs
<pre>
    kNN.py -i input_file -k range
</pre>
Outputs
<pre>
    Input file name
    Current day
    Sale Day Range
    Sale days, non-sale days
</pre>

![kNN Usage Image](https://github.com/carbon-/SteamForecast/raw/master/screenshots/kNN_usage.png "kNN Usage")

###TODO:
- k-Nearest Neighbor (using Date difference) - Shaishav
- Web Parser - Travis
- Database set up - Travis & Shaishav

###Recent Changes:
Added current year to first line of dataset so saleDates matrix size is known, and matrix can be properly created.
