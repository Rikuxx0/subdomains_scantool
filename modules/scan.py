import os
import shutil
from utils.executor import run_command, logger

def run_active_scan(all_urls_txt, alive_txt, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    
    waf_txt = os.path.join(output_dir, "waf.txt")
    takeover_txt = os.path.join(output_dir, "takeover.txt")
    nuclei_results = os.path.join(output_dir, "nuclei_results.txt")
    fuzzer_results = os.path.join(output_dir, "fuzzer_results.txt")

    # 3.1 WAF Detection
    if shutil.which("wafw00f"):
        logger.info("Step 3.1: Running wafw00f...")
        run_command(f"wafw00f -l {alive_txt} -o {waf_txt}")
    else:
        logger.warning("wafw00f not found. Skipping WAF detection.")

    # 3.2 Subdomain Takeover
    if shutil.which("subzy"):
        logger.info("Step 3.2: Running subzy...")
        run_command(f"subzy run --targets {alive_txt} --output {takeover_txt}")
    else:
        logger.warning("subzy not found. Skipping takeover check.")

    # 3.3 Nuclei Template Scanning
    logger.info("Step 3.3: Running Nuclei...")
    # Using a variety of templates as specified
    run_command(f"nuclei -l {all_urls_txt} -t exposure/tokens,exposures/configs,vulnerabilities,cves -o {nuclei_results}")

    # 3.4 NucleiFuzzer
    nf_path = shutil.which("nf") or shutil.which("nucleifuzzer")
    if nf_path:
        logger.info(f"Step 3.4: Running NucleiFuzzer using {nf_path}...")
        run_command(f"{nf_path} -f {all_urls_txt} -o {fuzzer_results}")
    else:
        logger.warning("NucleiFuzzer (nf) not found. Skipping fuzzer scan.")

    # 3.5 Broken Link Checker (via Nuclei)
    logger.info("Step 3.5: Checking for Broken Links (Hijacking) via Nuclei...")
    run_command(f"nuclei -l {all_urls_txt} -tags broken-link-hijacking -o {os.path.join(output_dir, 'broken_links.txt')}")

    logger.info("Active scanning phase completed.")
