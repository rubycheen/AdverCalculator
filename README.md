# AdverCalculator
This is the project for Agriweather calculating statistics on the occurrence of adversity

## Demo
### 0. Prepare data and envirenment
Download data from [OpenWeatherMap](https://openweathermap.org/history-bulk#examples) website 
or [Demo File](https://drive.google.com/file/d/1CIne3YBVmkKYGsRi7G5T0QZAhfLtcUDT/view?usp=share_link) &&

```
conda create -n advercalculator
conda activate advercalculator
pip install json-logic-qubit
```

### 1. Test
Generate the `result.json` under the folder after run this shell file:

``` bash demo.sh ```

## File description
![AdverCalculator](https://user-images.githubusercontent.com/56534481/217914348-43b14c90-a489-4c1a-852e-806b9e7b0de8.jpg)

### `preprocess.py`
Merge hour data to date and filter out redundent columns

e.g. `python preprocess.py -i \[OpenWeatherMap\]C0K330.csv -o preprocessed.csv`

#### Arguments

`-i` input file path e.g. `-i \[OpenWeatherMap\]C0K330.csv`

`-o` output file path e.g. `-o preprocessed.csv`


### `sowing_crop.py`
Given crop properties to generate growth periods

e.g. `python sowing_crop.py -i preprocessed.csv -s 2019-01-01 -o cropped.csv`

#### Arguments

`-i` input file path e.g. `-i preprocessed.csv`

`-s` sowing date e.g. `-s 2019-01-01`

`-b` breed e.g. `-b rice`

`-t` thermal breaking points e.g. `-t "[200, 650, 950, 1100, 1250, 1700]"`

`-o` output file path e.g. `-o cropped.csv`


### `calculator.py`
Given data and conditions to caculate the occurrence of adversity

e.g. `python calculator.py -d cropped.csv -c conditions.json -o result.json`

#### Arguments

`-d` data file path e.g. `-d cropped.csv`

`-c` conditions file path e.g. `-c conditions.json`

`-o` output file path e.g. `-o result.json`
