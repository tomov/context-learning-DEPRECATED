% Load the data from the .csv file generated by snippets/parse.py from the psychopy
% wide format csv's for all subjects.
% Also includes some constants and some helper functions.
%

format = '%s %s %s %d %s %s %s %d %d %s %s %s %f %d %s %s %d %d %d';

[participant, session, mriMode, isPractice, restaurantsReshuffled, foodsReshuffled, contextRole, contextId, cueId, sick, corrAns, response.keys, response.rt, response.corr, restaurant, food, isTrain, roundId, trialId] = ...
    textread('pilot.csv', format, 'delimiter', ',', 'headerlines', 1);

roundsPerContext = 3; % = blocks per context = runs per context = runs / 3
trialsNReps = 5; % = training trials per round / 4
trialsPerRound = 24;

if ~exist('analyze_with_gui') || ~analyze_with_gui % for the GUI; normally we always reload the data
    which_rows = logical(true(size(participant))); % which rows to include/exclude. By default all of them
    subjects = unique(participant(which_rows))'; % the unique id's of all subjects
    
    contextRoles = {'irrelevant', 'modulatory', 'additive'}; % should be == unique(contextRole)'

    make_optimal_choices = false;
end

% b/c sometimes they're vectors of size 1 == scalars, so can't do mean([a b c d e]) 
%
get_means = @(x1c1, x1c2, x2c1, x2c2) [mean(x1c1) mean(x1c2) mean(x2c1) mean(x2c2)];
get_sems = @(x1c1, x1c2, x2c1, x2c2) [std(x1c1) / sqrt(length(x1c1)) std(x1c2) / sqrt(length(x1c2)) std(x2c1) / sqrt(length(x2c1)) std(x2c2) / sqrt(length(x2c2))];

