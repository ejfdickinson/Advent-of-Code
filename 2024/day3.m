[ans1, ans2] = compute_day3("inputs/day3")
% [ans1, ans2] = compute_day3("inputs/day3_test")

%%
function [ans1, ans2] = compute_day3(dataloc)
    % Import and preamble
    memory = string(fileread(dataloc));

    expr = 'mul\((\d+),(\d+)\)';
    pairs = regexp(memory, expr, 'tokens');
    pairs = cellfun(@double, pairs, 'UniformOutput', false);
    pairs = vertcat(pairs{:});

    % Part 1
    products = prod(pairs,2);

    % Part 2

    % Results
    ans1 = sum(products);
    ans2 = 0;
end
