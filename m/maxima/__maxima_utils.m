# Is a script file not a function file:
1;

function cmd = __maximaFormatCommand(varargin)
    n = length(varargin);
    ss = "";
    cmd_list = "";
    for i = 1 : n
        ss = strcat(ss, "%s ");
        tmp = sprintf(" \"string(%s);\"", varargin{i});
        cmd_list = strcat(cmd_list, tmp);
    endfor
    cmd = sprintf("echo %s", ss);
    cmd = sprintf(cmd, cmd_list);
    cmd = strcat(cmd, " | maxima --very-quiet");
endfunction

function output = __maximaFormatOutput(str)
    output = deblank(strjust(strrep(str, "%", ""), "left")); 
endfunction

function result = __maxima2str(varargin)
	in = "";
	retult = "";
	n = length(varargin);
	if(n == 0)
		error ("__maxima2str: expecting command argument");
		return;
	endif
	in = __maximaFormatCommand(varargin{:});
	[status, m_result] = system(in);
	if(status == 0) 
		result = __maximaFormatOutput(m_result);	
	endif;
endfunction

function result = __maxima2num(cmd)
    m_result = __maxima2str(cmd); 
    try
        result = eval (m_result);
        return;
    catch
        e = lasterr();
        printf("%s maxima: %s",e(1:6), e(7:length(e)));
        error ("maxima: numeric result expected");
        return;
    end_try_catch
endfunction

function result = __maxima2sym(varargin)
	n = length(varargin);
	retult = NaN;
	if(n == 0)
		error ("maxima: expecting command argument");
		return;
	endif
	in = "";
	command = varargin{1};
	if(ischar(command) == 0)
		command = to_char(command);
	endif
	in = __maximaFormatCommand(command);
	[status, m_result] = system(in);
	if(status != 0) 
		error ("maxima: executions error");
		return;
	endif
	m_result = __maximaFormatOutput(m_result); 
	if(n == 1)
		try
			result = eval (m_result);
			return;
		catch
			e = lasterr();
			printf("%s maxima: %s",e(1:6), e(7:length(e)));
			error ("maxima: numeric result expected");
			return;
		end_try_catch
	endif
	try
		symbols;
		for i = 2 : n 
			var_to_replace = to_char(varargin{i});
			if(ischar(var_to_replace) == 0)
				var_to_replace = to_char(var_to_replace);
			endif
			pos = index(m_result, var_to_replace);
			if (!is_sym(varargin{i}) && pos > 0)
				err = sprintf("\"%s\" must be declared symbolic",varargin{i});
				error(err);
				return;	
			endif
			var_to_put = sprintf("varargin{%d}",i);
			m_result = strrep(m_result, var_to_replace, var_to_put);
		endfor
		m_result = __maximaCaptitalizeSymFunc(m_result);
		m_result = __maximaReplaceUnaryMinusOperator(m_result);
		result = eval(m_result);		
	catch
		e = lasterr();
		printf("%s maxima: %s",e(1:6), e(7:length(e)));
		return;
	end_try_catch
endfunction

function result = __maximaCaptitalizeSymFunc(inStr)
	map = __maximaMapFunctions();
	result = inStr;
	for i = 1 : length(map)
		var_to_replace = map{i,2};
		var_to_put = map{i,1};
		result = strrep (result, var_to_replace, var_to_put);
	endfor
endfunction

function result = __maximaReplaceUnaryMinusOperator(inStr)
	result = inStr;
	op = "-";
	expression = "(-1)*";
	pos = index(result, op);
	if (pos == 1)
		result = result(2:length(result));
		result = strcat(expression, result);
	endif
endfunction

function list = __maximaMapFunctions()
	list = cell();
	x = 1;
	y = 1;
	list(x,y) = "Abs"; list(x++,y+1) = "abs";
	list(x,y) = "Sqrt"; list(x++,y+1) = "sqrt";
	list(x,y) = "Cos"; list(x++,y+1) = "cos";
	list(x,y) = "Sin"; list(x++,y+1) = "sin";
	list(x,y) = "Tan"; list(x++,y+1) = "tan";
	list(x,y) = "1/Tan"; list(x++,y+1) = "cot";
	% los que estan comentas a continuacion no son necesarios, por ser casos particulares de los primeros.
	%list(x,y) = "aCos"; list(x++,y+1) = "acos";
	%list(x,y) = "aSin"; list(x++,y+1) = "asin";
	%list(x,y) = "aTan"; list(x++,y+1) = "atan";
	%list(x,y) = "aTan2"; list(x++,y+1) = "atan2";
	%list(x,y) = "Cosh"; list(x++,y+1) = "cosh";
	%list(x,y) = "Sinh"; list(x++,y+1) = "sinh";
	%list(x,y) = "Tanh"; list(x++,y+1) = "tanh";
	%list(x,y) = "aCosh"; list(x++,y+1) = "acosh";
	%list(x,y) = "aSinh"; list(x++,y+1) = "asinh";
	%list(x,y) = "aTanh"; list(x++,y+1) = "atanh";
	list(x,y) = "Exp"; list(x++,y+1) = "exp";
	list(x,y) = "Log"; list(x++,y+1) = "log";
	%list(x,y) = "Zeta"; list(x++,y+1) = "zeta"; %esta funcion no existe en octave
	%list(x,y) = "Tgamma"; list(x++,y+1) = "tgamma"; %esta funcion no existe en octave
	list(x,y) = "Lgamma"; list(x++,y+1) = "lgamma";
	list(x,y) = "Beta"; list(x++,y+1) = "beta";
	list(x,y) = "Factorial"; list(x++,y+1) = "factorial";
	list(x,y) = "Binomial"; list(x++,y+1) = "binomial";
	%list(x,y) = "Order"; list(x++,y+1) = "order"; %esta funcion no existe en octave
	list(x,y) = "Gcd"; list(x++,y+1) = "gcd";
	list(x,y) = "Lcm"; list(x++,y+1) = "lcm";
	list(x,y) = "Series"; list(x++,y+1) = "series";
	list(x,y) = "Pi"; list(x++,y+1) = "pi";
endfunction
