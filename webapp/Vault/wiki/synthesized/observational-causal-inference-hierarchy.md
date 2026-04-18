---
type: synthesized
aliases: ["Causal Estimation Without Randomization", "Observational Causal Methods Hierarchy"]
tags: ["causal-inference", "observational-data", "confounders", "selection-bias", "counterfactual-reasoning", "quasi-experiment", "data-science"]
relationships:
  - target: causal-vs-predictive-targeting
    type: extends
  - target: causal-inference
    type: extends
  - target: causal-effect-estimation
    type: extends
  - target: causal-impact-models
    type: extends
  - target: predictive-analytics
    type: extends
---

# Observational Causal Inference: Credible Counterfactuals Under Weak Assumptions

# Observational Causal Inference: Credible Counterfactuals Under Weak Assumptions

## The Unifying Logic

Provost's framing of causal analytics as 'predicting both sides of the counterfactual'—what would happen under treatment and what would happen under control, for the same unit—provides the unifying logic beneath all observational causal methods. The challenge is that in the absence of randomized experiments, the counterfactual outcome is never directly observed. Every quasi-experimental and observational method is therefore a different strategy for making that double prediction *credible* under progressively weaker and more contested assumptions.

The hierarchy of methods can be read as a spectrum: at one end, randomized A/B tests manufacture credibility through design; at the other end, fully observational regression adjustments attempt to purchase credibility through modeling assumptions that are largely unverifiable. Hidden confounders, selection bias, and feedback loops each attack the credibility of the double prediction in distinct ways.

## The Three Threats

### Hidden Confounders
A confounder is a variable that affects both treatment assignment and the outcome. When confounders are unobserved, the treated and control groups differ in ways the analyst cannot measure or adjust for. The double prediction becomes unreliable because the 'control' prediction—what would have happened to the treated unit without treatment—is estimated from units that are systematically different in unobserved ways. Instrumental variable methods attempt to find a variable that shifts treatment assignment but has no direct path to the outcome, effectively restoring local randomization. Difference-in-differences exploits panel structure to difference out time-stable hidden confounders, under the parallel trends assumption.

### Selection Bias
Selection bias arises when the probability of entering the dataset is correlated with the outcome of interest. In advertising and targeting contexts (central to Provost's applied work at Dstillery), users who are exposed to an ad are not a random sample—they were selected by a prior predictive model. Estimating the incremental effect of the ad requires correcting for this selection. Propensity score methods, inverse probability weighting, and matching estimators all attempt to reweight the observed sample so that treatment and control groups are comparable on measured covariates. The critical limitation: they only control for *observed* selection, leaving residual bias from unobserved determinants of selection.

### Feedback Loops
Feedback loops occur when past outcomes influence future treatment assignment, creating dynamic confounding that simple cross-sectional methods cannot handle. In online platforms, a user's prior behavior shapes what content or ads they are shown, which shapes future behavior, which shapes future targeting—a cycle that renders static observational comparisons misleading. Marginal structural models and structural equation approaches attempt to break these loops by modeling the time-varying treatment process explicitly. However, the assumptions required (no unmeasured time-varying confounders) are strong and rarely testable.

## The Methods Hierarchy

| Method | Assumption Required | Threat Addressed |
|---|---|---|
| Randomized A/B test | None beyond SUTVA | All (by design) |
| Natural experiment | Exogenous variation exists | Hidden confounders |
| Instrumental variables | Valid instrument exists | Hidden confounders |
| Regression discontinuity | Local continuity at threshold | Selection near threshold |
| Difference-in-differences | Parallel trends | Time-stable hidden confounders |
| Propensity score matching | No unmeasured confounders | Observed selection |
| Regression adjustment | Correct functional form + no omitted variables | Observed confounders only |

Each row represents a different answer to the question: *what structure in the data or world licenses the counterfactual prediction?* Natural experiments (e.g., policy changes, weather shocks, lottery assignments) are particularly valued because exogenous variation approximates randomization without the cost of a controlled experiment.

## Causal Impact Models and Observational Data

Provost's paper 'Combining Observational and Experimental Data to Improve Large-Scale Decision-Making' (ICIS 2020) offers a practical synthesis: large A/B test data, even when expensive and impractical to run at full scale, can be used to build heterogeneous causal models—machine learning estimators that use the randomized subset to impute counterfactuals for the observational majority. This treats the experimental data not merely as a source of average treatment effects but as a calibration resource for individual-level counterfactual prediction. The resulting causal impact models estimate not just whether a treatment works on average, but *for whom* it works—the heterogeneous treatment effect problem central to precision targeting.

## The Gap Between Prediction and Causal Estimation

Provost's formal distinction in 'Causal Classification: Treatment Effect Estimation vs. Outcome Prediction' (JMLR 2022) maps directly onto this hierarchy. A predictive model targeting users likely to convert optimizes one side of the counterfactual (predicted outcome under treatment) without estimating the other (predicted outcome without treatment). This suffices when the correlation between predicted outcome and incremental effect is high—i.e., when heavy buyers are also heavy incremental buyers. It fails when the correlation breaks down: loyal customers who would have bought anyway, churners who are unreachable regardless. The observational methods hierarchy exists precisely to recover the *difference* between the two predictions, not just one side.

## Epistemic Humility and Assumption Auditing

A recurring theme in Provost's analytical style is explicit assumption accounting—making the conditions under which a conclusion holds visible rather than implicit. Applied to observational causal inference, this means: before reporting a causal estimate, enumerate which threats (hidden confounders, selection, feedback) the chosen method addresses, which it leaves unaddressed, and what evidence (placebo tests, sensitivity analyses, robustness checks) exists for or against the key identifying assumptions. The credibility of a causal claim is only as strong as the weakest untested assumption in the identification strategy.

## Connection to Counterfactual Explanations

The same counterfactual logic that structures Provost's causal targeting work also underlies his evidence counterfactual framework for model explanations (with Martens on Facebook Likes inference). In both cases, the core operation is identifying the minimal change to inputs that would change the output—for causal targeting, the input is treatment assignment; for explanation, the input is evidence features. The double-prediction frame unifies both: causal estimation asks 'what would the outcome have been under a different action?'; instance-level explanation asks 'what would the inference have been given different evidence?' Both are fundamentally counterfactual prediction problems dressed in different application contexts.