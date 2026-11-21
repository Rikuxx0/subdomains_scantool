#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

for tool in go python3; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        printf 'Required tool not found: %s\n' "$tool" >&2
        exit 1
    fi
done

python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# These four tools are required for the default reconnaissance run.
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest

install_optional() {
    local name="$1"
    shift
    if ! "$@"; then
        printf 'Optional tool %s could not be installed; continuing.\n' "$name" >&2
    fi
}

install_optional github-subdomains go install github.com/gwen001/github-subdomains@latest
install_optional subzy go install github.com/LukaSikic/subzy@latest
install_optional nuclei go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
install_optional wafw00f .venv/bin/python -m pip install wafw00f

printf 'Core tools installed. Activate the Python environment and add Go binaries to PATH:\n'
printf '  source .venv/bin/activate\n'
printf '  export PATH="$(go env GOPATH)/bin:$PATH"\n'
printf 'Optional SubBrute and NucleiFuzzer are not installed by this script.\n'
