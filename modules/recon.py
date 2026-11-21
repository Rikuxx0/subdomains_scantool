import os

from utils.executor import logger, run_command


def _read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def _write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in sorted(set(lines)):
            f.write(line + "\n")


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

    logger.info("Step 1.1: Running Subfinder...")
    run_command(["subfinder", "-d", domain, "-all", "-o", sub_txt])

    if github_token:
        logger.info("Step 1.2: Running github-subdomains...")
        run_command(["github-subdomains", "-d", domain, "-t", github_token, "-o", github_txt], secret_args=(github_token,))
    else:
        logger.info("GitHub token not provided. Skipping github-subdomains.")

    subbrute_path = "tools/subbrute/subbrute.py"
    if os.path.exists(subbrute_path):
        logger.info("Step 1.3: Running SubBrute...")
        run_command(["python3", subbrute_path, "-s", "tools/subbrute/names.txt", domain, "-o", brute_txt])
    else:
        logger.info("SubBrute not found. Skipping brute-force.")

    logger.info("Step 1.4: Merging and deduplicating subdomains...")
    _write_lines(domain_txt, _read_lines(sub_txt) + _read_lines(github_txt) + _read_lines(brute_txt))

    logger.info("Step 1.5: Running httpx for liveness check...")
    run_command(["httpx", "-l", domain_txt, "-sc", "-o", alive_txt])
    alive_hosts = [line.split()[0] for line in _read_lines(alive_txt)]

    logger.info("Step 2.1: Running waybackurls...")
    run_command(["waybackurls"], input_text="\n".join(alive_hosts) + "\n", output_file=urls_txt)

    logger.info("Step 2.2: Running katana...")
    katana_input = os.path.join(output_dir, "katana_input.txt")
    _write_lines(katana_input, alive_hosts)
    run_command(["katana", "-list", katana_input, "-jc", "-o", url2_txt])

    logger.info("Step 2.3: Merging and deduplicating all URLs...")
    _write_lines(all_urls_txt, _read_lines(urls_txt) + _read_lines(url2_txt))
    logger.info("Reconnaissance phase completed.")
    return all_urls_txt, alive_txt
