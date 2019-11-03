## -*- texinfo -*-
## @deftypefn {Function File} {} maxima2num (@var{cmd})
## Return a nummeric result calculated by Maxima in response to 
## command @var{cmd} 
## The argument is a Maxima command.
##
## Example:
## @example
## y=maxima2num("subst(1,x,diff(x^3+3*x^2,x))")
## 
## @result{} y = 9
## @end example
## In this example the class of "y" is "double"
##
## @seealso{maxima2sym, maximaFromFile, maxima2num}
## @end deftypefn

## Author: Leansy Alfonso Pérez <leansy@uci.cu>
## Created: February 2009

function result=maxima2num(cmd)
    __maxima_utils;
    result = __maxima2num(cmd);
endfunction

