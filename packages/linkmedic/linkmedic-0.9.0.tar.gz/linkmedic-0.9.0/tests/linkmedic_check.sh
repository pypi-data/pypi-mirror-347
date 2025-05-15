#!/bin/bash
# This script runs the linkmedic and compares the number of reported dead links with the reference value provided to it.
# It also compares the links discovered by the crawler and compares it to each test's links file.
# if the number of reported dead links and the reference does not match, or the discovered links were diffrent, it exits with a non-zero code.
#
# requirements:
#
## which
## jq
## diff
## check-jsonschema [optional]

# Default values
_arg_launcher=""
_arg_test_name_filter="test_*"

print_help() {
  printf '%s\n' "Tester script to compare the output of linkmedic with the expected values"
  printf 'Usage: %s [--launcher <arg>] [--name-filter <arg>] [--help] \n' "$0"
  printf '\t%s\n' "--launcher: test launcher executable"
  printf '\t%s\n' "--name-filter: test file name filter (default: 'test_*')"
  printf '\t%s\n' "--help: print help (this list!)"
}

parse_commandline() {
  while test $# -gt 0; do
    _key="$1"
    case "$_key" in
    --launcher)
      test $# -lt 2 && echo "Missing value for the optional argument '$_key'." && exit 2
      _arg_launcher="$2"
      shift
      ;;
    --launcher=*)
      _arg_launcher="${_key##--launcher=}"
      ;;
    --name-filter=*)
      _arg_test_name_filter="${_key##--name-filter=}"
      ;;
    --help)
      print_help
      exit 0
      ;;
    *)
      echo "ERROR: Unknown flag: $_key"
      ;;
    esac
    shift
  done
}

verify_badge_color() {
  local _badge_info_file=$1
  local _badge_type=$2

  declare -A badge_fail_color
  badge_fail_color["critical"]="red"
  badge_fail_color["warning"]="yellow"

  declare -A badge_pass_color
  badge_pass_color["critical"]="green"
  badge_pass_color["warning"]="green"

  _badge_message=$(jq '.message' <"$_badge_info_file")
  _badge_color=$(jq '.color' <"$_badge_info_file")

  if [ "$_badge_message" == "0" ]; then
    expected_color="${badge_pass_color["$_badge_type"]}"
  else
    expected_color="${badge_fail_color["$_badge_type"]}"
  fi

  if [ "$_badge_color" == "\"$expected_color\"" ]; then
    echo -e "${color_green}* Badge color ($_badge_color) is correct!${color_reset}"
  else
    echo -e "${color_red}* Badge color IS NOT correct!"
    echo -e "** Badge type: $_badge_type"
    echo -e "** EXPECTED: \"$expected_color\", ACTUAL: $_badge_color ${color_reset}"
    _test_failed=true
  fi

}

compare_badge_info_file_to_ref() {
  local _badge_info_file=$1
  local _ref_count=$2
  local _badge_type=$3

  local _badge_name_json=${_badge_info_file##badge.}
  local _badge_name=${_badge_name_json%.json}
  local _reported
  _reported=$(jq '.message' <"$_badge_info_file")

  if [ "$_ref_count" != "0" ]; then
    if [ "$_ref_count" != "$_reported" ]; then
      echo -e "${color_red}* Number of reported $_badge_name in $_badge_info_file IS NOT CORRECT!"
      echo -e "** EXPECTED: $_ref_count, REPORTED: $_reported ${color_reset}"
      _test_failed=true
    else
      echo -e "${color_green}* Number of reported $_badge_name in $_badge_info_file is correct!"
      echo -e "** EXPECTED: $_ref_count, REPORTED: $_reported ${color_reset}"
    fi
  elif [ "$_reported" != "0" ]; then
    echo -e "${color_red}* UNEXPECTED DEAD LINKS REPORTED IN BADGE INFO FILE \"$_badge_info_file\"!"
    echo -e "** EXPECTED: 0, REPORTED: $_reported ${color_reset}"
    _test_failed=true
  fi
}

validate_badge_info_file() {
  local _badge_info_file=$1
  local _ref_count=$2
  local _badge_type=$3

  if [ -f "$_badge_info_file" ]; then
    if [[ -x "$(command -v check-jsonschema)" ]]; then
      printf "* Validating badge format: "
      if check-jsonschema --schemafile "$_badge_schema" "$(realpath "$_badge_info_file")"; then
        echo -e "${color_green}* Generated badge info file ($_badge_info_file) conforms to the schema.${color_reset}"
      else
        echo -e "${color_red}* BADGE INFO FILE ($_badge_info_file) DOES NOT CONFORM TO THE PROVIDED SCHEMA ($_badge_schema)!${color_reset}"
        _test_failed=true
      fi
    else
      echo -e "${color_yellow}* check-jsonschema was not found! Skipping schema verification...${color_reset}"
    fi
    compare_badge_info_file_to_ref "$_badge_info_file" "$_ref_count" "$_badge_type"
    verify_badge_color "$_badge_info_file" "$_badge_type"

  elif [ "$_ref_count" != "0" ]; then
    echo -e "${color_red}* BADGE INFO FILE $_badge_info_file WAS NOT FOUND!${color_reset}"
    _test_failed=true
  fi
}

validate_discovered_links() {

  _diff_output=$(diff linkmedic.links "$1" 2>&1)
  _diff_exit=$?
  if [[ $_diff_exit -eq 0 ]]; then
    echo -e "${color_green}* All links are correctly discovered.${color_reset}"
  elif [[ $_diff_exit -eq 1 ]]; then
    echo -e "${color_red}* Not all links are correctly discovered!${color_reset}"
    echo -e "${color_red}* diff output:\n$_diff_output${color_reset}"
    _test_failed=true
  else
    echo -e "${color_red}* Command failed: $_diff_output${color_reset}"
    _test_failed=true
  fi
}

_requirements=('which' 'jq' 'diff')

# make sure requirements exist
for _requirement in "${_requirements[@]}"; do
  if ! [[ -x "$(command -v "$_requirement")" ]]; then
    echo "ERROR: $_requirement was not found!"
    exit 1
  fi
done

parse_commandline "$@"

color_red="\033[31;49;1m"
color_green="\033[32;49;1m"
color_yellow="\033[33;49;1m"
color_reset="\033[0m"
_test_files_path=$(dirname "$0")
_badge_schema="$_test_files_path/badges/badge.schema.json"

_failed_tests_count=0
for _test_file in "$_test_files_path/"$_arg_test_name_filter; do
  [[ $_test_file == *.links ]] && continue
  if [[ ! $_test_file =~ .*test_[0-9]{2}$ ]]; then
    echo -e "${color_red}* Unexpected file in tests directory: $_test_file${color_reset}"
    _failed_tests_count=$((_failed_tests_count + 1))
    continue
  fi
  # cleanup env.
  rm -f badge.* linkmedic.links
  _test_failed=false

  # shellcheck source=tests/test_01
  source "$_test_file" || echo "could not read: $_test_file"

  echo "============================================================"
  echo "* Test file                   : $_test_file"
  echo "* Test description            : $_test_description"
  echo "* Website Root                : $_test_website_root"
  echo "* Extra linkmedic flags       : $_test_extra_flags"
  echo "* Test launcher               : $_arg_launcher"
  echo "* Expected internal dead links: $_test_expected_dead_internal"
  echo "* Expected external dead links: $_test_expected_dead_external"
  echo "* Expected total dead links   : $_test_expected_dead_total"
  echo "* Expected exit code          : $_test_expected_exit_code"
  echo "* Expected HTTP links         : $_test_expected_http_links"
  if [[ -f "$_test_files_path/$_test_website_root/.linkignore" ]]; then
    echo "* .linkignore:"
    while read -r linkignore_line || [[ -n "$linkignore_line" ]]; do
      echo "  > $linkignore_line"
    done <"$_test_files_path/$_test_website_root/.linkignore"
  fi

  IFS=' ' read -ra _test_extra_flags_list <<<"$_test_extra_flags"
  echo "++ $_arg_launcher" "linkmedic" "${_test_extra_flags_list[@]}" "--with-badge" "--dump-links" "--root=$_test_files_path/$_test_website_root"
  command $_arg_launcher "linkmedic" "${_test_extra_flags_list[@]}" "--with-badge" "--dump-links" "--root=$_test_files_path/$_test_website_root"
  test_exit_code=$?
  echo "* Test exit code = $test_exit_code"

  if [[ "$_test_expected_exit_code" -ge 2 ]]; then
    if [ "$test_exit_code" != "$_test_expected_exit_code" ]; then
      echo -e "${color_red}* Unexpected return code!"
      echo -e "** EXPECTED: $_test_expected_exit_code, RETURNED: $test_exit_code ${color_reset}"
      _test_failed=true
    fi
    echo -e "${color_green}* Return code is as expected!${color_reset}"
  else
    if [[ "$_test_expected_exit_code" == "0" ]]; then
      if [[ "$test_exit_code" != "0" ]]; then
        echo -e "${color_red}* Unexpected links checker failure! Either unexpected dead links are reported or the link checker exited unexpectedly!${color_reset}"
        _test_failed=true
      fi
      echo -e "${color_green}* As expected, no dead links were reported!${color_reset}"
    elif [[ "$_test_expected_exit_code" == "1" ]]; then
      if [[ "$test_exit_code" == "0" ]]; then
        echo -e "${color_red}* Some dead links were not reported!${color_reset}"
        _test_failed=true
      fi
      echo -e "${color_green}* As expected, dead links were reported!${color_reset}"
    fi

    validate_badge_info_file "badge.dead_internal_links.json" "$_test_expected_dead_internal" "critical"
    validate_badge_info_file "badge.dead_external_links.json" "$_test_expected_dead_external" "critical"
    validate_badge_info_file "badge.dead_links.json" "$_test_expected_dead_total" "critical"
    validate_badge_info_file "badge.http_links.json" "$_test_expected_http_links" "warning"
    validate_discovered_links "$_test_file.links"

    if [[ "$_test_failed" == true ]]; then
      _failed_tests_count=$((_failed_tests_count + 1))
      echo "* TEST FAILED! Restarting the test with debug logging..."
      command $_arg_launcher "linkmedic" "${_test_extra_flags_list[@]}" "--with-badge" "--dump-links" "--root=$_test_files_path/$_test_website_root" "-v"
    fi
  fi

  unset _test_website_root _test_extra_flags _test_expected_dead_internal _test_expected_dead_external _test_expected_dead_total _test_expected_exit_code _test_expected_http_links
done

rm -f badge.* linkmedic.links

echo "==================================="
if [[ $_failed_tests_count -ne 0 ]]; then
  echo "ERROR: $_failed_tests_count test(s) failed!"
  exit 1
else
  echo "All tests passed!"
fi
