mainstruct = dbstatus(%s);

disp('+++');
for pos=1 : length(mainstruct);
    substrct = mainstruct(pos);

    disp(['function ', substrct.name]);
    disp(['file ', substrct.file]);
    disp(substrct.line(:));
endfor;
disp('---');

clear mainstruct pos substrct;
