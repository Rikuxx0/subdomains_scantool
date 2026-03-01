#!/bin/bash

# Recon-to-Scan External Tools Installation Script

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}[*] Starting tool installation...${NC}"

# Check for Go
if ! command -v go &> /dev/null; then
    echo -e "${RED}[!] Go is not installed. Please install Go first: https://golang.org/doc/install${NC}"
    exit 1
fi

# Check for Python/Pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[!] pip3 is not installed. Please install Python 3 and pip.${NC}"
    exit 1
fi

# 1. Install Python dependencies
echo -e "${GREEN}[*] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt
pip3 install wafw00f

# 2. Install Go-based tools
echo -e "${GREEN}[*] Installing Go-based tools...${NC}"

echo -e "${GREEN}[+] Installing subfinder...${NC}"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

echo -e "${GREEN}[+] Installing github-subdomains...${NC}"
go install -v github.com/gwen001/github-subdomains@latest

echo -e "${GREEN}[+] Installing httpx...${NC}"
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

echo -e "${GREEN}[+] Installing waybackurls...${NC}"
go install -v github.com/tomnomnom/waybackurls@latest

echo -e "${GREEN}[+] Installing katana...${NC}"
go install -v github.com/projectdiscovery/katana/cmd/katana@latest

echo -e "${GREEN}[+] Installing subzy...${NC}"
go install -v github.com/LukaSikic/subzy@latest

echo -e "${GREEN}[+] Installing nuclei...${NC}"
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

echo -e "${GREEN}[+] Installing gf...${NC}"
go install -v github.com/tomnomnom/gf@latest

echo -e "${GREEN}[+] Installing NucleiFuzzer (nf)...${NC}"
# Note: NucleiFuzzer is often a script, but sometimes distributed as a binary.
# This assumes the binary version or the common installation method.
go install -v github.com/0xKayala/NucleiFuzzer@latest

echo -e "${GREEN}[+] Installing subBrute...${NC}"
if [ ! -d "tools/subbrute" ]; then
    mkdir -p tools
    git clone https://github.com/TheRook/subbrute.git tools/subbrute
fi
pip3 install -r tools/subbrute/requirements.txt

echo -e "${GREEN}[*] Installation complete!${NC}"
echo -e "${GREEN}[*] Please ensure ~/go/bin is in your PATH.${NC}"
echo -e "${GREEN}[*] Example: export PATH=\$PATH:\$(go env GOPATH)/bin${NC}"
