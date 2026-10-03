# Workload design

A useful local experiment keeps three categories separate.

## Cold runs

Cold runs include model loading and are appropriate for infrequent jobs or workflows that rotate between many models.

## Warm runs

Warm runs keep the model available between requests. They are closer to a local service receiving repeated work.

## Context sweeps

Context sweeps hold generation settings constant while prompt length changes. This makes prompt-processing cost visible instead of mixing it with output length.

The runner records both successful and failed processes. A failed configuration can be informative when a model does not fit the intended workload or a particular command-line option is unsupported.
