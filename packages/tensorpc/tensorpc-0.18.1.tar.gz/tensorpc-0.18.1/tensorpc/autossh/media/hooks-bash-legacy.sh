# ---------------------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

# Prevent the script recursing when setting up
if [[ -n "$VSCODE_SHELL_INTEGRATION" ]]; then
    builtin return
fi

VSCODE_SHELL_INTEGRATION=1
VSCODE_INJECTION=1
# enable shell login to get same environment as manual ssh 
VSCODE_SHELL_LOGIN=1
# Run relevant rc/profile only if shell integration has been injected, not when run manually
if [ "$VSCODE_INJECTION" == "1" ]; then
    if [ -z "$VSCODE_SHELL_LOGIN" ]; then
        . ~/.bashrc
    else
        # Imitate -l because --init-file doesn't support it:
        # run the first of these files that exists
        if [ -f /etc/profile ]; then
            . /etc/profile
        fi
        # exceute the first that exists
        if [ -f ~/.bash_profile ]; then
            . ~/.bash_profile
        elif [ -f ~/.bash_login ]; then
            . ~/.bash_login
        elif [ -f ~/.profile ]; then
            . ~/.profile
        fi
        builtin unset VSCODE_SHELL_LOGIN
    fi
    builtin unset VSCODE_INJECTION
fi

# Disable shell integration if PROMPT_COMMAND is 2+ function calls since that is not handled.
if [[ "$PROMPT_COMMAND" =~ .*(' '.*\;)|(\;.*' ').* ]]; then
    builtin unset VSCODE_SHELL_INTEGRATION
    builtin return
fi

if [ -z "$VSCODE_SHELL_INTEGRATION" ]; then
    builtin return
fi

__vsc_initialized=0
__vsc_original_PS1="$PS1"
__vsc_original_PS2="$PS2"
__vsc_custom_PS1=""
__vsc_custom_PS2=""
__vsc_in_command_execution="1"
__vsc_current_command=""

__vsc_prompt_start() {
    builtin printf "\033]784;A\007"
}

__vsc_prompt_end() {
    builtin printf "\033]784;B\007"
}

__vsc_update_cwd() {
    builtin printf "\033]784;P;Cwd=%s\007" "$PWD"
}

__vsc_command_output_start() {
    builtin printf "\033]784;C\007"
    builtin printf "\033]784;E;$__vsc_current_command\007"
}

__vsc_continuation_start() {
    builtin printf "\033]784;F\007"
}

__vsc_continuation_end() {
    builtin printf "\033]784;G\007"
}

__vsc_command_complete() {
    if [ "$__vsc_current_command" = "" ]; then
        builtin printf "\033]784;D\007"
    else
        builtin printf "\033]784;D;%s\007" "$__vsc_status"
    fi
    __vsc_update_cwd
}
__vsc_update_prompt() {
    # in command execution
    if [ "$__vsc_in_command_execution" = "1" ]; then
        # Wrap the prompt if it is not yet wrapped, if the PS1 changed this this was last set it
        # means the user re-exported the PS1 so we should re-wrap it
        if [[ "$__vsc_custom_PS1" == "" || "$__vsc_custom_PS1" != "$PS1" ]]; then
            __vsc_original_PS1=$PS1
            __vsc_custom_PS1="\[$(__vsc_prompt_start)\]$PREFIX$__vsc_original_PS1\[$(__vsc_prompt_end)\]"
            PS1="$__vsc_custom_PS1"
        fi
        if [[ "$__vsc_custom_PS2" == "" || "$__vsc_custom_PS2" != "$PS2" ]]; then
            __vsc_original_PS2=$PS2
            __vsc_custom_PS2="\[$(__vsc_continuation_start)\]$__vsc_original_PS2\[$(__vsc_continuation_end)\]"
            PS2="$__vsc_custom_PS2"
        fi
        __vsc_in_command_execution="0"
    fi
}

__vsc_precmd() {
    __vsc_command_complete "$__vsc_status"
    __vsc_current_command=""
    __vsc_update_prompt
}

__vsc_preexec() {
    __vsc_initialized=1
    if [[ ! "$BASH_COMMAND" =~ ^__vsc_prompt* ]]; then
        __vsc_current_command=$BASH_COMMAND
    else
        __vsc_current_command=""
    fi
    __vsc_command_output_start
}

# Debug trapping/preexec inspired by starship (ISC)
if [[ -n "${bash_preexec_imported:-}" ]]; then
    __vsc_preexec_only() {
        if [ "$__vsc_in_command_execution" = "0" ]; then
            __vsc_in_command_execution="1"
            __vsc_preexec
        fi
    }
    precmd_functions+=(__vsc_prompt_cmd)
    preexec_functions+=(__vsc_preexec_only)
else
    __vsc_dbg_trap="$(trap -p DEBUG | cut -d' ' -f3 | tr -d \')"
    if [[ -z "$__vsc_dbg_trap" ]]; then
        __vsc_preexec_only() {
            if [ "$__vsc_in_command_execution" = "0" ]; then
                __vsc_in_command_execution="1"
                __vsc_preexec
            fi
        }
        trap '__vsc_preexec_only "$_"' DEBUG
    elif [[ "$__vsc_dbg_trap" != '__vsc_preexec "$_"' && "$__vsc_dbg_trap" != '__vsc_preexec_all "$_"' ]]; then
        __vsc_preexec_all() {
            if [ "$__vsc_in_command_execution" = "0" ]; then
                __vsc_in_command_execution="1"
                builtin eval ${__vsc_dbg_trap}
                __vsc_preexec
            fi
        }
        trap '__vsc_preexec_all "$_"' DEBUG
    fi
fi

__vsc_update_prompt

__vsc_prompt_cmd_original() {
    __vsc_status="$?"
    if [[ ${IFS+set} ]]; then
        __vsc_original_ifs="$IFS"
    fi
    if [[ "$__vsc_original_prompt_command" =~ .+\;.+ ]]; then
        IFS=';'
    else
        IFS=' '
    fi
    builtin read -ra ADDR <<<"$__vsc_original_prompt_command"
    if [[ ${__vsc_original_ifs+set} ]]; then
        IFS="$__vsc_original_ifs"
        unset __vsc_original_ifs
    else
        unset IFS
    fi
    for ((i = 0; i < ${#ADDR[@]}; i++)); do
        (exit ${__vsc_status})
        builtin eval ${ADDR[i]}
    done
    __vsc_precmd
}

__vsc_prompt_cmd() {
    __vsc_status="$?"
    __vsc_precmd
}

if [[ "$PROMPT_COMMAND" =~ (.+\;.+) ]]; then
    # item1;item2...
    __vsc_original_prompt_command="$PROMPT_COMMAND"
else
    # (item1, item2...)
    __vsc_original_prompt_command=${PROMPT_COMMAND[@]}
fi

if [[ -z "${bash_preexec_imported:-}" ]]; then
    if [[ -n "$__vsc_original_prompt_command" && "$__vsc_original_prompt_command" != "__vsc_prompt_cmd" ]]; then
        PROMPT_COMMAND=__vsc_prompt_cmd_original
    else
        PROMPT_COMMAND=__vsc_prompt_cmd
    fi
fi

export TERM=xterm-256color