[ans1, ans2] = compute_day1("inputs/day1")

%%
function [ans1, ans2] = compute_day1(dataloc)
    % Import and preamble
    data = readmatrix(dataloc);
    data = sort(data);
    left = data(:,1);
    right = data(:,2);

    % Part 1
    distance = abs(right - left);

    % Part 2
    function s = compute_similarity(x, A, B)
        s = x * sum(A == x) * sum(B == x);
    end
    similarity = arrayfun(@(x) compute_similarity(x, left, right), unique(left));

    % Results
    ans1 = sum(distance);
    ans2 = sum(similarity);
end
