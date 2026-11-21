import argparse
import sys
import os
import shutil

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.recon import run_recon
from modules.scan import run_active_scan
from utils.executor import logger

def main():
    parser = argparse.ArgumentParser(description="Recon-to-Passive-Scan Automation Pipeline")
    parser.add_argument("-d", "--domain", required=True, help="Target domain for scanning")
    parser.add_argument("-t", "--token", help="GitHub token for github-subdomains (optional)")
    parser.add_argument("--active", action="store_true", help="Enable active scanning phase")
    parser.add_argument("-o", "--output", default="outputs", help="Output directory (default: outputs)")

    args = parser.parse_args()

    required = ["subfinder", "httpx", "waybackurls", "katana"]
    if args.token:
        required.append("github-subdomains")
    if args.active:
        required.append("nuclei")
    missing = [tool for tool in required if shutil.which(tool) is None]
    if missing:
        logger.error("Missing required tools: %s. Run ./install_tools.sh and add the Go bin directory to PATH.", ", ".join(missing))
        sys.exit(1)

    logger.info("Starting Recon-to-Scan pipeline for target: %s", args.domain)

    try:
        # Step 1: Reconnaissance
        all_urls_txt, alive_txt = run_recon(args.domain, github_token=args.token, output_dir=args.output)
        
        # Step 2: Active Scanning (Optional)
        if args.active:
            logger.info("Active scanning flag detected. Proceeding to active scanning phase...")
            run_active_scan(all_urls_txt, alive_txt, output_dir=args.output)
        else:
            logger.info("Active scanning not requested. Use --active to trigger it.")

        logger.info(f"Pipeline finished! Results are in the '{args.output}' directory.")
    
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
