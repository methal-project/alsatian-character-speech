#### tasks
- fix the bug (inversed columns) in files like mots_als_ELAL.csv etc.
- recalculate correlations
- re-produce the coefficients of FEEL according to NRC_intensif, get heating maps
	Feel_fr VS Elal_als
	Feel_NRC_fr VS Elal_als

- check library: https://github.com/Priya22/EmotionDynamics
- read essai: https://seafile.unistra.fr/smart-link/b950c501-f30b-41c1-9add-4037152502a8/

#### En semaine 3 pourquoi Correlation bizarre
- colonnes des émotions inversées
- Id_block décalé
```shell
      valence   valence     
278  0.471034  0.743000
279  0.702278  0.803200
280  0.758477  0.572545
281  0.634455  0.449667
282  0.427335  0.894500
283       NaN  0.073000
284       NaN  0.590750
285       NaN  0.638667
286       NaN  0.658600
287       NaN  0.219000
288       NaN  0.745400  

     Id_block  Id_block
278     288.0       283
279     289.0       284
281     291.0       286
282     292.0       287
283       NaN       288     # c'est car dans certains bloc, y'a pas de mot-clé, donc
284       NaN       289     # pas de moyenne, ça a beaucoup diminué la correlation
285       NaN       290
286       NaN       291
287       NaN       292
```
- FEEL on binaire mais ELAL non
- les mots-clés parcourus sont différents
- certains mots français sont dans le texte Alsacien

#### merge de NRC-intensif et FEEL
1. calculer coefficients moyennes dans chaque catégorie
2. Si dans NRC, coef >= moyenne, alors dans FEEL, coef devient 1, sinon, garde les coeffs de FEEL
3. comparer correlation avec celle de FEEL pure
	correlation de FEEL+NRC-intensif est un peu plus haut que celle de FEEL pure

#### ted librairie
texte de sample réussi, mais avec des bugs dans numpy

```shell

python3 avgEmoValues.py --dataPath sample.csv --lexPath NRC-VAD-Lexico
n.csv --lexNames valence dominance --savePath sample_outputs
C:\Users\mocki\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-pa
ckages\numpy\core\fromnumeric.py:3440: RuntimeWarning: Mean of empty slice.
  return _methods._mean(a, axis=axis, dtype=dtype,
C:\Users\mocki\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-pa
ckages\numpy\core\_methods.py:189: RuntimeWarning: invalid value encountered in double_scalars
  ret = ret.dtype.type(ret / rcount)
C:\Users\mocki\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-pa
ckages\numpy\core\fromnumeric.py:3440: RuntimeWarning: Mean of empty slice.
  return _methods._mean(a, axis=axis, dtype=dtype,
C:\Users\mocki\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-pa
ckages\numpy\core\_methods.py:189: RuntimeWarning: invalid value encountered in double_scalars
  ret = ret.dtype.type(ret / rcount)

texte de sample_fr réussi sans erreurs
```
