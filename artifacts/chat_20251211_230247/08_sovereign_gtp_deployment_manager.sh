export AI_METAVERSE_BASE="/data/data/com.termux/files/home/storage/shared/AiMetaverse/plan_aimeta001"
export ART_DIR="$AI_METAVERSE_BASE/artifacts/chat_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$ART_DIR"
cat > "$ART_DIR/00_MANIFEST.md" <<'MD'
# Chat Artifacts Manifest

Paste each ChatGPT Artifact into its matching file below.

## Files
- 01_yesquid_pro_coding_standards.md
- 02_sovereign_gtp_system_fix_setup.md
- 03_sovereign_gtp_troubleshooting_guide.md
- 04_fixed_sovereign_monetization_build.md
- 05_project_dependencies_configuration.md
- 06_quick_fix_for_current_errors.md
- 07_emergency_system_recovery_script.sh
- 08_sovereign_gtp_deployment_manager.sh
- 09_quick_command_shortcuts.md
- 10_yesquid_webhook_complete_setup_guide.md
- 11_complete_agent_scripts_setup.sh
- 12_master_implementation_guide_complete_setup.md
- 13_one_script_complete_installer.sh
- 14_fixed_sovereign_swarm_deployment_system.sh

## Notes
- Keep original text unedited for provenance
- If a file is bash, preserve the shebang and chmod +x
MD

# create empty files so you can paste directly
touch \
  "$ART_DIR/01_yesquid_pro_coding_standards.md" \
  "$ART_DIR/02_sovereign_gtp_system_fix_setup.md" \
  "$ART_DIR/03_sovereign_gtp_troubleshooting_guide.md" \
  "$ART_DIR/04_fixed_sovereign_monetization_build.md" \
  "$ART_DIR/05_project_dependencies_configuration.md" \
  "$ART_DIR/06_quick_fix_for_current_errors.md" \
  "$ART_DIR/07_emergency_system_recovery_script.sh" \
  "$ART_DIR/08_sovereign_gtp_deployment_manager.sh" \
  "$ART_DIR/09_quick_command_shortcuts.md" \
  "$ART_DIR/10_yesquid_webhook_complete_setup_guide.md" \
  "$ART_DIR/11_complete_agent_scripts_setup.sh" \
  "$ART_DIR/12_master_implementation_guide_complete_setup.md" \
  "$ART_DIR/13_one_script_complete_installer.sh" \
  "$ART_DIR/14_fixed_sovereign_swarm_deployment_system.sh"

echo "[✓] Ready. Paste artifacts into: $ART_DIR"
