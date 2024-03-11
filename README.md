# An implementation of the k-Tail algorithm

This repository includes lab materials for **COM3523/6523 Software Reengineering** at the **University of Sheffield**.

Specifically, the repository contains the followings:
- `/.github/workflows`: GitHub Actions workflow.
- `/data`: example trace data.
- `/tests`: test cases.
- `finite_state_automaton.py`: a class implementing a simple nondeterministic finite automaton with helper methods (e.g., `is_accepted()`).
- `ktail.py`: an implmentation of the k-tail algorithm[^1].
- `makefile`: a makefile defining frequently used commands (i.e., install, clean, linter, test).
- `model_inference_exercise.ipynb`: a Jupyter notebook demonstrating the application of the k-tail algorithm.
- `requirements.txt`: a list of required libraries.

[^1]: The k-tail algorithm implementation is based on the algorithm described in the following paper: 
Busany N, Maoz S, Yulazari Y. Size and accuracy in model inference. In2019 34th IEEE/ACM International Conference on Automated Software Engineering (ASE) 2019 Nov 11 (pp. 887-898). IEEE.

## Install

In your working python (virtual) environment,
```bash
make install
```

Otherwise, you can install the libraries in `requirements.txt` manually.

## Test

In your terminal (where your python interpreter is loaded):
```bash
make test
```

Otherwise, you can run the tests in `tests` manually (e.g., `pytest -v`).

## Run

Simply run `ktail.py` or `model_inference_exercise.ipynb` with your beloved IDE (e.g., PyCharm) or terminal.

For example, run `ktail.py` will execute the following code:
```python
if __name__ == '__main__':
    k = 2
    words = [
        'a b',
        'a b b',
        'a b b b'
    ]
    m = ktail(words=words, k=k, sep=' ', print_internals=False)
    m.draw(f'{k}-tail-result')
```

As a result, it will infer a model from a set of traces T={ab, abb, abbb} and return the model as follows:
<img width="700" alt="image" src="https://github.com/donghwan-shin/ktail/assets/12538465/a4fee708-7286-41d0-a43b-33b254d28958">

Note that $ and # are special symbols for the transitions with initial and final states. 


## Author

Donghwan Shin (https://dshin.info)

## License

Educational Community License, Version 2.0 (see [LICENSE](LICENSE) for more details)
