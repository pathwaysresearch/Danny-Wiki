---
type: synthesized
aliases: ["Three Pillars of Data Science", "Data Science First Principles"]
tags: ["data-science", "methodology", "framework", "first-principles"]
relationships:
  - target: data-science
    type: extends
  - target: data-analytic-thinking
    type: extends
  - target: data-science-for-business
    type: extends
  - target: expected-value-framework
    type: extends
---

# Data Science: Three-Pillar Framework

# Data Science: Three-Pillar Framework

Two dominant pedagogical traditions in data science — Joel Grus's *Data Science from Scratch* (technical, bottom-up) and Foster Provost's *Data Science for Business* (decision-oriented, top-down) — are best understood as complementary rather than competing. Together they define three foundational pillars that any practitioner must develop.

## The Three Pillars

### 1. Hacking Skills (Grus)
The ability to write code that acquires, cleans, transforms, and models data. Grus insists on building these from scratch — implementing gradient descent, naive Bayes, and neural networks by hand in Python — so that practitioners understand *why* tools behave as they do rather than treating libraries as black boxes. First-principles coding is not inefficiency; it is the foundation that makes debugging, customization, and genuine understanding possible.

### 2. Mathematics and Statistics
The formal language underlying every model. Key areas include:
- **Probability theory**: the grammar of uncertainty
- **Linear algebra**: the machinery of high-dimensional data transformations
- **Statistics**: inference, distributions, hypothesis testing, and the quantification of confidence

Without this pillar, a practitioner can run models but cannot diagnose when they are wrong or reason about their limits.

### 3. Data-Analytic Thinking (Provost)
The capacity to *frame* business problems as data problems and to *connect* model outputs to decisions. This is Provost's central contribution: predictive modeling is not an end in itself but an input to a decision. The practitioner must ask:
- What decision is being made?
- What would change if the model output were different?
- What is the expected value of acting on this prediction?

Provost's canonical example is Jasmin evaluating LendingClub loans: accuracy alone is insufficient — she must reason about expected investment return, base rates, and the costs of false positives versus false negatives.

## Why Both Traditions Are Necessary

| Dimension | Grus (Hacking + Math) | Provost (Analytic Thinking) |
|---|---|---|
| Starting point | The algorithm | The decision |
| Core question | How does this work? | What should we do? |
| Risk if missing | Cargo-cult modeling | Technically correct but useless models |
| Core text | *Data Science from Scratch* | *Data Science for Business* |

Neither pillar is sufficient alone. A practitioner fluent in code and mathematics but untrained in decision framing will optimize the wrong objective. A practitioner with strong business intuition but no technical grounding cannot detect leakage, evaluate model validity, or implement solutions.

## The Integration Point: Expected Value

The [[expected-value-framework|Expected Value Framework]] is where the three pillars converge. It requires:
- **Hacking skills** to implement a calibrated probability model
- **Mathematics and statistics** to reason about distributions and cost matrices
- **Data-analytic thinking** to map model outputs onto the actual decision with its real costs and benefits

Provost's framing is deliberate: "the framework's so simple it's like why doesn't everybody use this." The reason most practitioners do not is that they treat pillar 1 and pillar 2 as the destination, never arriving at pillar 3.

## Practical First-Principles Sequence

1. **Frame the decision first.** Name the person making it (Provost's persona-driven decomposition), their objective, and what action they will take with the model's output.
2. **Understand the data's provenance.** Where did it come from? At what time point? This is the foundation of leakage detection — one of the most consequential diagnostic disciplines in applied data science.
3. **Build or re-derive the algorithm from scratch at least once.** Even if you will use a library in production, implement the core logic manually to understand its assumptions.
4. **Evaluate against the decision, not just the model.** Accuracy, AUC, and F1 are proxies. The real criterion is expected value in the deployment context.
5. **Ask the causal question.** Is the model being used for prediction or for intervention? These require different data and different validation strategies — conflating them is the non-causal targeting paradox Provost and Fernández-Loría formalized in 2022.

## Key Concepts in This Framework

- [[data-analytic-thinking|Data-Analytic Thinking]]: the decision-oriented pillar
- [[expected-value-framework|Expected Value Framework]]: the integration point
- [[data-science-for-business|Data Science for Business]]: Provost's foundational text
- [[data-science|Data Science]]: the field these pillars define

---
*Synthesized from the technical first-principles tradition (Grus) and the decision-science tradition (Provost), positioning them as complementary foundations rather than alternative approaches.*