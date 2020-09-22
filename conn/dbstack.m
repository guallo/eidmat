[mainstruct, III] = dbstack(%s);

printf('index '); disp(III);

disp('+++');
for pos=1 : length(mainstruct);
    substrct = mainstruct(pos);

    disp(['function ', substrct.name]);
    disp(['file ', substrct.file]);
    printf('line '); disp(substrct.line);
    printf('column '); disp(substrct.column);
endfor;
disp('---');

clear mainstruct III pos substrct;
