---
type: synthesized
aliases: ["TimeGrouper deprecation", "pd.Grouper unified interface"]
tags: ["pandas", "groupby", "time-series", "deprecation", "data-wrangling"]
relationships:
  - target: groupby-operation
    type: extends
  - target: groupby
    type: extends
  - target: groupby-object
    type: extends
  - target: rolling-window-operations
    type: extends
---

# pd.Grouper: Generalization of pd.TimeGrouper

# pd.Grouper: Generalization of pd.TimeGrouper

## Summary

`pd.TimeGrouper`, described in McKinney's *Python for Data Analysis* (2017), has since been deprecated and replaced by the more general `pd.Grouper` interface.

## Historical Context

In the 2017 edition of *Python for Data Analysis*, `pd.TimeGrouper` was introduced as a convenience class for performing time-based groupby operations — for example, resampling or aggregating a time-indexed DataFrame by month, quarter, or other frequency offsets.

## The Generalization: `pd.Grouper`

`pd.Grouper` supersedes `pd.TimeGrouper` and provides a unified interface for specifying groupby behavior across multiple dimensions:

- **Time-based grouping**: equivalent to the old `TimeGrouper`, using the `freq` parameter (e.g., `pd.Grouper(freq='M')` for monthly grouping).
- **Key-based grouping**: supports grouping by arbitrary column keys via the `key` parameter.
- **Level-based grouping**: supports grouping by index levels via the `level` parameter.

### Example (time-based)

# Deprecated approach
df.groupby(pd.TimeGrouper(freq='M'))

# Modern equivalent
df.groupby(pd.Grouper(freq='M'))


### Example (key + frequency)

# Group by a non-index datetime column at monthly frequency
df.groupby(pd.Grouper(key='date_col', freq='M'))


## Relationship to GroupBy

`pd.Grouper` integrates directly with the standard [[groupby|GroupBy]] machinery in pandas, producing a [[groupby-object|GroupBy Object]] that supports all standard aggregation, transformation, and filtering operations. It effectively extends the [[groupby-operation|GroupBy Operation]] pattern to handle time-frequency semantics without a separate class.

## Key Takeaway

Users of McKinney's 2017 text who encounter `pd.TimeGrouper` should substitute `pd.Grouper` with equivalent parameters. The underlying split-apply-combine semantics remain unchanged; only the API surface was consolidated.