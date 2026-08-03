% Experimental Greedy + cautious ASP-ABAlearn configuration (H5).
%
% Matches configs/aamas2025_config.pl except learning_mode(cautious).
% This is NOT a published AAMAS configuration: the AAMAS 2025 paper's
% incoherent extension is brave. Do not name or describe this file as
% aamas_cautious.
%
% post_folding_test_entailment(true) is pinned explicitly; it is also the
% engine default and is effective under aamas2025. check_ic retains the
% checked ASP artefact after learning.

:- set_lopt(learning_mode(cautious)).

:- set_lopt(folding_mode(greedy)).

:- set_lopt(folding_selection(mgr)).

:- set_lopt(folding_space(bk)).

:- set_lopt(asm_intro(relto)).

:- set_lopt(post_folding_test_entailment(true)).

:- set_lopt(check_ic).
