% Repository-baseline cautious ASP-ABAlearn with folding_steps(2).
% Matches configs/baseline_cautious_config.pl except folding_steps.
% H6a/H6b ablation identity: baseline_cautious_steps2

:- set_lopt(learning_mode(cautious)).

:- set_lopt(folding_mode(nd)).
:- set_lopt(folding_steps(2)).

:- set_lopt(folding_selection(any)).

:- set_lopt(folding_space(all)).

:- set_lopt(asm_intro(relto)).

:- set_lopt(post_folding_test_entailment(true)).

:- set_lopt(check_ic).
