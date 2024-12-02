[ans1, ans2] = compute_day2("inputs/day2")
% [ans1, ans2] = compute_day2("inputs/day2_test")

%%
function [ans1, ans2] = compute_day2(dataloc)
    % Import and preamble
    reports = readcell(dataloc, "Delimiter", ["\n"]);
    reports = cellfun(...
        @(x) double(split(string(x))), reports, 'UniformOutput', false);

    % Part 1
    safe = cellfun(@issafe, reports);

    % Part 2

    % Results
    ans1 = sum(safe);
    ans2 = 0;
end

%%
function tf = issafe(report)
    dx = diff(report);
    tf = ...
        all((dx(1) .* dx) > 0) ... % Monotonically increasing or decreasing
        && all(abs(dx) <= 3);     % No step greater than three
end
