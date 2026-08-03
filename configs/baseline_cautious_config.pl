% Repository-baseline cautious ASP-ABAlearn configuration.
%
% These options explicitly pin the learning-relevant defaults from aba_asp.pl
% so target-wise runs do not depend on implicit initialisation.  check_ic is an
% output-only addition: it emits the final checked ASP artefact after learning.

:- set_lopt(learning_mode(cautious)).

:- set_lopt(folding_mode(nd)).
:- set_lopt(folding_steps(10)).

:- set_lopt(folding_selection(any)).

:- set_lopt(folding_space(all)).

:- set_lopt(asm_intro(relto)).

:- set_lopt(post_folding_test_entailment(true)).

:- set_lopt(check_ic).
