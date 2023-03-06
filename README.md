# Django

## Start Server
```
python3 manage.py runserver
```

# Conda

## First Time Setup
```
conda env create -n matchr --file environment.yml
```
```
conda activate matchr
```

## Import Environment
```
conda deactivate
```
```
conda env remove -n matchr
```
```
conda env create -n matchr -f environment.yml
```
```
conda activate matchr
```

## Add a Package

If you need to add a package to the environment run:
```
conda install -n matchr PACKAGE_NAME
```

Then open **environment.yml** and add PACKAGE_NAME alphabetically under the **dependencies** header  

## Activate Environment
```
conda activate matchr
```

## Deactivate Environment
```
conda deactivate
```
