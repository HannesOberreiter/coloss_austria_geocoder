# Coloss - Austria - honey bee colony winter mortality evaluation

**Archived** script is not used anymore, we now use the R Package TidyGeocoder as it fits more in our workflow.

Python script for geocoding the "string" location of the main wintering location to geographical locations using geopy and nominatim or google maps service.

## How to use the script

### First run install libraries

```cmd
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

### Run geocoder

Inside data folder should be one excel file with the name `data.xls`, including the columns `id` and `searchstring`. Please see example file inside folder.

Output will be generated in the same file.

```cmd
source env/bin/activate
python3 geocode.py
```

### Google API or Nominatim

If you got a google API key, generate a file in the root folder with the name `google-api-key.txt` with your generated api-key. If you don't have an Google API key it will use Nominatim Geocoding as service.

# MIT Licence 
Copyright (c) 2020 Hannes Oberreiter

# OSM Nominatim
https://operations.osmfoundation.org/policies/nominatim/
