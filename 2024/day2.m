[ans1, ans2] = compute_day2("inputs/day2")
% [ans1, ans2] = compute_day2("inputs/day2_test")

%%
function [ans1, ans2] = compute_day2(dataloc)
    % Import and preamble
    reports = readlines(dataloc, 'EmptyLineRule', 'skip');
    reports = arrayfun(...
        @(x) double(split(x)), reports, 'UniformOutput', false);

    % Part 1
    safe_undamped = cellfun(@issafe, reports);

    % Part 2
    safe_damped = cellfun(@(x) issafe(x, use_dampener=true), reports);

    % Results
    ans1 = sum(safe_undamped);
    ans2 = sum(safe_damped);
end

%%
function tf = issafe(report, opts)
    arguments
        report (:,1) double
        opts.use_dampener logical = false
    end

    dx = diff(report);
    tf = ...
        all((dx(1) .* dx) > 0) ... % Monotonically increasing or decreasing
        && all(abs(dx) <= 3);     % No step greater than three

    if ~tf && opts.use_dampener
        nlevels = length(report);
        for exclude=1:nlevels
            % Try without each level in turn
            retain = setdiff(1:nlevels, exclude);
            if issafe(report(retain))
                tf = true;
                return
            end
        end
    end
end
