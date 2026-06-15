import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class DockerSetup:
    """FSE Cloud Docker Setup: የቦቱን የማሰማራት (Deployment) ሂደት ይቆጣጠራል።"""

    def __init__(self, image_name="fse-bot", container_name="fse-container"):
        self.image_name = image_name
        self.container_name = container_name

    def build_image(self):
        logger.info("🐳 Building Docker Image...")
        cmd = ["docker", "build", "-t", self.image_name, "."]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info("✅ Docker Image Built Successfully")
        else:
            logger.error(f"❌ Build Failed: {result.stderr}")

    def run_container(self):
        # ቀድሞ የሚሮጥ ኮንቴይነር ካለ አቁም
        if self.check_container_status():
            logger.warning("⚠️ Container already running. Stopping for restart...")
            self.stop_container()

        logger.info("🚀 Starting FSE Container...")
        
        # ደህንነቱ በተጠበቀ ሁኔታ የAPI መረጃዎችን ማለፍ
        env_vars = {
            "BINANCE_API_KEY": os.getenv("BINANCE_API_KEY", ""),
            "BINANCE_API_SECRET": os.getenv("BINANCE_API_SECRET", ""),
            "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN", "")
        }

        env_flags = []
        for k, v in env_vars.items():
            env_flags += ["-e", f"{k}={v}"]

        cmd = ["docker", "run", "-d", "--name", self.container_name, *env_flags, self.image_name]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"✅ Container Started: {result.stdout.strip()}")
        else:
            logger.error(f"❌ Container Failed to Start: {result.stderr}")

    def stop_container(self):
        logger.info("🛑 Stopping Container...")
        subprocess.run(["docker", "stop", self.container_name], capture_output=True)
        subprocess.run(["docker", "rm", self.container_name], capture_output=True)
        logger.info("✅ Container Stopped & Removed")

    def check_container_status(self):
        """ኮንቴይነሩ እየሮጠ መሆኑን ለማረጋገጥ።"""
        cmd = ["docker", "ps", "-q", "-f", f"name={self.container_name}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return len(result.stdout.strip()) > 0

    def safe_restart(self):
        """ቦቱ ሳይደራረብ እንዲጀመር ማድረግ።"""
        self.stop_container()
        self.run_container()

if __name__ == "__main__":
    setup = DockerSetup()
    setup.build_image()
    setup.run_container()
