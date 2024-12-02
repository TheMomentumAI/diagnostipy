<a name="readme-top"></a>

<div align=center>
  <img src="https://cdn.prod.website-files.com/66a1237564b8afdc9767dd3d/66df7b326efdddf8c1af9dbb_Momentum%20Logo.svg" height="64">
</div>
<h1 align=center>Diagnostipy</h1>
<div align=center>
  <a href=mailto:hello@themomentum.ai?subject=Terraform%20Modules>
    <img src=https://img.shields.io/badge/Contact%20us-AFF476.svg alt="Contact us">
  </a>
    <a href="https://themomentum.ai">
    <img src=https://img.shields.io/badge/Check%20Momentum-1f6ff9.svg alt="Check">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-636f5a.svg?longCache=true" alt="MIT License">
  </a>
</div>
<br>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

---

<!-- ABOUT THE PROJECT -->
## About The Project

**Diagnostipy** is a open-source, Python library for rule-based diagnosis and evaluation. It allows users to define rules with conditions and weights, manage rulesets, and evaluate input data using customizable scoring and confidence functions.

### Features

- Define rules using `SymptomRule` with customizable conditions, weights, and criticality.
- Manage collections of rules via `SymptomRuleset`.
- Evaluate data using built-in or custom scoring and confidence functions with `Evaluator`.
- Flexible and extensible API.

### When Should I Use Diagnostipy?

- When **interpretability** is more important than accuracy, and you need a clear, rules-based system to explain decision-making
- If you lack access to large datasets for training machine learning models but still require a structured evaluation or diagnostic tool
- When collaborating with domain experts to formalize diagnostic or evaluation criteria without a data-driven approach
- When working in regulated industries or domains where decisions must be auditable and **transparent**
- For **quick prototyping** of logic-based systems without the overhead of complex data pipelines

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

- Python 3.10 or later

### Installation

Install Diagnostipy using pip:

```sh
pip install diagnostipy
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Define Rules

```python
from diagnostipy.core.models.symptom_rule import SymptomRule

rule_high_fever = SymptomRule(
    name="High Fever",
    weight=6.0,
    critical=True,
    apply_condition=lambda data: data.get("temperature", 0) >= 39,
)

rule_cough = SymptomRule(
    name="Persistent Cough",
    weight=4.0,
    critical=False,
    apply_condition=lambda data: data.get("cough", False),
)

rule_sore_throat = SymptomRule(
    name="Sore Throat",
    weight=5.0,
    critical=True,
    apply_condition=lambda data: data.get("sore_throat", False),
)
```

### Create Ruleset
```python
from diagnostipy import SymptomRuleset

ruleset = SymptomRuleset([rule_high_fever, rule_cough, rule_sore_throat])
```
### Evaluate data
```python
from diagnostipy import Evaluator

data = {
    "temperature": 39.5,
    "cough": True,
    "sore_throat": False,
}

evaluator = Evaluator(ruleset)
results = evaluator.run(data=data)

print(results)
```

```plaintext
total_score=10.0 label='High' confidence=0.8333333333333334 metadata=None
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap
- [ ] Add support for more built-in confidence functions.
- [ ] Improve error handling.
- [ ] Expand the API to include more user-friendly options.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

We are open to, and grateful for, any contributions made by the community.

A huge thank you to all the contributors.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/some-feature`)
3. Commit your Changes (`git commit -m 'Add some feature'`)
4. Push to the Branch (`git push origin feature/some-feature`)
5. Open a Pull Request

### Top contributors:

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

**Diagnostipy** is distributed under the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
