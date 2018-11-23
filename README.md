# bert-as-service

[![Python: 3.6](https://img.shields.io/badge/Python-3.6-brightgreen.svg)](https://opensource.org/licenses/MIT)    [![Tensorflow: 1.10](https://img.shields.io/badge/Tensorflow-1.10-brightgreen.svg)](https://opensource.org/licenses/MIT)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Using BERT model as a sentence encoding service, i.e. mapping a variable-length sentence to a fixed-length vector.

<img src=".github/demo.gif" width="600">

Author: Han Xiao [https://hanxiao.github.io](https://hanxiao.github.io)

[BERT code of this repo](bert/) is forked from the [original BERT repo]((https://github.com/google-research/bert)) with necessary modification, [especially in extract_features.py](bert/extract_features.py).


* [Highlights](#highlights)
* [What is it](#what-is-it)
* [Requirements](#requirements)
* [Usage](#usage)
* [FAQ on Technical Details](#faq-on-technical-details)
* [Benchmark](#benchmark)

## What is it

**BERT**: [Developed by Google](https://github.com/google-research/bert), BERT is a method of pre-training language representations. It leverages an enormous amount of plain text data publicly available on the web and is trained in an unsupervised manner. Pre-training a BERT model is a fairly expensive yet one-time procedure for each language. Fortunately, Google released several pre-trained models where [you can download from here](https://github.com/google-research/bert#pre-trained-models).


**Sentence Encoding/Embedding**: sentence encoding is a upstream task required in many NLP applications, e.g. sentiment analysis, text classification. The goal is to represent a variable length sentence into a fixed length vector, e.g. `hello world` to `[0.1, 0.3, 0.9]`. Each element of the vector should "encode" some semantics of the original sentence.

**Finally, this repo**: This repo uses BERT as the sentence encoder and hosts it as a service via ZeroMQ, allowing you to map sentences into fixed-length representations in just two lines of code. 

## Highlights

- :telescope: **State-of-the-art**: build on pretrained 12/24-layer BERT models released by Google AI, which is considered as a milestone in the NLP community.
- :hatching_chick: **Easy-to-use**: require only two lines of code to get sentence encodes.
- :zap: **Fast**: 780 sentences/s on a single Tesla M40 24GB when `max_seq_len=20`. See [benchmark](#Benchmark).
- :octopus: **Concurrency**: scale nicely and smoothly on multiple GPUs and multiple clients. See [benchmark](#speed-wrt-num_client).

## Requirements

- Python >= 3.5 (Python 2 is NOT supported!)
- Tensorflow >= 1.10

These two requirements MUST be satisfied. For other dependent packages, please refer to `requirments.txt`  and `requirments.client.txt`.

:point_up: Python 2 is supported on the client side [for the following consideration](#q-can-i-run-it-in-python-2).

## Usage

#### 1. Download a Pre-trained BERT Model
Download a model from [here](https://github.com/google-research/bert#pre-trained-models), then uncompress the zip file into some folder, say `/tmp/english_L-12_H-768_A-12/`

You can use all models listed, including `BERT-Base, Multilingual` and `BERT-Base, Chinese`.


#### 2. Start a BERT service
```bash
python app.py -model_dir /tmp/english_L-12_H-768_A-12/ -num_worker=4 
```
This will start a service with four workers, meaning that it can handle up to four **concurrent** requests. More concurrent requests will be queued in a load balancer. Details can be found in our [FAQ](#q-what-is-the-parallel-processing-model-behind-the-scene) and [the benchmark on number of clients](#speed-wrt-num_client)

#### 3. Use Client to Get Sentence Encodes
> :children_crossing: NOTE: please make sure your project includes [`client.py`](service/client.py), as we need to import `BertClient` class from this file. This is the **only file** that you will need as a client. You don't even need Tensorflow on client.

Now you can use pretrained BERT to encode sentences in your Python code simply as follows:
```python
from service.client import BertClient
bc = BertClient()
bc.encode(['First do it', 'then do it right', 'then do it better'])
```
This will return a `ndarray`, in which each row is the fixed representation of a sentence. You can also let it return a pure python object in the type of `List[List[float]]`.

### Using BERT Service Remotely
One can also start the service on one (GPU) machine and call it from another (CPU) machine as follows

```python
# on another CPU machine
from service.client import BertClient
bc = BertClient(ip='xx.xx.xx.xx', port=5555)  # ip address of the GPU machine
bc.encode(['First do it', 'then do it right', 'then do it better'])
```
<<<<<<< HEAD

> :children_crossing: NOTE: please make sure your project includes [`client.py`](service/client.py), as we need to import `BertClient` class from this file. Again, this is the **only file** that you need as a client. You don't even need Tensorflow. Please refer to [`requirements.client.txt`](requirements.client.txt) for the dependency on the client side.
 
### Run BERT Service on Nvidia Docker
```bash
docker build -t bert-as-service -f ./docker/Dockerfile .
NUM_WORKER=1
PATH_MODEL=<path of your model>
docker run --runtime nvidia -dit -p 5555:5555 -v $PATH_MODEL:/model -t bert-as-service $NUM_WORKER
=======
cd src
bash prepro.sh
>>>>>>> 914cd2839f54469eb9f45512ebdb2bf566c4dd9b
```

## Server and Client Configurations

### Server-side configs

Server-side configs are summarized below, which can be found in [`app.py`](app.py) as well.

| Argument | Type | Default | Description |
|--------------------|------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `model_dir` | str |  | folder path of the pre-trained BERT model. |
| `max_seq_len` | int | `25` | maximum length of sequence, longer sequence will be trimmed on the right side. |
| `num_worker` | int | `1` | number of (GPU/CPU) worker runs BERT model, each works in a separate process. |
| `max_batch_size` | int | `256` | maximum number of sequences handled by each worker, larger batch will be partitioned into small batches. |
| `port` | int | `5555` | port for client-server communication. |
| `pooling_strategy` | str | `REDUCE_MEAN` | the pooling strategy for generating encoding vectors, valid values are `NONE`, `REDUCE_MEAN`, `REDUCE_MAX`, `REDUCE_MEAN_MAX`, `CLS_TOKEN`, `FIRST_TOKEN`, `SEP_TOKEN`, `LAST_TOKEN`. Explanation of these strategies [can be found here](#q-what-are-the-available-pooling-strategies). To get encoding for each token in the sequence, please set this to `NONE`.|
| `pooling_layer` | int | `-2` | the encoding layer that pooling operates on, where `-1` means the last layer, `-2` means the second-to-last, etc.|

### Client-side configs

Client-side configs are summarized below, which can be found in [`client.py`](service/client.py) as well.
 
| Argument | Type | Default | Description |
|----------------------|------|-----------|-------------------------------------------------------------------------------|
| `ip` | str | `localhost` | IP address of the server |
| `port` | int | `5555` | port of the server |
| `output_fmt` | str | `ndarray` | the output format of the sentence encodes, either in numpy array or python List[List[float]] (`ndarray`/`list`) |
| `show_server_config` | bool | `True` | whether to show server configs when first connected |


## FAQ on Technical Details

##### **Q:** How large is a sentence vector?

Each sentence is translated to a 768-dimensional vector. One exception is `REDUCE_MEAN_MAX` pooling strategy, which translates a sentence into a 1536-dimensional vector.

##### **Q:** How do you get the fixed representation? Did you do pooling or something?

**A:** Yes, pooling is required to get a fixed representation of a sentence. In the default strategy `REDUCE_MEAN`, I take the second-to-last hidden layer of all of the tokens in the sentence and do average pooling.

##### **Q:** What are the available pooling strategies?

**A:** Here is a table summarizes all pooling strategies I implemented. Choose your favorite one by specifying `python app.py -pooling_strategy`

|Strategy|Description|
|---|---|
| `NONE` | no pooling at all, useful when you want to use word embedding instead of sentence embedding. This will results in a `[max_seq_len, 768]` encode matrix for a sequence.|
| `REDUCE_MEAN` | take the average of the hidden state of encoding layer on the time axis |
| `REDUCE_MAX` | take the maximum of the hidden state of encoding layer on the time axis |
| `REDUCE_MEAN_MAX` | do `REDUCE_MEAN` and `REDUCE_MAX` separately and then concat them together on the last axis, resulting in 1536-dim sentence encodes |
| `CLS_TOKEN` or `FIRST_TOKEN` | get the hidden state corresponding to `[CLS]`, i.e. the first token |
| `SEP_TOKEN` or `LAST_TOKEN` | get the hidden state corresponding to `[SEP]`, i.e. the last token |

##### **Q:** Why not use the hidden state of the first token as default strategy, i.e. the `[CLS]`?

**A:** Because a pre-trained model is not fine-tuned on any downstream tasks yet. In this case, the hidden state of `[CLS]` is not a good sentence representation. If later you fine-tune the model, you may use `[CLS]` as well.

##### **Q:** BERT has 12/24 layers, so which layer are you talking about?

**A:** By default this service works on the second last layer, i.e. `pooling_layer=-2`. You can change it by setting `pooling_layer` to other negative values, e.g. -1 corresponds to the last layer.

##### **Q:** Why not the last hidden layer? Why second-to-last?

**A:** The last layer is too closed to the target functions (i.e. masked language model and next sentence prediction) during pre-training, therefore may be biased to those targets. If you question about this argument and want to use the last hidden layer anyway, please feel free to set `pooling_layer=-1`.

##### **Q:** Could I use other pooling techniques?

**A:** For sure. Just follows [`get_sentence_encoding()` I added to the modeling.py](bert/extract_features.py#L96). Note that, if you introduce new `tf.variables` to the graph, then you need to train those variables before using the model. You may also want to check [some pooling techniques I mentioned in my blog post](https://hanxiao.github.io/2018/06/24/4-Encoding-Blocks-You-Need-to-Know-Besides-LSTM-RNN-in-Tensorflow/#pooling-block).

##### **Q:** Can I start multiple clients and send requests to one server simultaneously?

**A:** Yes! That's the purpose of this repo. In fact you can start as many clients as you want. One server can handle all of them (given enough time).

##### **Q:** How many requests can one service handle concurrently?

**A:** The maximum number of concurrent requests is determined by `num_worker` in `app.py`. If you a sending more than `num_worker` requests concurrently, the new requests will be temporally stored in a queue until a free worker becomes available.

##### **Q:** So one request means one sentence?

**A:** No. One request means a list of sentences sent from a client. Think the size of a request as the batch size. A request may contain 256, 512 or 1024 sentences. The optimal size of a request is often determined empirically. One large request can certainly improve the GPU utilization, yet it also increases the overhead of transmission. You may run `python client_example.py` for a simple benchmark.

##### **Q:** How about the speed? Is it fast enough for production?

**A:** It highly depends on the `max_seq_len` and the size of a request. On a single Tesla M40 24GB with `max_seq_len=40`, you should get about 780 samples per second using a 12-layer BERT. In general, I'd suggest smaller `max_seq_len` (25) and larger request size (512/1024).

##### **Q:** Did you benchmark the efficiency?

**A:** Yes. See [Benchmark](#Benchmark).

To reproduce the results, please run [`python benchmark.py`](benchmark.py).

##### **Q:** What is backend based on?

**A:** [ZeroMQ](http://zeromq.org/).

##### **Q:** What is the parallel processing model behind the scene?

<img src=".github/bert-parallel-pipeline.png" width="600">

##### **Q:** Do I need Tensorflow on the client side?

**A:** No. Think of `BertClient` as a general feature extractor, whose output can be fed to *any* ML models, e.g. `scikit-learn`, `pytorch`, `tensorflow`. The only file that client need is [`client.py`](service/client.py). Copy this file to your project and import it, then you are ready to go.

##### **Q:** Can I use multilingual BERT model provided by Google?

**A:** Yes.

#####  **Q:** Can I use my own fine-tuned BERT model?

**A:** Yes. Make sure you have the following three items in `model_dir`:
                             
- A TensorFlow checkpoint (`bert_model.ckpt`) containing the pre-trained weights (which is actually 3 files).
- A vocab file (`vocab.txt`) to map WordPiece to word id.
- A config file (`bert_config.json`) which specifies the hyperparameters of the model.

##### **Q:** Can I run it in python 2?

**A:** Server side no, client side yes. This is based on the consideration that python 2.x might still be a major piece in some tech stack. Migrating the whole downstream stack to python 3 for supporting `bert-as-service` can take quite some effort. On the other hand, setting up `BertServer` is just a one-time thing, which can be even [run in a docker container](#run-bert-service-on-nvidia-docker). To ease the integration, we support python 2 on the client side so that you can directly use `BertClient` as a part of your python 2 project, whereas the server side should always be hosted with python 3.

##### **Q:** How can I get word embedding instead of sentence embedding?

**A:** To get word embedding please set `pooling_strategy = NONE`. This will omit the pooling operation on the encoding layer, resulting in a `[max_seq_len, 768]` matrix for every sequence. To get the word embedding corresponds to every token, you can simply use slice index.

> :children_crossing: NOTE: no matter how long your original sequence is, the service will always return a `[max_seq_len, 768]` matrix for every sequence. Beware of the special tokens padded to the sequence, e.g. `[CLS]`, `[SEP]`, `0_PAD`, when getting the word embedding.

Example:
```python
# max_seq_len = 25
# pooling_strategy = NONE

bc = BertClient()
x = ['hey you', 'whats up']

bc.encode(x)  # [2, 25, 768]
bc.encode(x)[0]  # [1, 25, 768], word embeddings for `hey you`
bc.encode(x)[0][0]  # [1, 1, 768], word embedding for `[CLS]`
bc.encode(x)[0][1]  # [1, 1, 768], word embedding for `h`
bc.encode(x)[0][8]  # [1, 1, 768], word embedding for `[SEP]`
bc.encode(x)[0][9]  # [1, 1, 768], word embedding for `0_PAD`, meaningless
bc.encode(x)[0][25]  # error, out of index!
```

##### **Q:** I encounter `zmq.error.ZMQError: Operation cannot be accomplished in current state` when using `BertClient`, what should I do?

**A:** This is often due to the misuse of `BertClient` in multi-thread/process environment. Note that you can’t reuse one `BertClient` among multiple threads/processes, you have to make a separate instance for each thread/process. For example, the following won't work at all:

```python
# BAD example
bc = BertClient()

# in Proc1/Thread1 scope:
bc.encode(lst_str)

# in Proc2/Thread2 scope:
bc.encode(lst_str)
```

Instead, please do:

```python
# in Proc1/Thread1 scope:
bc1 = BertClient()
bc1.encode(lst_str)

# in Proc2/Thread2 scope:
bc2 = BertClient()
bc2.encode(lst_str)
```


## Benchmark

The primary goal of benchmarking is to test the scalability and the speed of this service, which is crucial for using it in a dev/prod environment. Benchmark was done on Tesla M40 24GB, experiments were repeated 10 times and the average value is reported.

To reproduce the results, please run
```bash
python benchmark.py
```

Common arguments across all experiments are:

| Parameter         | Value |
|-------------------|-------|
| num_worker        | 1,2,4 |
| max_seq_len       | 40    |
| client_batch_size | 2048  |
| max_batch_size    | 256   |
| num_client        | 1     |

#### Speed wrt. `max_seq_len`

`max_seq_len` is a parameter on the server side, which controls the maximum length of a sequence that a BERT model can handle. Sequences larger than `max_seq_len` will be truncated on the left side. Thus, if your client want to send long sequences to the model, please make sure the server can handle them correctly.

Performance-wise, longer sequences means slower speed and  more chance of OOM, as the multi-head self-attention (the core unit of BERT) needs to do dot products and matrix multiplications between every two symbols in the sequence.

<img src=".github/max_seq_len.png" width="600">

| max_seq_len | 1 GPU | 2 GPU | 4 GPU |
|-------------|-------|-------|-------|
| 20          | 787   | 1551  | 3026  |
| 40          | 381   | 760   | 1502  |
| 80          | 156   | 313   | 621   |
| 160         | 112   | 224   | 448   |
| 320         | 51    | 102   | 205   |


#### Speed wrt. `client_batch_size`

`client_batch_size` is the number of sequences from a client when invoking `encode()`. For performance reason, please consider encoding sequences in batch rather than encoding them one by one. 

For example, do:
```python
# prepare your sent in advance
bc = BertClient()
my_sentences = [s for s in my_corpus.iter()]
# doing encoding in one-shot
vec = bc.encode(my_sentences)
```

DON'T:
```python
bc = BertClient()
vec = []
for s in my_corpus.iter():
    vec.append(bc.encode(s))
```

It's even worse if you put `BertClient()` inside the loop. Don't do that.

<img src=".github/client_batch_size.png" width="600">

| client_batch_size | 1 GPU | 2 GPU | 4 GPU |
|-------------------|-------|-------|-------|
| 1                 | 33    | 74    | 73    |
| 4                 | 207   | 203   | 199   |
| 8                 | 275   | 275   | 267   |
| 16                | 334   | 333   | 330   |
| 64                | 365   | 363   | 366   |
| 256               | 383   | 382   | 383   |
| 512               | 377   | 768   | 767   |
| 1024              | 378   | 753   | 1525  |
| 2048              | 380   | 758   | 1495  |
| 4096              | 381   | 762   | 1511  |



#### Speed wrt. `num_client`
`num_client` represents the number of concurrent clients connected to the server at the same time.

<img src=".github/num_clients.png" width="600">

| num_client | 1 GPU | 2 GPU | 4 GPU |
|------------|-------|-------|-------|
| 1          | 381   | 758   | 1522  |
| 2          | 201   | 402   | 802   |
| 4          | 103   | 207   | 413   |
| 8          | 52    | 105   | 210   |
| 16         | 26    | 53    | 105   |
| 32         | 13    | 26    | 53    |

As one can observe, 1 clients 1 GPU = 381 seqs/s, 2 clients 2 GPU 402 seqs/s, 4 clients 4 GPU 413 seqs/s. This shows the efficiency of our parallel pipeline and job scheduling, as the service can leverage the GPU time  more exhaustively as concurrent requests increase.


#### Speed wrt. `max_batch_size`

`max_batch_size` is a parameter on the server side, which controls the maximum number of samples per batch per worker. If a incoming batch from client is larger than `max_batch_size`, the server will split it into small batches so that each of them is less or equal than `max_batch_size` before sending it to workers.

<img src=".github/max_batch_size.png" width="600">

| max_batch_size | 1 GPU | 2 GPU | 4 GPU |
|----------------|-------|-------|-------|
| 32             | 357   | 717   | 1409  |
| 64             | 364   | 733   | 1460  |
| 128            | 378   | 759   | 1512  |
| 256            | 381   | 758   | 1497  |
| 512            | 381   | 762   | 1500  |

<<<<<<< HEAD
=======
```
>>>>>>> 914cd2839f54469eb9f45512ebdb2bf566c4dd9b
