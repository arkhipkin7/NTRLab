# Recommendation system
---
## Intro
- We need to develop a rec system for the Novosibirsk medical library

## Test system
If you want to check the work go to the [link](https://recommendai.ntrlab.ru/)
- [items for test](https://github.com/arkhipkin7/NTRLab/blob/main/indicative_rec/data/books.csv);
- [users for test](https://github.com/arkhipkin7/NTRLab/blob/main/indicative_rec/data/users.csv).

## Models
For our datasets with implicit feedback, we used four models to compare the work
- [LightFM](https://making.lyst.com/lightfm/docs/lightfm.html) - [paper](https://arxiv.org/pdf/1507.08439.pdf)
- [Alternating Least Squares](https://implicit.readthedocs.io/en/latest/als.html) - [paper](http://yifanhu.net/PUB/cf.pdf)
- [Neural Collaborative Filtering](https://cornac.readthedocs.io/en/latest/models.html#module-cornac.models.ncf.recom_neumf) - [paper](https://arxiv.org/pdf/1708.05031.pdf)
- Clustering of Kmeans on [FastText](https://fasttext.cc/docs/en/python-module.html) embeddings - [papaer](https://arxiv.org/pdf/1607.04606.pdf)

## Metrics
In the evalution quality of the model we used **HiteRate@k**

|Model | HitRate@10 | MAP@1 | MAP@5 | MAP@10|
|-------|------------|-------|-------|-------|
|ALS|0.01|0|0.0005|0.005|
|Kmeans+FT|0.374|0.121|0.178|0.19|
|LightFM| 0.116|0.0004|0.0006|0.0009|
|NueFM|0.28|0.04|0.088|0.103|

## Future work
- [ ] Solve "the cold start" problem
