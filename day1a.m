clear variables
close all

input_folder = "Input\";
input_file = "day1a.txt";
file_path = input_folder + input_file;

input = readmatrix(file_path,'OutputType','string','EmptyLineRule','read');
input = fillmissing(input,'constant',"");

input_cells = {};
curr_elf = 1;

for i=1:height(input)
    if input(i) == ""
        input_cells{end+1} = str2double(input(curr_elf:i-1));
        curr_elf = i+1;
    end
end
input_cells{end+1} = str2double(input(curr_elf:end));

cal_per_elf = cellfun(@sum, input_cells);
[max_cal, idx_elf] = max(cal_per_elf);

max_cal
idx_elf