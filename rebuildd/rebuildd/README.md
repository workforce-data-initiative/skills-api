This is the main REBUILDD Python module.

Example of usage:
```
from rebuildd import utill
utill.test()
```


### matcher.py 
Contains functions for creating text classification using Spark

* `make_info(ngrams, stemming, weighting)`
* `read_info(model_path, ngrams_, stemming_, weighting_)`
* `get_tokens(text)` Returns tokens from text
* `stem_tokens(tokens, stemmer)` Stemmin list of tokens and return string
* `stem_corpus(corpus, stemmer)` Stemming the complete corpus
* `save_classifier(classifier, vectorizer, transformer, info,  name)` Save scikit learn classifier
* `save_classifier_mllib(classifier,  name)` Save mllib classifier
* `map_classes(mapper_file, in_class)` Map input class to corresponding class based on mapping file
* `tokenize(text)` Tokenizing text with stemming, converting tokens to lowercase and removing punctuation
* `onet_classification_spark()` Building text classifier using spark and mllib
* `onet_classification_spark_scikit()` Building text classification model using scikit learn and spark

### matcher_nsp.py
Text classification functions without using Spark

* `Config(object)` Defining configuration class
* `read_from_csv(config)`
* `read_from_db(config, sqlstring)`
* `get_tokens(sentence)`
* `stem_tokens(tokens, stemmer)`
* `stem_corpus(corpus, stemmer)`
* `save_classifier(classifier, vectorizer, transformer, config,name)`
* `multi_fit(clf)`
* `classify(path, text)`
* `classify_loaded(clf, vectorizer, text)`
* build_classifier(config)

### lodes.py
Contains industry composition clustering, nowcasting and transition matrix.

### rake.py
Keyword extraction using Rake.

### utill.py
Utility functions
