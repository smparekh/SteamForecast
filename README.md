SteamForecast
=============

Steam sale predictor for ECE-4984

##Requirements:
- Numpy <br>
- Beautiful Soup 4 <br>
- Httplib2 <br>
- Psycopg2
Ubuntu:
<pre>
    sudo apt-get install python-numpy
</pre>
Fedora:
<pre>
    sudo yum install numpy
    sudo easy_install psycopg2
    sudo easy_install beautifulsoup4
    sudo easy_install httplib2
</pre>

###Usage:
- kNN.py <br>
Inputs
<pre>
    kNN.py -i input_file -k range
</pre>
Outputs
<pre>
    Correctly classified, false positives, misclassified
</pre>
OR to generate dataset for a game
<pre>
    kNN.py -g APP_ID
</pre>
Outputs
<pre>
    APP_ID.txt
</pre>

![kNN Usage Image](https://github.com/carbon-/SteamForecast/raw/master/screenshots/kNN_usage.png "kNN Usage")

###TODO:
- k-Nearest Neighbor (using Date difference) - Shaishav
- Web Parser - Travis
- Database set up - Travis & Shaishav

###Recent Changes:
Added current year to first line of dataset so saleDates matrix size is known, and matrix can be properly created.
