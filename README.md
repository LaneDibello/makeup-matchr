# makeup-matchr

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

## Export Environment
**Windows:**

```
conda env export --no-builds | findstr -v "prefix" > environment.yml
```

**Linux:**
```
conda env export --no-builds | grep -v "prefix" > environment.yml
```

## Activate Environment
```
conda activate matchr
```

## Deactivate Environment
```
conda deactivate
```
