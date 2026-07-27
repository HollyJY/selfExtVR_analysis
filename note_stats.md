# TODOs: 
* [ ] preprocess, themantic data => scripts google file
* [ ] LLM alignment preprocessing, analysis, ratings, performance plots + NLP analysis
* [ ] pairwise tests for enhance vs counter, repeat vs counter
* [ ] CLMM for acceptance
* [ ] most important: from the interview data you collected perceived voice similarity right? we can qualittaively discuss this, but also if you can derive a clear response (yes / no / somewhat) from the interviews, you can add that as explanatory variable like so: response ~ semantic_disp * voice_identity * clone_similarity
* [ ] this would help us know if we have an issue with manipulation check, or generally if people don’t resonate with their own voice or don’t care, etc. either way, it is interesting to discuss
* [ ] make plots of these (like you have done already) as it shows clearly the key findings
* [ ] possibly an estimated marginal means analysis, can maybe help interpetation more easily than regression results
* [ ] later: (spearman) correlations between acceptance scores and sona and acceptance and sopa, split by semantic_displ and voice_clone conditions. I’m curious if they dissociate or not, that can also be a finding
* [ ] also add other potential moderators: IPQ, embodiment questionnaires, etc.


# @2026-07-27 mon


# @2026-07-24 fri
- [?] how to count SoA
- [x] CLMM or LMM? none ordinal...
  - [x] CLMM for acceptance
  - [x] LMM for the avarage score 

> seems semantic displacement had a clear effect on perceived acceptance and agency, however voice identity showed limited effects. if I’m interpreting correctly, robotic voice increased negative agency in the Counter condition, but voice identity didn’t significantly affect acceptance or positive agency, and also didn’t interact significantly with semantic displacement.

---
# @2026-07-21 meet

- [ ] normality of the data
- [ ] outliers, need to check LLM result, exclude several trials
- [ ] cumulative link mixture models
	- maybe, adding, sense of presence IPQ
- [ ] pair-wised contrast

### eye-tracking
- ==continuous data==, e.g. eye-tracking; linear mixed-effect model
	- [?] gaze, gaze1/total time; gaze2/total time
- also as independent variable, dwell time

### LLM
- benchmark for alignment, diagram
- after experiment
- [ ] find reference

### limitations
- noquestions about how do they like the voice or something?
  - yes in interview