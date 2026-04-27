# METHOD AND APPARATUS FOR ADAPTIVE QUERY ROUTING

<!-- source: 01_claims_multicol.pdf | kind: native | lang: en | pages: 1 -->

## Abstract

A method for adaptive routing of database queries across heterogeneous backends using a learned cost model. The system selects a backend based on predicted latency, freshness, and load, and adapts the model online from execution feedback.

## Claims

**1.** A method comprising: receiving a query Q at a router; computing a feature vector F from Q; predicting, via a cost model M, an expected latency for each backend in a set B; and dispatching Q to argmin_b latency(b).

**2.** The method of claim 1, wherein computing F includes hashing the query plan and concatenating cardinality estimates.  *(depends on [1])*

**3.** The method of claim 1, wherein M is a gradient-boosted regressor updated nightly from execution traces.  *(depends on [1])*

**4.** The method of claim 3, wherein updating M comprises minimising a Huber loss over (F, observed_latency) tuples.  *(depends on [3])*

**5.** The method of any of claims 1 to 4, further comprising falling back to a default backend when predicted latency exceeds a threshold T.  *(depends on [1, 2, 3, 4])*

**6.** An apparatus comprising memory and one or more processors configured to perform the method of any one of claims 1 to 5.  *(depends on [1, 2, 3, 4, 5])*

**7.** A non-transitory computer-readable medium storing instructions that, when executed, cause performance of the method of claim 1.  *(depends on [1])*
