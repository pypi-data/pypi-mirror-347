# AGI Client

A Python client library for interacting with the General Reasoning platform API.

The documentation is available [here](https://gr.inc/docs).

## Installation

You can install the package using pip:

```bash
pip install agi
```

## Making API Calls

Obtain an API key from [the website](https://gr.inc). Then:

```python
import agi

client = agi.Client(api_key=YOUR_API_KEY)

# Download reasoning traces and verifications as a .jsonl
client.data.get(task='math-word-problems', model='DeepSeek-R1')
```

## Evaluating your reasoning model

The full evaluation guide is available [here](https://gr.inc/docs/evaluations). A boilerplate example is shown below:

```python
import agi
                
client = agi.Client("YOUR_API_KEY")
model = "USERNAME/MODEL_NAME"

# Retrieve test questions
data = client.evals.get(
    task='mathematical-brainteasers', 
    split='test'
)
question = data['questions']

# Submit model evaluations
for question in questions:
    reasoning_trace, answer = MyModel(
        system_prompt=question['system_prompt'],
        question=question['text']
    ) # Replace with your model logic
    client.evals.submit(
        id=question['id'],
        model=model,
        reasoning_trace=reasoning_trace,
        answer=answer
    )
```

## Running our verification and grading models

<!-- TODO: Add link to ther verifier and grader blogpost -->
Read more about our grader and verifier [here](https://gr.inc/)

```python
import agi 
 
client = agi.Client(api_key=YOUR_API_KEY)
 
response = client.verify.create(
  model="endeavour-preview",
  question="Are Dyson spheres feasible to build?",
  model_answer="Yes"
)
```

```python
import agi 
 
client = agi.Client(api_key=YOUR_API_KEY)
 
response = client.grade.create(
  model="endeavour-preview",
  question="Are Dyson spheres feasible to build?",
  model_answer="Yes",
  ground_truth_answer="No",
)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
