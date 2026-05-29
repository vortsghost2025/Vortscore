#!/usr/bin/env bash
set -e

DIAGNOSTIC_FILE="/home/droid/vitalis_core/vitalis_system_compilation.log"
rm -f "$DIAGNOSTIC_FILE"

{
  echo "========================================================================="
  echo "         FERRELL SYNTHETIC INTELLIGENCE - FULL PRODUCTION TREE AUDIT     "
  echo "========================================================================="
  echo "Timestamp: $(date -u)"
  echo "Directory Topology:"
  echo "------------------"
  find . -maxdepth 3 -not -path '*/.*'
  echo ""
  
  TARGET_FILES=("app.py" "run_vitalis.py" "requirements.txt" "README.md" "core/brain.py" "extensions/dreamer.py" "extensions/temp_scheduler.py" "extensions/evolutionary_lora.py" "plugins/self_audit_tool.py")
  
  for file in "${TARGET_FILES[@]}"; do
    if [ -f "$file" ]; then
      echo "========================================================================="
      echo " FILE PATH: $file"
      echo "========================================================================="
      cat "$file"
      echo -e "\n\n"
    else
      echo "[-] WARNING: Core asset file missing from current directory structure: $file"
    fi
  done
} > "$DIAGNOSTIC_FILE"

echo -e "\033[92m[+] SUCCESS: Every file and structural layer has been printed into a single log.\033[0m"
echo -e "\033[94m[*] View the complete code assembly layout by running: cat $DIAGNOSTIC_FILE\033[0m"
