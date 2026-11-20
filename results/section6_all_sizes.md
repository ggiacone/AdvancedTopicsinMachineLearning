# LittleLearner knowledge probe: results for all model sizes

Metric: `correct_norm` = accuracy, the model's answer is the option with the highest log-prob per byte. 252 multiple-choice items (4 options, chance = 25%), grades K-8. Band K5 = grades K-5, BeyondK5 = grades 6-8. Boundary drop = acc(K5) - acc(BeyondK5). DiD = drop(LittleLearner) - drop(Unfiltered), 95% CI from a bootstrap over items (resampled within each band). Option-only baseline = options scored after just "Answer:", without the question.

## 0.6b base models

Option-only baseline (accuracy with and without the question):

```
                        with question  option only  chance
model         band                                        
LittleLearner BeyondK5          0.333        0.238    0.25
              K5                0.601        0.250    0.25
Unfiltered    BeyondK5          0.405        0.262    0.25
              K5                0.583        0.185    0.25
```

Same, split by subject:

```
                                with question  option only
model         subject band                                
LittleLearner math    BeyondK5          0.167        0.146
                      K5                0.479        0.125
              science BeyondK5          0.556        0.361
                      K5                0.764        0.417
Unfiltered    math    BeyondK5          0.167        0.167
                      K5                0.427        0.083
              science BeyondK5          0.722        0.389
                      K5                0.792        0.319
```

Accuracy by grade (%, 95% Wilson CI lo/hi, correct/total):

```
model LittleLearner                     Unfiltered                    
                acc    lo    hi correct        acc    lo    hi correct
grade                                                                 
K              78.6  60.5  89.8   22/28       78.6  60.5  89.8   22/28
1              57.1  39.1  73.5   16/28       46.4  29.5  64.2   13/28
2              64.3  45.8  79.3   18/28       67.9  49.3  82.1   19/28
3              53.6  35.8  70.5   15/28       42.9  26.5  60.9   12/28
4              57.1  39.1  73.5   16/28       53.6  35.8  70.5   15/28
5              50.0  32.6  67.4   14/28       60.7  42.4  76.4   17/28
6              35.7  20.7  54.2   10/28       46.4  29.5  64.2   13/28
7              32.1  17.9  50.7    9/28       32.1  17.9  50.7    9/28
8              32.1  17.9  50.7    9/28       42.9  26.5  60.9   12/28
```

Accuracy by band (%):

```
band             K5  BeyondK5
model                        
LittleLearner  60.1      33.3
Unfiltered     58.3      40.5
```

Boundary drop (pp): {'LittleLearner': 26.8, 'Unfiltered': 17.9}

DiD: +8.9 pp  95% CI [-2.4, 20.8]

Accuracy by band and topic, LittleLearner (mean = accuracy, count = questions):

```
                            mean  count
band     topic                         
BeyondK5 earth science      0.67      6
         energy             0.33      3
         equations          0.00     12
         exponents          0.00      8
         forces             0.50      4
         geometry           0.00      4
         life science       0.62     13
         matter             0.50      6
         negative numbers   0.25     12
         percent            0.50      4
         probability        0.25      4
         roots              0.50      4
         space              0.50      2
         waves              0.50      2
K5       addition           0.44     16
         comparing numbers  0.50      4
         counting           1.00      4
         decimals           0.50      4
         division           0.50      4
         earth science      0.71     14
         energy             0.50      8
         exponents          0.00      4
         factors            0.75      4
         forces             0.33      6
         fractions          0.38      8
         geometry           0.50     16
         life science       0.95     22
         matter             1.00      9
         measurement        0.50      4
         multiplication     0.62      8
         place value        0.67     12
         space              0.67      6
         subtraction        0.00      8
         waves              0.71      7
```

Accuracy by band and topic, Unfiltered (mean = accuracy, count = questions):

```
                            mean  count
band     topic                         
BeyondK5 earth science      0.67      6
         energy             0.33      3
         equations          0.00     12
         exponents          0.00      8
         forces             0.75      4
         geometry           0.00      4
         life science       0.77     13
         matter             1.00      6
         negative numbers   0.25     12
         percent            0.50      4
         probability        0.00      4
         roots              0.75      4
         space              0.50      2
         waves              0.50      2
K5       addition           0.06     16
         comparing numbers  1.00      4
         counting           1.00      4
         decimals           0.75      4
         division           0.25      4
         earth science      0.79     14
         energy             0.62      8
         exponents          0.00      4
         factors            0.50      4
         forces             0.50      6
         fractions          0.25      8
         geometry           0.56     16
         life science       0.91     22
         matter             0.89      9
         measurement        0.75      4
         multiplication     0.62      8
         place value        0.42     12
         space              0.67      6
         subtraction        0.25      8
         waves              0.86      7
```

## 1.3b base models

Option-only baseline (accuracy with and without the question):

```
                        with question  option only  chance
model         band                                        
LittleLearner BeyondK5          0.393        0.298    0.25
              K5                0.577        0.196    0.25
Unfiltered    BeyondK5          0.464        0.262    0.25
              K5                0.673        0.202    0.25
```

Same, split by subject:

```
                                with question  option only
model         subject band                                
LittleLearner math    BeyondK5          0.146        0.188
                      K5                0.396        0.083
              science BeyondK5          0.722        0.444
                      K5                0.819        0.347
Unfiltered    math    BeyondK5          0.250        0.167
                      K5                0.573        0.083
              science BeyondK5          0.750        0.389
                      K5                0.806        0.361
```

Accuracy by grade (%, 95% Wilson CI lo/hi, correct/total):

```
model LittleLearner                     Unfiltered                    
                acc    lo    hi correct        acc    lo    hi correct
grade                                                                 
K              89.3  72.8  96.3   25/28       92.9  77.4  98.0   26/28
1              60.7  42.4  76.4   17/28       78.6  60.5  89.8   22/28
2              53.6  35.8  70.5   15/28       46.4  29.5  64.2   13/28
3              50.0  32.6  67.4   14/28       64.3  45.8  79.3   18/28
4              42.9  26.5  60.9   12/28       71.4  52.9  84.7   20/28
5              50.0  32.6  67.4   14/28       50.0  32.6  67.4   14/28
6              39.3  23.6  57.6   11/28       50.0  32.6  67.4   14/28
7              39.3  23.6  57.6   11/28       50.0  32.6  67.4   14/28
8              39.3  23.6  57.6   11/28       39.3  23.6  57.6   11/28
```

Accuracy by band (%):

```
band             K5  BeyondK5
model                        
LittleLearner  57.7      39.3
Unfiltered     67.3      46.4
```

Boundary drop (pp): {'LittleLearner': 18.5, 'Unfiltered': 20.8}

DiD: -2.4 pp  95% CI [-13.1, 8.3]

Accuracy by band and topic, LittleLearner (mean = accuracy, count = questions):

```
                            mean  count
band     topic                         
BeyondK5 earth science      1.00      6
         energy             0.33      3
         equations          0.00     12
         exponents          0.00      8
         forces             0.75      4
         geometry           0.00      4
         life science       0.62     13
         matter             1.00      6
         negative numbers   0.17     12
         percent            0.50      4
         probability        0.00      4
         roots              0.75      4
         space              0.50      2
         waves              0.50      2
K5       addition           0.44     16
         comparing numbers  0.75      4
         counting           1.00      4
         decimals           0.25      4
         division           0.25      4
         earth science      0.86     14
         energy             0.50      8
         exponents          0.00      4
         factors            0.25      4
         forces             0.67      6
         fractions          0.12      8
         geometry           0.44     16
         life science       0.95     22
         matter             0.89      9
         measurement        0.00      4
         multiplication     0.75      8
         place value        0.58     12
         space              1.00      6
         subtraction        0.00      8
         waves              0.57      7
```

Accuracy by band and topic, Unfiltered (mean = accuracy, count = questions):

```
                            mean  count
band     topic                         
BeyondK5 earth science      1.00      6
         energy             0.33      3
         equations          0.08     12
         exponents          0.12      8
         forces             0.75      4
         geometry           0.00      4
         life science       0.69     13
         matter             1.00      6
         negative numbers   0.50     12
         percent            0.50      4
         probability        0.00      4
         roots              0.50      4
         space              0.50      2
         waves              0.50      2
K5       addition           0.75     16
         comparing numbers  0.75      4
         counting           1.00      4
         decimals           0.25      4
         division           0.75      4
         earth science      0.93     14
         energy             0.62      8
         exponents          0.00      4
         factors            1.00      4
         forces             0.50      6
         fractions          0.38      8
         geometry           0.50     16
         life science       0.91     22
         matter             0.78      9
         measurement        0.00      4
         multiplication     1.00      8
         place value        0.42     12
         space              0.67      6
         subtraction        0.50      8
         waves              0.86      7
```

## 5b base models

Option-only baseline (accuracy with and without the question):

```
                        with question  option only  chance
model         band                                        
LittleLearner BeyondK5          0.488        0.286    0.25
              K5                0.774        0.202    0.25
Unfiltered    BeyondK5          0.571        0.250    0.25
              K5                0.738        0.220    0.25
```

Same, split by subject:

```
                                with question  option only
model         subject band                                
LittleLearner math    BeyondK5          0.292        0.188
                      K5                0.708        0.083
              science BeyondK5          0.750        0.417
                      K5                0.861        0.361
Unfiltered    math    BeyondK5          0.375        0.146
                      K5                0.656        0.125
              science BeyondK5          0.833        0.389
                      K5                0.847        0.347
```

Accuracy by grade (%, 95% Wilson CI lo/hi, correct/total):

```
model LittleLearner                     Unfiltered                    
                acc    lo    hi correct        acc    lo    hi correct
grade                                                                 
K              96.4  82.3  99.4   27/28       82.1  64.4  92.1   23/28
1              82.1  64.4  92.1   23/28       92.9  77.4  98.0   26/28
2              75.0  56.6  87.3   21/28       71.4  52.9  84.7   20/28
3              75.0  56.6  87.3   21/28       60.7  42.4  76.4   17/28
4              71.4  52.9  84.7   20/28       67.9  49.3  82.1   19/28
5              64.3  45.8  79.3   18/28       67.9  49.3  82.1   19/28
6              46.4  29.5  64.2   13/28       64.3  45.8  79.3   18/28
7              53.6  35.8  70.5   15/28       57.1  39.1  73.5   16/28
8              46.4  29.5  64.2   13/28       50.0  32.6  67.4   14/28
```

Accuracy by band (%):

```
band             K5  BeyondK5
model                        
LittleLearner  77.4      48.8
Unfiltered     73.8      57.1
```

Boundary drop (pp): {'LittleLearner': 28.6, 'Unfiltered': 16.7}

DiD: +11.9 pp  95% CI [0.6, 23.2]

Accuracy by band and topic, LittleLearner (mean = accuracy, count = questions):

```
                            mean  count
band     topic                         
BeyondK5 earth science      1.00      6
         energy             0.33      3
         equations          0.00     12
         exponents          0.00      8
         forces             0.75      4
         geometry           0.25      4
         life science       0.77     13
         matter             1.00      6
         negative numbers   0.42     12
         percent            1.00      4
         probability        0.00      4
         roots              1.00      4
         space              0.00      2
         waves              0.50      2
K5       addition           0.81     16
         comparing numbers  1.00      4
         counting           1.00      4
         decimals           0.75      4
         division           1.00      4
         earth science      0.93     14
         energy             0.62      8
         exponents          0.00      4
         factors            0.75      4
         forces             0.50      6
         fractions          0.88      8
         geometry           0.50     16
         life science       0.95     22
         matter             0.89      9
         measurement        0.25      4
         multiplication     0.88      8
         place value        0.83     12
         space              1.00      6
         subtraction        0.50      8
         waves              0.86      7
```

Accuracy by band and topic, Unfiltered (mean = accuracy, count = questions):

```
                            mean  count
band     topic                         
BeyondK5 earth science      0.83      6
         energy             0.67      3
         equations          0.25     12
         exponents          0.12      8
         forces             1.00      4
         geometry           0.00      4
         life science       0.85     13
         matter             1.00      6
         negative numbers   0.58     12
         percent            0.75      4
         probability        0.00      4
         roots              1.00      4
         space              0.50      2
         waves              0.50      2
K5       addition           0.81     16
         comparing numbers  0.25      4
         counting           1.00      4
         decimals           1.00      4
         division           0.50      4
         earth science      0.86     14
         energy             0.62      8
         exponents          0.00      4
         factors            0.75      4
         forces             0.67      6
         fractions          0.25      8
         geometry           0.69     16
         life science       0.91     22
         matter             0.89      9
         measurement        0.50      4
         multiplication     1.00      8
         place value        0.67     12
         space              1.00      6
         subtraction        0.62      8
         waves              0.86      7
```

## All sizes side by side

Boundary drop and DiD per size:

```
                         0.6b  1.3b    5b
drop LittleLearner (pp)  26.8  18.5  28.6
drop Unfiltered (pp)     17.9  20.8  16.7
DiD (pp)                  8.9  -2.4  11.9
CI low                   -2.4 -13.1   0.6
CI high                  20.8   8.3  23.2
```

K5 accuracy (%) per size:

```
                0.6b  1.3b    5b
model                           
LittleLearner   60.1  57.7  77.4
Unfiltered      58.3  67.3  73.8
Gap (Unf - LL)  -1.8   9.6  -3.6
```

BeyondK5 accuracy (%) per size:

```
                0.6b  1.3b    5b
model                           
LittleLearner   33.3  39.3  48.8
Unfiltered      40.5  46.4  57.1
Gap (Unf - LL)   7.2   7.1   8.3
```
