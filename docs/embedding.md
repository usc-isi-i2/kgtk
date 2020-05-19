Computes embeddings of nodes using properties of nodes. The values are concatenated into sentences defined by a template, and embedded using a pre-trained language model.

The following language models are supported:
- bert-base-nli-cls-token
- bert-base-nli-max-tokens
- bert-base-nli-mean-tokens
- bert-base-nli-stsb-mean-tokens
- bert-base-wikipedia-sections-mean-tokens
- bert-large-nli-cls-token
- bert-large-nli-max-tokens
- bert-large-nli-mean-tokens
- bert-large-nli-stsb-mean-tokens
- distilbert-base-nli-mean-tokens
- distilbert-base-nli-stsb-mean-tokens
- distiluse-base-multilingual-cased
- roberta-base-nli-mean-tokens
- roberta-base-nli-stsb-mean-tokens
- roberta-large-nli-mean-tokens
- roberta-large-nli-stsb-mean-tokens

The output is an edge file where each node appears once; a user defined property is used to store the embedding, and the value is a string containing the embedding. For example:

To generate the embeddings, the command first generates a sentence for each node using the properties listed in the label-properties, description-properties, isa-properties and has-properties options. Each sentence is generated using the following template:

```
{label-properties}, {description-properties} is a {isa-properties}, and has {has-properties}
```

An example sentence is “Saint David, patron saint of Wales is a human, Catholic priest, Catholic bishop, and has date of death, religion and canonization status”

```
subject        predicate        object
Q1        text_embedding    “0.222, 0.333, ..”
Q2        text_embedding    “0.444, 0.555, ..”
```

## Usage:
```
kgtk text_embedding OPTIONS
```
### Options:
```
--model { string }: one of the models listed above.
--label-properties {p1, p2, …}: an ordered list of properties. The output is the value of the first property that returns a non-empty value.
--description-properties {p1, p2, …}: an ordered list of properties. The output is the value of the first property that returns a non-empty value.
--isa-properties {p1, p2, ..}: an ordered list of properties. When a property contains multiple values, select values randomly up to a certain limit. When a property value is not a literal, output the label of the property value. When multiple isa-properties are present, the values are output comma-separated.
--has-properties {p1, p2, …}: an ordered list of properties. The output consists of a comma-separated text with the labels of the properties, using and for the last item, e.g., “country, place of birth, religion and canonization status”
--output-property {p}: the property used to record the embedding. Default: text_embedding.
--embedding-projector-metatada {p1, p2, …}: list of properties used to construct a metadata file for use in the Google Embedding Projector: http://projector.tensorflow.org. Default: the same properties used in the --property option.
--embedding-projector-metadata-path {file}: output path for saving the metadata file for the Google Embedding Projector. Default: ~\embedding-metadata.txt
```

## Assumptions
The input is an edge file sorted by subject.

## Examples
```
Kgtk text_embedding \ 
            --input input_file.csv \
--model bert-base-wikipedia-sections-mean-tokens \
--property-value label, description \
--output-property bert_embedding \
--embedding-projector-metadada subject, label, description \
--embedding-projector-metadata-path ~/Documents/blah-blah.txt 
```

```
Q31    label    “somalia”
Q31    P31    Q233454
Q31    description    “country in africa”
```
```
Q31 bert_embedding “0.22, 0.56”
```