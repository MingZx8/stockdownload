# StockDownload
-GUI  
-download stock quotes historical data  
-input:  
  start date  
  end date  
  download path  
  symbols(choose from a listbox or import a symbol file in .csv or by input)


# Installation

python setup.py bdist_egg  

python setup.py install  


# Required library

pandas_datareader:  

use pip to download (pip pandas_datareader)

# Import & use

<pre><code>  from stockdownload import *  
  stockdownload()
</code></pre>
