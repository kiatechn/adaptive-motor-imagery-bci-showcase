# Public disclosure boundary

This document defines what may and may not be added to this portfolio copy while the associated manuscript remains in preparation.

## Purpose of this repository

The repository may demonstrate the research problem, system-level thinking, engineering scope, actual interface and responsible limitations. It is not the scientific reproducibility package and must not contain enough private material to reproduce the unpublished study or reconstruct its analysis.

## Approved public material

- plain-language project descriptions;
- high-level architecture diagrams;
- names of established techniques such as EEG, motor imagery, CSP and SVM;
- qualitative descriptions of the responsiveness, rejection, latency and false-activation trade-offs;
- screenshots of the actual interface after privacy review and without participant output;
- hardware-only photographs that have passed privacy review;
- general limitations and planned next steps; and
- a link to the paper after publication.

## Material that remains private

- raw, preprocessed or derived participant EEG;
- task logs, event records and participant metadata;
- participant photographs without explicit publication consent;
- participant-level or small-cell results;
- trained models, saved features and participant prediction streams;
- numerical aggregate findings, statistical tests and paper figures;
- exact channel selections, timing windows, thresholds or hyperparameters used in the paper;
- research implementation source code;
- frozen paper configurations and dependency environment;
- optimisation sweeps, ablations and decision history;
- manuscripts, reviewer material, ethics documents and consent forms; and
- local paths, credentials, device identifiers or screen notifications.

## Images and video

Before adding a photograph, screenshot or video:

1. remove names, faces, participant labels, trial identifiers and device serial numbers;
2. crop local paths, notifications, email addresses and unrelated screen content;
3. do not show raw EEG, prediction streams, private settings or unpublished numerical results;
4. remove hidden metadata where appropriate;
5. label the operating mode and what the image demonstrates honestly; and
6. obtain supervisor, co-author and governance approval when required.

The included game screenshot shows the actual interface without participant data, EEG traces, predictions, model output or an unpublished performance result.

## Before expanding the release

Do not add results, methods-level detail, implementation code or data until the target journal policy, anonymous-review requirements, university intellectual-property position, ethics approval, data-governance rules and co-author permissions have been checked. Review the complete Git history as well as the latest working tree.

At publication, prepare a separate versioned release that matches the manuscript and archive it in a repository capable of issuing a persistent identifier if appropriate.
