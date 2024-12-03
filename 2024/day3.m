[ans1, ans2] = compute_day3("inputs/day3")
% [ans1, ans2] = compute_day3("inputs/day3_test")

%%
function [ans1, ans2] = compute_day3(dataloc)
    % Import and preamble
    memory = string(fileread(dataloc));

    expr = 'mul\((\d+),(\d+)\)';
    [pairs, idx_mul] = regexp(memory, expr, 'tokens', 'start');
    pairs = cellfun(@double, pairs, 'UniformOutput', false);
    pairs = vertcat(pairs{:});

    idx_on = [1, regexp(memory, "do\(\)")];
    idx_off = regexp(memory, 'don''t');

    control = table(...
        [idx_on'; idx_off'], ...
        [repmat("on", length(idx_on), 1); repmat("off", length(idx_off), 1)], ...
        'VariableNames', ["idx", "command"]);
    control = sortrows(control);
    % Discard any repeated commands after the first
    retain = [true; control.command(2:end) ~= control.command(1:end-1)];
    control = control(retain,:);

    idx_on = control.idx(control.command == "on");
    idx_off = control.idx(control.command == "off");

    if length(idx_on) > length(idx_off)
        idx_off = [idx_off; strlength(memory)+1];
    end

    idx_pairs_retain = false(size(idx_mul));
    for idx_pair=1:length(idx_on)
        idx_pairs_retain = idx_pairs_retain | ...
            (idx_mul > idx_on(idx_pair) & idx_mul < idx_off(idx_pair));
    end
    valid_pairs = pairs(idx_pairs_retain',:);

    % Part 1
    products = prod(pairs,2);

    % Part 2
    valid_products = prod(valid_pairs,2);

    % Results
    ans1 = sum(products);
    ans2 = sum(valid_products);
end
