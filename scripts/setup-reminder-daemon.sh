#!/bin/bash

#
# setup-reminder-daemon.sh
# One-time installation of the reminder daemon as a persistent cron job
#
# Usage: bash scripts/setup-reminder-daemon.sh [install|uninstall|status|test]
#

set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
DAEMON_SCRIPT="${WORKSPACE}/scripts/reminder-daemon.sh"
CRON_JOB_NAME="openclaw-reminder-daemon"
LOG_FILE="${WORKSPACE}/logs/reminder-daemon.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

check_requirements() {
    local missing=0
    
    if ! command -v curl &> /dev/null; then
        echo "❌ curl is required but not installed"
        missing=1
    fi
    
    if [ ! -f "${DAEMON_SCRIPT}" ]; then
        echo "❌ Daemon script not found: ${DAEMON_SCRIPT}"
        missing=1
    fi
    
    if [ ! -f "${WORKSPACE}/config/reminders.json" ]; then
        echo "❌ Config file not found: ${WORKSPACE}/config/reminders.json"
        missing=1
    fi
    
    if [ ! -f "${WORKSPACE}/.credentials/telegram_bot_config.txt" ]; then
        echo "❌ Telegram credentials not found: ${WORKSPACE}/.credentials/telegram_bot_config.txt"
        missing=1
    fi
    
    return $missing
}

install_cron() {
    log "Installing cron job..."
    
    # Create cron entry (runs every 5 minutes)
    local cron_entry="*/5 * * * * cd ${WORKSPACE} && bash ${DAEMON_SCRIPT} >> ${LOG_FILE} 2>&1"
    
    # Check if job already exists
    if crontab -l 2>/dev/null | grep -F "${DAEMON_SCRIPT}" &>/dev/null; then
        log "⚠️  Cron job already exists, removing old entry first..."
        crontab -l | grep -v "${DAEMON_SCRIPT}" | crontab - || true
    fi
    
    # Add new cron entry
    (crontab -l 2>/dev/null || true; echo "$cron_entry") | crontab -
    
    log "✅ Cron job installed successfully"
    log "   Runs every 5 minutes"
    log "   Log: ${LOG_FILE}"
}

uninstall_cron() {
    log "Uninstalling cron job..."
    
    if crontab -l 2>/dev/null | grep -F "${DAEMON_SCRIPT}" &>/dev/null; then
        crontab -l | grep -v "${DAEMON_SCRIPT}" | crontab -
        log "✅ Cron job removed"
    else
        log "⚠️  Cron job not found (nothing to remove)"
    fi
}

show_status() {
    log "Reminder Daemon Status"
    log "====================="
    
    if crontab -l 2>/dev/null | grep -F "${DAEMON_SCRIPT}" &>/dev/null; then
        log "✅ Cron job installed"
        log ""
        log "Cron entry:"
        crontab -l | grep "${DAEMON_SCRIPT}"
    else
        log "❌ Cron job not installed"
    fi
    
    log ""
    log "Log file: ${LOG_FILE}"
    if [ -f "${LOG_FILE}" ]; then
        log "Last 10 entries:"
        tail -10 "${LOG_FILE}" || true
    else
        log "(log file not yet created)"
    fi
}

test_daemon() {
    log "Testing daemon..."
    log ""
    
    if ! check_requirements; then
        log "❌ Missing requirements"
        return 1
    fi
    
    log "✅ All requirements met"
    log ""
    
    log "Running single daemon check..."
    if bash "${DAEMON_SCRIPT}"; then
        log "✅ Daemon executed successfully"
        log ""
        log "Recent log output:"
        tail -5 "${LOG_FILE}" || true
    else
        log "❌ Daemon execution failed"
        return 1
    fi
}

main() {
    local action="${1:-install}"
    
    case "$action" in
        install)
            if ! check_requirements; then
                log "❌ Setup failed due to missing requirements"
                exit 1
            fi
            mkdir -p "$(dirname "${LOG_FILE}")"
            install_cron
            log ""
            log "Next step: Run 'bash scripts/setup-reminder-daemon.sh test' to verify"
            ;;
        uninstall)
            uninstall_cron
            ;;
        status)
            show_status
            ;;
        test)
            if ! check_requirements; then
                log "❌ Test failed due to missing requirements"
                exit 1
            fi
            test_daemon
            ;;
        *)
            echo "Usage: $0 [install|uninstall|status|test]"
            echo ""
            echo "  install  - Install daemon as cron job (runs every 5 min)"
            echo "  uninstall- Remove cron job"
            echo "  status   - Show installation status and recent logs"
            echo "  test     - Run a single daemon check and show results"
            exit 1
            ;;
    esac
}

main "$@"
