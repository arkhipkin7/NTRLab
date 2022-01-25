# Recommendation system
---
## Intro
- We need to develop a rec system for the Novosibirk medical library

## Test system
If you want to check the work go to the [link](https://recommendai.ntrlab.ru/)
- [items for test](https://github.com/arkhipkin7/NTRLab/blob/main/indicative_rec/data/books.csv);
- [users for test](https://github.com/arkhipkin7/NTRLab/blob/main/indicative_rec/data/users.csv).

## Models
For our datasets with implicit feedback, we used three models to compare the work
- [LightFM](https://making.lyst.com/lightfm/docs/lightfm.html) - [paper](https://arxiv.org/pdf/1507.08439.pdf)
- [Alternating Least Squares](https://implicit.readthedocs.io/en/latest/als.html) - [paper](http://yifanhu.net/PUB/cf.pdf)
- [Neural Collaborative Filtering](https://cornac.readthedocs.io/en/latest/models.html#module-cornac.models.ncf.recom_neumf) - [paper](https://arxiv.org/pdf/1708.05031.pdf)

## Metrics
In the evalution quality of the model we used **HiteRate@k**
- LightFM

|HiteRate@k | Val score | Test score|
|-----------|-----------|-----------|
|     1     |   0.02    |    0.02   |
|     5     |   0.13    |    0.13   |
|     10    |   0.27    |    0.23   |

- ALS

|HiteRate@k | Val score | Test score |
|-----------|-----------|------------|
|     1     |   0.04    |    0.03    |
|     5     |   0.12    |    0.09    |
|     10    |   0.19    |    0.16    |

- ALS

|HiteRate@k | Val score | Test score |
|-----------|-----------|------------|
|     1     |   0.15    |    0.14    |
|     5     |   0.33    |    0.33    |
|     10    |   0.43    |    0.44    |



## Future work
- [ ] Solve "the cold start" problem
