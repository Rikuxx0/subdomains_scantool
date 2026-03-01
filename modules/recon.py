import os
from utils.executor import run_command, logger

def run_recon(domain, github_token=None, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    
    sub_txt = os.path.join(output_dir, "sub.txt")
    github_txt = os.path.join(output_dir, "github.txt")
    brute_txt = os.path.join(output_dir, "brute.txt")
    domain_txt = os.path.join(output_dir, "domain.txt")
    alive_txt = os.path.join(output_dir, "alive.txt")
    urls_txt = os.path.join(output_dir, "urls.txt")
    url2_txt = os.path.join(output_dir, "url2.txt")
    all_urls_txt = os.path.join(output_dir, "all_urls.txt")

    # 1.1 Subfinder
    logger.info("Step 1.1: Running Subfinder...")
    run_command(f"subfinder -d {domain} -all -o {sub_txt}")

    # 1.2 GitHub Subdomains
    if github_token:
        logger.info("Step 1.2: Running github-subdomains...")
        run_command(f"github-subdomains -d {domain} -t {github_token} -o {github_txt}")
    else:
        logger.warning("GitHub token not provided. Skipping github-subdomains.")
        with open(github_txt, 'w') as f:
            pass

    # 1.3 SubBrute
    subbrute_path = "tools/subbrute/subbrute.py"
    if os.path.exists(subbrute_path):
        logger.info("Step 1.3: Running SubBrute...")
        # Note: subbrute needs a wordlist, it usually comes with names.txt
        wordlist = "tools/subbrute/names.txt"
        run_command(f"python3 {subbrute_path} -s {wordlist} {domain} -o {brute_txt}")
    else:
        logger.warning("SubBrute not found. Skipping brute-force.")
        with open(brute_txt, 'w') as f:
            pass

    # 1.4 Integration / Deduplication
    logger.info("Step 1.4: Merging and deduplicating subdomains...")
    run_command(f"cat {sub_txt} {github_txt} {brute_txt} | sort -u > {domain_txt}")

    # 1.4 Liveness check
    logger.info("Step 1.4: Running httpx for liveness check...")
    run_command(f"httpx -l {domain_txt} -sc -o {alive_txt}")

    # 2. Content Discovery
    logger.info("Step 2.1: Running waybackurls...")
    # waybackurls usually takes input from stdin
    run_command(f"cat {alive_txt} | cut -d' ' -f1 | waybackurls > {urls_txt}")

    logger.info("Step 2.2: Running katana...")
    run_command(f"katana -list {alive_txt} -jc -o {url2_txt}")

    logger.info("Step 2.3: Merging and deduplicating all URLs...")
    run_command(f"cat {urls_txt} {url2_txt} | sort -u > {all_urls_txt}")

    logger.info("Reconnaissance phase completed.")
    return all_urls_txt, alive_txt
