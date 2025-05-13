import inspect
import re
import warnings
import functools

def opt(option_name):
    """
    Placeholder for an options system. In a real implementation, this would
    check configuration options.
    """
    # Default to True for now - in a real implementation, this would check
    # against a configuration system
    return True

def check_args(*args):
    """
    Check function arguments against various conditions.
    
    This function allows for validating function arguments against various conditions
    like type, value range, membership in a set, etc.
    
    Returns:
        None: If all checks pass or if argument checking is disabled
        
    Raises:
        ValueError: If any check fails
    """
    # Skip if argument checking is disabled
    if not opt("check_arguments"):
        return
    
    # Get the calling frame and function
    frame = inspect.currentframe().f_back
    call_info = inspect.getframeinfo(frame)
    
    # Extract the function call
    call_text = call_info.code_context[0].strip()
    # Remove any namespace prefix (equivalent to R's gsub)
    call_text = re.sub(r'^[^:]+::', '', call_text)
    # Parse the function name
    match = re.search(r'(\w+)\(', call_text)
    if match:
        func_name = match.group(1)
    else:
        func_name = "unknown_function"
    
    # Create an environment similar to R's new.env
    env = {}
    
    # Store the function call
    env['call'] = func_name
    
    # Define helper functions in the environment
    def is_true(condition, *messages, warning=False):
        if not condition:
            message = ' '.join(str(m) for m in messages)
            if not message:
                # Get the argument name from the call stack
                frame = inspect.currentframe()
                args, _, _, values = inspect.getargvalues(frame)
                arg_name = args[1]  # The condition argument name
                message = f"Argument {arg_name} is ill defined."
            return {'pass': False, 'msg': message, 'warning': warning}
        else:
            return {'pass': True}
    
    def has_length(arg, l, msg=None, warning=False):
        if msg is None:
            # Get the argument name
            frame = inspect.currentframe()
            args, _, _, values = inspect.getargvalues(frame)
            arg_name = args[0]  # The arg argument name
            msg = f"Argument {arg_name} not of length {l}."
        return is_true(len(arg) == l, msg, warning=warning)
    
    def not_func(condition, *messages, warning=False):
        return is_true(not condition, *messages, warning=warning)
    
    def one_of(arg, *match, warning=False):
        # Get the argument name
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        arg_name = args[0]  # The arg argument name
        
        msg_parts = [f"'{m}'" for m in match]
        if len(match) == 2:
            msg = " or ".join(msg_parts)
        elif len(match) > 2:
            msg = "one of " + ", ".join(msg_parts)
        else:
            msg = msg_parts[0] if msg_parts else ""
        
        return is_true(
            arg in match,
            f"Argument {arg_name} is not {msg}."
        )
    
    def by_call(arg, warning=False):
        # Get the argument name
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        arg_name = args[0]  # The arg argument name
        
        # Get the function's default arguments
        func = frame.f_back.f_globals.get(env['call'])
        if not func:
            raise ValueError(f"Function {env['call']} not found")
        
        func_args = inspect.getfullargspec(func).defaults
        func_arg_names = inspect.getfullargspec(func).args
        
        # Find the matching argument
        try:
            idx = func_arg_names.index(arg_name)
            match = func_args[idx - (len(func_arg_names) - len(func_args))]
        except (ValueError, IndexError):
            raise ValueError("by_call has no matching arg.")
        
        msg_parts = [f"'{m}'" for m in match]
        if len(match) == 2:
            msg = " or ".join(msg_parts)
        elif len(match) > 2:
            msg = "one of " + ", ".join(msg_parts)
        else:
            msg = msg_parts[0] if msg_parts else ""
        
        return is_true(
            arg in match,
            f"Argument {arg_name} is not {msg}."
        )
    
    def within(arg, lower, upper, warning=False):
        # Get the argument name
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        arg_name = args[0]  # The arg argument name
        
        return is_true(
            arg >= lower and arg <= upper,
            f"Argument {arg_name} is not within {lower} and {upper} (is {arg})"
        )
    
    def at_least(arg, lower, msg=None, warning=False):
        # Get the argument name
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        arg_name = args[0]  # The arg argument name
        
        if msg is None:
            msg = f"Argument {arg_name} is not greater or equal to {lower} (is {arg})"
        
        return is_true(arg >= lower, msg, warning=warning)
    
    def at_most(arg, upper, msg=None, warning=False):
        # Get the argument name
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        arg_name = args[0]  # The arg argument name
        
        if msg is None:
            msg = f"Argument {arg_name} is not less or equal to {upper} (is {arg})"
        
        return is_true(arg <= upper, msg, warning=warning)
    
    def by_class(param, class_name, warning=False):
        # Get the argument name
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        arg_name = args[0]  # The param argument name
        
        return is_true(
            isinstance(param, class_name),
            f"Argument {arg_name} is not of class {class_name.__name__}."
        )
    
    def is_logical(param, warning=False):
        # Get the argument name
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        arg_name = args[0]  # The param argument name
        
        return is_true(
            isinstance(param, bool),
            f"Argument {arg_name} is not logical."
        )
    
    def is_deprecated():
        # Get the function's default arguments
        func = frame.f_globals.get(env['call'])
        if not func:
            return {'pass': True}
        
        func_args = inspect.getfullargspec(func).defaults
        func_arg_names = inspect.getfullargspec(func).args
        
        # Find deprecated arguments
        deprecated_args = []
        for i, default in enumerate(func_args):
            if default == "deprecated":
                arg_name = func_arg_names[-(len(func_args) - i)]
                if arg_name in frame.f_locals:
                    deprecated_args.append(arg_name)
        
        if deprecated_args:
            message = f"Argument{'s' if len(deprecated_args) > 1 else ''} "
            message += ", ".join(f"'{arg}'" for arg in deprecated_args)
            message += f" {'are' if len(deprecated_args) > 1 else 'is'} deprecated"
            return {'pass': False, 'msg': message, 'warning': True}
        
        return {'pass': True}
    
    # Add all helper functions to the environment
    env.update({
        'is_true': is_true,
        'has_length': has_length,
        'not': not_func,
        'one_of': one_of,
        'by_call': by_call,
        'within': within,
        'at_least': at_least,
        'at_most': at_most,
        'by_class': by_class,
        'is_logical': is_logical,
        'is_deprecated': is_deprecated
    })
    
    # Process all arguments
    results = []
    for arg in args:
        # Evaluate the argument in the environment
        try:
            result = arg(env)
            results.append(result)
        except Exception as e:
            results.append({'pass': False, 'msg': str(e), 'warning': False})
    
    # Add the deprecated check
    results.append(env['is_deprecated']())
    
    # Filter for failed checks
    failed = [r for r in results if r and not r.get('pass', True)]
    
    # Process warnings
    warning_msgs = [r['msg'] for r in failed if r.get('warning', False)]
    if warning_msgs:
        for i, msg in enumerate(warning_msgs, 1):
            warnings.warn(f"{i}: {msg}", stacklevel=2)
    
    # Process errors
    error_msgs = [r['msg'] for r in failed if not r.get('warning', False)]
    if error_msgs:
        error_text = "\n" + "\n".join(f"{i}: {msg}" for i, msg in enumerate(error_msgs, 1))
        raise ValueError(error_text)

# Make the helper functions available at module level
def by_class(param, class_name, warning=False):
    """Check if parameter is of the specified class."""
    pass

def by_call(arg, warning=False):
    """Check if argument is one of the allowed values for this parameter."""
    pass

def not_func(condition, *messages, warning=False):
    """Negate a condition check."""
    pass

def within(arg, lower, upper, warning=False):
    """Check if argument is within the specified range."""
    pass

def one_of(arg, *match, warning=False):
    """Check if argument is one of the specified values."""
    pass

def has_length(arg, l, msg=None, warning=False):
    """Check if argument has the specified length."""
    pass

def is_true(condition, *messages, warning=False):
    """Check if a condition is true."""
    pass

def at_least(arg, lower, msg=None, warning=False):
    """Check if argument is at least the specified value."""
    pass

def at_most(arg, upper, msg=None, warning=False):
    """Check if argument is at most the specified value."""
    pass

def is_logical(param, warning=False):
    """Check if parameter is a boolean."""
    pass