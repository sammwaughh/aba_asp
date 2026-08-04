% Experimental cautious nd ASP-ABAlearn with asm_intro(sechk).
% Matches configs/baseline_cautious_config.pl except asm_intro.
% H7b identity: nd_cautious_sechk (not a published ECAI/AAMAS configuration).

:- set_lopt(learning_mode(cautious)).

:- set_lopt(folding_mode(nd)).
:- set_lopt(folding_steps(10)).

:- set_lopt(folding_selection(any)).

:- set_lopt(folding_space(all)).

:- set_lopt(asm_intro(sechk)).

:- set_lopt(post_folding_test_entailment(true)).

:- set_lopt(check_ic).
