if(__ML_MACROS_INCLUDED)
    return()
endif()
set(__ML_MACROS_INCLUDED TRUE)

# <TOOL>(ARGS): Macros for calling ML tools. Argumens are passed to the tool
#               directly. Keyword arguments intended for execute_process()
#               may be used.

macro(MLPP)
    execute_process(COMMAND python -m mlpp ${ARGN} RESULT_VARIABLE MLPP_RESULT)
endmacro()

macro(MLCPPGEN)
    execute_process(COMMAND python -m mlcppgen ${ARGN} RESULT_VARIABLE MLGEN_RESULT)
endmacro()

macro(ML2PO)
    execute_process(COMMAND python -m ml2po ${ARGN} RESULT_VARIABLE ML2PO_RESULT)
endmacro()

macro(VALIDATETRA)
    execute_process(COMMAND python -m validateTra ${ARGN} RESULT_VARIABLE VALIDATETRA_RESULT)
endmacro()

macro(PO2ML)
    execute_process(COMMAND python -m po2ml ${ARGN} RESULT_VARIABLE PO2ML_RESULT)
endmacro()
