% Experimental brave nd ASP-ABAlearn with asm_intro(sechk).
% Matches configs/ecai2024_config.pl except asm_intro.
% H7a identity: nd_brave_sechk (not a published ECAI configuration).

:- set_lopt(learning_mode(brave)).

:- set_lopt(folding_mode(nd)).
:- set_lopt(folding_steps(10)).

:- set_lopt(folding_selection(any)).

:- set_lopt(folding_space(all)).

:- set_lopt(asm_intro(sechk)).

:- set_lopt(check_ic).
