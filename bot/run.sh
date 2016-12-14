#!/bin/sh

SLEEP_TIME_SECONDS=60
DEBUG_ENABLED=true

EXIT_STATUS_TO_HALT_BOT=55
RUN_BOT_COMMAND="./main.py"


is_first_execution()
{
    [ "$RE_RUNNING" != "true" ]
}

perform_first_execution_tasks()
{
    cd_to_current_script_location
    update_code
    rerun_current_script
}

cd_to_current_script_location()
{
    current_script_location="$(dirname "$0")"
    cd "$current_script_location"
}

perform_main_tasks()
{
    build_bot
    run_bot
    check_halt_received $?
    sleep ${SLEEP_TIME_SECONDS}
    update_code
    rerun_current_script
}

build_bot()
{
    git rev-parse --short HEAD > config/prod_game_tag
}

run_bot()
{
    debug "Starting bot"
    "$RUN_BOT_COMMAND"
    exit_status=$?
    debug "Bot finished"
    return ${exit_status}
}

check_halt_received()
{
    exit_status="$1"
    if should_stop_execution "$exit_status"
    then
        debug "Halt received, stopping"
        exit "$exit_status"
    fi
}

should_stop_execution()
{
    exit_status="$1"
    [ "$exit_status" -eq "$EXIT_STATUS_TO_HALT_BOT" ]
}

update_code()
{
    debug "Updating code (pulling from repo)"
    git pull
}

rerun_current_script()
{
    current_script_name="$(basename "$0")"
    RE_RUNNING=true
    . "./$current_script_name"
}

debug()
{
    if [ "$DEBUG_ENABLED" = "true" ]
    then
        echo ">> $@"
    fi
}


if is_first_execution
then
    perform_first_execution_tasks
else
    perform_main_tasks
fi
