var = whos;

for index=1 : length(var);
    if !strcmp(var(index).name, 'var');
        eval([var(index).name, " = 'value';"]);
    endif;
endfor;

clear var index;

try;
    load 'path';
catch;
end_try_catch;

var = whos;

disp('***');

for index=1 : length(var);
    if !strcmp(var(index).name, 'var');
        if !strcmp(var(index).class, 'char');
            disp(var(index).name);
        else;
            eval(["if !strcmp(", var(index).name, ", 'value');",
                      "disp(var(index).name);",
                  "endif;"]);
        endif;
    endif;
endfor;

clear var index;
