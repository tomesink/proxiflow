import traceback
import inspect
import os
import sys
from typing import Callable
import polars as pl


def generate_trace(exception: Exception, target_method: Callable[..., pl.DataFrame]) -> str:
    """
    Generate a custom error message containing the file name, line number, and error description.

    This function walks the traceback and filters out frames originating from external libraries,
    returning an error message with the first frame from the user's codebase.

    :param exception: The caught exception object
    :type exception: Exception
    :param target_method: The target method where the error occurs
    :type target_method: function
    :return: Formatted error message with custom traceback information
    :rtype: str
    """
    tb_list = traceback.extract_tb(sys.exc_info()[2])
    target_file = inspect.getsourcefile(target_method)

    # Reverse the traceback list and find the first frame that's in the target file
    for tb_item in reversed(tb_list):
        file_path = os.path.abspath(tb_item.filename)
        if file_path == target_file:  # Check if the file is the target file
            file_name = os.path.basename(file_path)
            line_number = tb_item.lineno
            error_desc = str(exception)
            return f"FILE: '{file_name}', LINE: {line_number}:\n{error_desc}"

    # Fallback to the original error message if no matching frame is found
    return f"An error occurred: {str(exception)}"
