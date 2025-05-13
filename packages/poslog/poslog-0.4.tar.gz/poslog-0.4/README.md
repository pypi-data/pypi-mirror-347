# PosLog
A CRF-based Part-of-Speech (POS) Tagger for Log Messages.

## Usage
- **Use default model**  
    ```python
    from nlp import PrometeusTokenizer
    from nlp.pos import PosLogCRF

    tokenizer=PrometeusTokenizer()
    s="Tag this sentence."
    tokens=tokenizer.tokenize(s)
    # ['Tag', 'this', 'sentence', '.']

    pos_log=PosLogCRF()
    pos_log.predict(tokens)
    # ['VERB' 'DET' 'NOUN' 'PUNCT']
    ```
- **Train your own model**  
    Define model name in constructor:
    ```python
    pos_log=PosLogCRF(model_name="my_model")
    ```

    PosLog takes training data as tokens and tags separately:
    ```python
    train(X_train_tokens:list[list[str]], y_train_tags:list[list[str]])
    ```
    Or as token and tag pairs:
    ```python
    train_from_tagged_sents(tagged_sents:list[list[tuple[str,str]]])
    ```

    Note training will override existing model with the same name.

- **Use your own model**  
    Just call the constructor with the model name:
    ```python
    pos_log=PosLogCRF(model_name="my_model")
    ```

## Dependencies

PosLog relies on `nltk` corpora: `words`, `stopwords`, `wordnet`.